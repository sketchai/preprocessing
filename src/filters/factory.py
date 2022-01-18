
ACCEPTED_LABEL = NODE_IDX_MAP + EDGE_IDX_MAP


D_FILTERS = {'label': LabelFilter,
             'count': CountElementFilter,
             'type': ObjectTypeFilter}


def sift(f_i, f_o, lMax=lMax, lMin=lMin, dof_max=dof_max, n_slice=1):
    """
    Filters, normalizes and weights sketches. A coarse filtering is done according to: the types of primitives and constraints, the number of primitives and the remaing degrees of freedom.
    f_i : str, .npy file containing the sketches as a list or a dictionary {'sequences': list};
    f_o : str, extension-less file for saving;
    lMax : int, maximal number of primitives. The sketches will be padded to lMax primitives;
    lMin : int, minimal number of primitives;
    dof_max : int, maximal number of remaing degrees of freedom;
    n_slice : int, number of slices used for parallel preprocessing. Used for computing weights.
    """

    seqs = []

    for i, seq in enumerate(data):
        l = 0
        l_edge = 0
        filtre = False
        for op in seq:

            # Check object type
            if not filter_object(op):
                break

            # Check the label status
            if not filter_label(op):
                break

            # Check the node count
            if not filter_node(op, current_count):
                break

            # Check the edge count
            if
            else:
                l_edge += 1
                if op.label not in EDGE_IDX_MAP:
                    filtre = True
                    break
                if len(op.references) == 3:  # to-do: convert three-reference-'midpoints'
                    filtre = True
                    break

        if l < lMin or l > lMax:
            continue
        if l_edge == 0:  # in function encode, edge_ops must contain elements
            continue
        if filtre:
            continue
        if dof_max:
            if np.sum(dof.get_sequence_dof(seq)) > dof_max:
                continue

        seqs.append(seq)

    print("{:.1%} of the sketches were discarded by the first filter.".format(
        1 - len(seqs) / len(data)))

    seqs = normalization.normalization(seqs)
    seqsU, weights = weighter.weighter(seqs, n_slice)

    data = flat_array.save_list_flat(seqsU)
    np.save(f_o + '_filtered.npy', data, allow_pickle=False)

    data = flat_array.save_list_flat(weights)
    np.save(f_o + '_weights.npy', data, allow_pickle=False)


def construct_list_filters(conf: Dict):
    l_filters = []
    for filter_name, filter_config in conf.items():
        l_filters.append(D_FILTERS[filter_name](filter_config))
    return l_filters


def filters_factory(conf_filters: Dict, show_logs: bool = True) -> None:
    """
        This function applies a list of filters to a list of arrays.
        Inputs:
            l_op_filters (List) : Filter list that must be apply on each element of the sequence
            l_seq_filters (List) : Filter list that must be apply on the all sequence
        Outputs :
            filtered_seq (List) : List of the sequences conserved after a first filtering
    """
    l_op_filters = construct_list_filters(conf_filter.get('op', {}))
    l_seq_filters = construct_list_filters(conf_filter.get('seq', {}))

    filtered_seq = []
    for i, seq in enumerate(data):
        seq_status = True

        # Apply the op filters all along the sequence
        for op in seq[:-1]:
            for filter in l_op_filters:
                if not filter.check(op):
                    seq_status = False
                    filter.update_wrong_op()
                    break
            if not seq_status:
                break
        if seq_status:  # Last op
            seq = seq[-1]
            for filter in l_filters:
                if not filter.check_last(op):
                    filter.update_wrong_op()
                    seq_status = False

        # Apply the sequence filters
        for filter in l_seq_filters:
            if not seq_status and filter.check(seq):
                seq_status = False

        if seq_status:
            filtered_seq.append(seq)

    if show_logs:
        for filter in l_op_filters.extend(l_seq_filters):
            print("{:.1%} of the sketches were discarded by filter {}.".format(
                filter.wrong_op_cnt / len(data)), filter.__name__)
        print("{:.1%} of the sketches were discarded by all the filters.".format(
            (1 - len(filtered_seq)) / len(data)))
    return filtered_seq
