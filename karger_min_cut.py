"""
Karger's randomized minimum-cut algorithm.

This implementation uses an edge list. Parallel edges are kept as separate
entries, so each remaining edge has an equal chance of being selected.
Self-loops are removed after every contraction.
"""

import random
from typing import Iterable


def _is_connected(vertices: set[str], edges: list[tuple[str, str]]) -> bool:
    """Return True when the undirected graph is connected."""
    if not vertices:
        return False

    adjacency = {vertex: set() for vertex in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    start = next(iter(vertices))
    visited = {start}
    stack = [start]

    while stack:
        current = stack.pop()
        for neighbour in adjacency[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(neighbour)

    return visited == vertices


def karger_once(
    vertices: Iterable[str],
    input_edges: Iterable[tuple[str, str]],
    rng: random.Random | None = None,
) -> tuple[int, list[set[str]]]:
    """
    Run one trial of Karger's algorithm.

    Returns:
        A tuple containing the cut size and the two groups of original vertices.
    """
    rng = rng or random.Random()
    vertices = set(vertices)
    edges = list(input_edges)

    if len(vertices) < 2:
        raise ValueError("The graph must contain at least two vertices.")

    for u, v in edges:
        if u not in vertices or v not in vertices:
            raise ValueError(f"Edge {(u, v)} refers to an unknown vertex.")
        if u == v:
            raise ValueError("Input edges must not contain self-loops.")

    if not _is_connected(vertices, edges):
        raise ValueError("Karger's algorithm requires a connected graph.")

    # Each active key represents one current super-vertex.
    # Its set stores the original vertices merged into that super-vertex.
    groups = {i: {vertex} for i, vertex in enumerate(sorted(vertices))}
    vertex_id = {
        vertex: group_id
        for group_id, vertex in enumerate(sorted(vertices))
    }

    # Convert original edges to super-vertex IDs.
    contracted_edges = [
        (vertex_id[u], vertex_id[v]) for u, v in edges
    ]

    while len(groups) > 2:
        # Selecting from the edge list means every edge, including each
        # parallel edge, has the same probability of being selected.
        u, v = rng.choice(contracted_edges)

        # Merge v into u.
        groups[u].update(groups[v])
        del groups[v]

        # Replace v with u in every edge and remove resulting self-loops.
        updated_edges = []
        for a, b in contracted_edges:
            a = u if a == v else a
            b = u if b == v else b
            if a != b:
                updated_edges.append((a, b))

        # Keep parallel edges: do not convert this list into a set.
        contracted_edges = updated_edges

    cut_size = len(contracted_edges)
    partition = list(groups.values())
    return cut_size, partition


def karger_min_cut(
    vertices: Iterable[str],
    edges: Iterable[tuple[str, str]],
    trials: int = 100,
    seed: int | None = None,
) -> tuple[int, list[set[str]]]:
    """
    Run Karger's algorithm repeatedly and return the smallest cut found.

    A fixed seed makes the random experiment reproducible.
    """
    if trials < 1:
        raise ValueError("trials must be at least 1.")

    vertices = list(vertices)
    edges = list(edges)
    rng = random.Random(seed)

    best_cut = None
    best_partition = None

    for _ in range(trials):
        cut_size, partition = karger_once(vertices, edges, rng)
        if best_cut is None or cut_size < best_cut:
            best_cut = cut_size
            best_partition = partition

    return best_cut, best_partition


if __name__ == "__main__":
    # A four-vertex cycle. Its minimum cut has size 2.
    graph_vertices = ["A", "B", "C", "D"]
    graph_edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "A"),
    ]

    cut, groups = karger_min_cut(
        graph_vertices,
        graph_edges,
        trials=100,
        seed=42,
    )

    print(f"Smallest cut found: {cut}")
    print(f"Partition: {groups}")
