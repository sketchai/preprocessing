import numpy as np
from scipy.cluster.hierarchy import fclusterdata

from sketchgraphs.data import sequence
from maps.maps import *


def weighter(seqs, n_slice=1):
    """
    Underweights similar sketches. This is a two-time procedure. First, classes are formed looking at sketches with identical sequences of operations and references. Then among each class sketches are clustered according to their numerical parameters. One sketch per cluster is kept and its weight is the inverse of the number of clusters among the class; so, the distribution of classes is uniform.
    
    seqs : list of sequences;
    n_slice : int, number of slices used for parallel preprocessing. To assess the global frequencies of the sketches.
    """
    seqs_ops_encoded = []
    for i, seq in enumerate(seqs):
        seq_ops_encoded = []
        for op in seq:
            if isinstance(op, sequence.NodeOp):
                seq_ops_encoded.append(NODE_IDX_MAP[op.label])
            else:
                seq_ops_encoded.append(EDGE_IDX_MAP[op.label] + len(NODE_IDX_MAP))
                seq_ops_encoded.append(op.references[0] + len(NODE_IDX_MAP) + len(EDGE_IDX_MAP))
                seq_ops_encoded.append(op.references[-1] + len(NODE_IDX_MAP) + len(EDGE_IDX_MAP))
        seqs_ops_encoded.append(seq_ops_encoded)

    seqsD = {}
    for i, seq_ops_encoded in enumerate(seqs_ops_encoded):
        key = str(seq_ops_encoded)
        if key in seqsD:
            seqsD[key].append(i)
        else:
            seqsD[key] = [i]

    seqsU = []
    weights = []

    for key in seqsD:
        nbr_seq = len(seqsD[key])
        if nbr_seq==1:
            seqsU.append(seqs[seqsD[key][0]])
            weights.append(1.)
            continue

        l_params = 0
        seq_template = seqs[seqsD[key][0]]
        for op in seq_template:
            if isinstance(op, sequence.NodeOp):
                l_params += len(NODES_PARAMETRIZED.get(op.label, []))

        params = np.zeros((nbr_seq, l_params))

        for i, i_seq in enumerate(seqsD[key]):
            for op in seqs[i_seq]:
                for j, param in enumerate(NODES_PARAMETRIZED.get(op.label, [])):
                    if isinstance(op, sequence.NodeOp):
                        params[i, j] = float(op.parameters[param])

        clusters = fclusterdata(params, 0.2, metric='cityblock')
        clusters_added = [False]*max(clusters)
        n_clusters = max(clusters)
        clusters_added = [False]*n_clusters
        for i,c in enumerate(clusters):
            if not clusters_added[c-1]:
                seqsU.append(seqs[seqsD[key][i]])
                weights.append(1./n_clusters/n_slice)
                clusters_added[c-1] = True
            
    print("{:.1%} of the sketches were discarded by the weighter; the effective weight was reduced by {:.1%}.".format(1-len(seqsU)/len(seqs), 1-np.sum(weights)/len(seqs)))
    
    return seqsU, weights
