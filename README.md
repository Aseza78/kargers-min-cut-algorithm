# Karger's Minimum Cut Algorithm

## Project overview

This project demonstrates Karger's randomized edge-contraction algorithm for
the minimum-cut problem in a connected, undirected graph.

A **cut** divides the vertices of a graph into two non-empty groups. The cut
size is the number of edges crossing between those groups. A **minimum cut**
is a cut with the smallest possible number of crossing edges.

This project is based on a university Applications and Algorithms group
assignment. The repository presents the topic as a learning and programming
demonstration. Check the course rules and obtain permission before publishing
any material that belongs to the group or university.

## What the algorithm does

1. Start with a connected, undirected graph.
2. Choose one remaining edge uniformly at random.
3. Contract the chosen edge by merging its two endpoint vertices.
4. Remove self-loops created by the contraction.
5. Keep parallel edges, because each represents a separate original edge.
6. Continue until only two super-vertices remain.
7. The number of edges between those two super-vertices is the cut found in
   that run.
8. Repeat the process and keep the smallest cut found.

One run is not guaranteed to find the true minimum cut. Repeating the
algorithm increases the chance of finding it.

## Repository contents

```text
kargers-min-cut-algorithm/
├── README.md
├── requirements.txt
└── src/
    └── karger_min_cut.py
```

## Requirements

- Python 3.10 or later
- No third-party Python packages are required

## Run the example

From the repository folder, run:

```bash
python src/karger_min_cut.py
```

The included example is a four-vertex cycle. Its minimum cut size is 2.
The script runs 100 trials using a fixed random seed so that the example is
reproducible.

## Use the functions with your own graph

```python
from src.karger_min_cut import karger_min_cut

vertices = ["A", "B", "C", "D"]
edges = [
    ("A", "B"),
    ("B", "C"),
    ("C", "D"),
    ("D", "A"),
]

cut_size, partition = karger_min_cut(
    vertices,
    edges,
    trials=100,
    seed=42,
)

print(cut_size)
print(partition)
```

For a different graph, replace `vertices` and `edges` with the graph's
vertices and undirected edges. If the graph contains parallel edges, list each
parallel edge separately.

## Implementation notes

- The graph is represented as an edge list.
- Edge selection is performed from the current edge list, so each remaining
  edge occurrence has equal probability of being selected.
- Parallel edges are retained during contraction.
- Self-loops are removed after each contraction.
- A fixed seed can be supplied to make a run reproducible.
- The input graph must be connected and undirected.

## Limitations

- This is a straightforward educational implementation, not an optimised
  large-graph implementation.
- Randomised algorithms can return a cut larger than the true minimum cut in
  an individual run.
- Increasing the number of trials can improve the chance of finding a
  minimum cut, but also increases execution time.
- The example graph is a simple demonstration and is not the same as the
  five-vertex diagram in the original assignment.

## Academic context and acknowledgement

This work develops the Karger's Minimum Cut topic studied in the
Applications and Algorithms university assignment. The original assignment
was completed as group work. Add the names of group members and describe your
own contribution only if you have permission to publish those details.

## References

- Karger, D. R. (1993). *Global min-cuts in RNC, and other ramifications of a
  simple min-cut algorithm*. Proceedings of the 4th Annual ACM-SIAM Symposium
  on Discrete Algorithms, pp. 29–37.
- Karger, D. R. and Stein, C. (1996). *A new approach to the minimum cut
  problem*. Journal of the ACM, 43(4), pp. 601–640.
  https://doi.org/10.1145/234533.234534
- Stoer, M. and Wagner, F. (1997). *A simple min-cut algorithm*. Journal of
  the ACM, 44(4), pp. 585–591.
  https://doi.org/10.1145/263867.263872
