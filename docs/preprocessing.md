# Preprocessing

## Filter
### Coarse filter
Sketches are filtered out according to:
- their primitives and their constraints. Sketches containing the less common ones are rejected. Sketches containing constraints with three references (mirror, a few midpoints) are rejected;
- the number of primitives;
- the number of remaining degrees of freedom.

### Normalization
We modify the numerical parameters of the primitives and the constraints according to:
- lines have six parameters. We reduce them to five zeroing the start parameter;
- sketches are centered using a proxy for the barycenter;
- numerical values are converted to numbers. Some sketches are not well formated, they are discarded;
- lengths and positions are sent to $\[-1,1\]$ applying one homothety per sketch; angles to $\[0,2\pi\]$. So each parameter is either a boolean or a numerical value which lies in these intervals.

### Weighting
Similar sketches are underweighted:
- classes are formed looking at sketches with identical sequences of operations and references;
- among each class sketches are clustered according to their numerical parameters;
- one sketch per cluster is kept; its weight is the inverse of the number of clusters among the class. So, the distribution of classes is uniform.

We underweight repeated sketches by an additional factor one over the number of slices, if the job is done paralelly on different slices. Indeed, common sketches are still over-represented since they appear in each slice; while unique sketches appear in only one slice. If a sketch appears two times or more in one slice, then surely it is present in all the other slices.

## Encoding
Sketches are converted toward the input format of the neural network. In particular there are:
- `*_features`: the types of the primitives/constraints;
- `sparse_*_features`: the discretizations of the parameters;
- `incidences`: the sparse adjacency matrix of the graph;
- `i_edges_given`: indices of the constraints that are given to the neural network; the indices refer to the list `edge_ops` or samely to `incidences`;
- `i_edges_possible`: indices of the constraints that can be given to the neural network;
- `edges_toInf_neg`: couples of nodes that are not neighboor.

