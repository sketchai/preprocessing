def encode(f_i, f_o, lMax=lMax, n_bins=n_bins):
    """
    f_i : str, _filtered.npy output of the sift function;
    f_o : str, extension-less file for saving;
    lMax : int, maximal number of primitives. The sketches are padded to lMax primitives;
    n_bins : int, number of bins for the discretization of the parameters.
    """
    seqs = flat_array.load_flat_array(f_i)
    sequences_encoded = []
    
    params_edge, params_node = discretization.create_params(n_bins)

    for n,seq in enumerate(seqs):
        node_ops = [op for op in seq if isinstance(op, sequence.NodeOp)]
        edge_ops = [op for op in seq if isinstance(op, sequence.EdgeOp)]

        l = len(node_ops)            
        assert l <= lMax
        node_ops += [sequence.NodeOp('void')]*(lMax-l)

        node_features = torch.tensor([NODE_IDX_MAP[op.label] for op in node_ops], dtype=torch.int64)
        sparse_node_features = discretization.discretization_nodes(node_ops, params_node)

        edge_features = torch.tensor([EDGE_IDX_MAP[op.label] for op in edge_ops], dtype=torch.int64)
        sparse_edge_features = discretization.discretization_edges(edge_ops, params_edge)
        incidences = torch.tensor([[op.references[0], op.references[-1]] for op in edge_ops], dtype=torch.int64)

        i_edges_given = []
        i_edges_possible = []
        edges_exemple = torch.zeros((l, l), dtype=torch.bool)
        for i, op in enumerate(edge_ops):
            edges_exemple[op.references[0], op.references[-1]] = True
            edges_exemple[op.references[-1], op.references[0]] = True
            if op.label == sequence.ConstraintType.Subnode:  # à minima
                i_edges_given.append(i)
            else:
                i_edges_possible.append(i)
        i_edges_given = np.array(i_edges_given, dtype=np.int64)
        i_edges_possible = np.array(i_edges_possible, dtype=np.int64)
        edges_toInf_neg = torch.nonzero(torch.triu(~edges_exemple))

        mask_attention = torch.ones(lMax, dtype=torch.bool)
        mask_attention[:l] = False

        sequences_encoded.append({
            'node_ops': node_ops,
            'edge_ops': edge_ops,
            'length': l,
            'node_features': node_features,
            'sparse_node_features': sparse_node_features,
            'edge_features': edge_features,
            'sparse_edge_features': sparse_edge_features,
            'incidences': incidences,
            'i_edges_given': i_edges_given,
            'i_edges_possible': i_edges_possible,
            'edges_toInf_neg': edges_toInf_neg,
            'mask_attention': mask_attention
        })

    data = flat_array.save_list_flat(sequences_encoded)
    np.save(f_o+'_final.npy', data, allow_pickle=False)

    
def export_parameters(fo='data/', lMax=lMax, lMin=lMin, dof_max=dof_max, n_bins=n_bins, n_slice=1):
    """
    Save the preprocessing parameters; they are required for the training.

    TO DO : add the conf dict 
    """
    edge_feature_dimensions, node_feature_dimensions = discretization.feature_dims(*discretization.create_params(n_bins))
    
    with open(fo+'preprocessing_params.pkl', 'wb') as f:
        pickle.dump({'lMax': lMax, 'lMin': lMin, 'dof_max': dof_max, 'n_bins': n_bins,
                     'node_feature_dimensions': node_feature_dimensions,
                     'edge_feature_dimensions': edge_feature_dimensions,
                     }, f)