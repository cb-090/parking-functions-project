from dataclasses import dataclass, field
from itertools import product, permutations

@dataclass(eq=True, frozen=True)
class Vertex:
    id: int
    label: str = ""

@dataclass(eq=True, frozen=True)
class Edge:
    u: Vertex
    v: Vertex

    def __post_init__(self):
        if self.u == self.v:
            raise ValueError("No self-loops allowed in simple graph")

    def endpoints(self):
        return (self.u, self.v)

class Graph:
    def __init__(self):
        self.vertices = set()
        self.adj = dict()  # Vertex -> set of neighbors

    def add_vertex(self, v: Vertex):
        if v not in self.vertices:
            self.vertices.add(v)
            self.adj[v] = set()

    def add_edge(self, u: Vertex, v: Vertex):
        if u == v:
            raise ValueError("No self-loops allowed")

        self.add_vertex(u)
        self.add_vertex(v)

        self.adj[u].add(v)
        self.adj[v].add(u)

    def neighbors(self, v: Vertex):
        return sorted(list(self.adj.get(v, list())))

    def edges(self):
        seen = set()
        edge_list = []
        for u in self.vertices:
            for v in self.adj[u]:
                if (v, u) not in seen:
                    edge_list.append(Edge(u, v))
                    seen.add((u, v))
        return edge_list
    
    def is_parking_function(self, sequence):
        n = len(self.vertices)
        parking_spots = ["-"] * n  # index = vertex-1

        # Step 2: place first car
        parking_spots[sequence[0] - 1] = sequence[0]

        for i in range(1, n):
            v = sequence[i]  # 1-based

            while parking_spots[v - 1] != "-":
                if v == n:
                    return False

                # neighbors strictly greater than v
                neighbors = [u for u in self.neighbors(v) if u > v]

                if not neighbors:
                    return False  # no valid move

                # split into empty and all
                empty_neighbors = [u for u in neighbors if parking_spots[u - 1] == "-"]

                if empty_neighbors:
                    v = max(empty_neighbors)  # largest unoccupied neighbor > v
                else:
                    v = min(neighbors)  # smallest neighbor > v

            parking_spots[v - 1] = sequence[i]

        return True
    
    def is_classical_parking_function(self, sequence):
        n = len(sequence)

        # Optional sanity check (since classical definition assumes values in 1..n)
        if any(x < 1 or x > n for x in sequence):
            return False

        seq = sorted(sequence)

        for i, val in enumerate(seq, start=1):  # i = 1..n
            if val > i:
                return False

        return True
    
def is_weakly_increasing(seq):
    return all(seq[i] <= seq[i+1] for i in range(len(seq) - 1))

def is_weakly_decreasing(seq):
    return all(seq[i] >= seq[i+1] for i in range(len(seq) - 1))
    
if __name__ == "__main__":
    g = Graph()
    # sequence = [2, 2, 2]

    for i in range(1, 8):
        g.add_vertex(i)
        if i != 8:
            g.add_edge(i, i+1)
            g.add_edge(i, 8)

    print("Vertices:", g.vertices)
    print("Edges:", g.edges())
    # print(f"Is {sequence} a parking function:", g.is_parking_function(sequence))
    parking_funcs = []
    sequences = list(product(range(1, 9), repeat=8))
    classical_not_parking_funcs = []
    weakly_inc_parking_funcs = []
    weakly_dec_parking_funcs = []

    for perm in sequences:
        if g.is_parking_function(perm):
            parking_funcs.append(perm)
            # print(f"Parking function found: {perm}")
            if is_weakly_increasing(perm):
                weakly_inc_parking_funcs.append(perm)
            if is_weakly_decreasing(perm):
                weakly_dec_parking_funcs.append(perm)
        elif g.is_classical_parking_function(perm):
            classical_not_parking_funcs.append(perm)

    print(f"Total permutations checked: {len(sequences)}")
    print(f"Total parking functions: {len(parking_funcs)}")
    print(f"Classical parking functions that are not parking functions: {len(classical_not_parking_funcs)}")
    # print(classical_not_parking_funcs)
    print(f"Weakly increasing parking functions: {len(weakly_inc_parking_funcs)}")  
    print(f"Weakly decreasing parking functions: {len(weakly_dec_parking_funcs)}")