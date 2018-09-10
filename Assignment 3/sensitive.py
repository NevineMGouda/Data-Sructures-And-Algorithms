#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3: Controlling Maximum Flow

Team Number: 60
Student Names: Mona Mohamed Elamin, Nevine Gouda
'''

import unittest
import networkx as nx
# API for networkx flow algorithms changed in v1.9:
if (list(map(lambda x: int(x), nx.__version__.split("."))) < [1, 9]):
    max_flow = nx.ford_fulkerson
else:
    max_flow = nx.maximum_flow
"""
We use max_flow() to generate flows for the included tests,
and you may of course use it as well in any tests you generate.
As always, your implementation of the senstive() function may NOT make use
of max_flow(), or any of the other graph algorithm implementations
provided by networkx.
"""

# If your solution needs a queue (like the BFS algorithm), you can use this one:
from collections import deque

try:
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False

"""
F is represented in python as a dictionary of dictionaries;
i.e., given two nodes u and v,
the computed flow from u to v is given by F[u][v].
"""


def BFS_reachable(G_f, source, destination, V):
    """
    Sig:   graph G(V,E), vertex, vertex, int ==> bool
    Pre:   the source and destination exist in G_f.
    Post:  Using BFS it returns True if the destination is reachable from the source in the given graph G_f, else returns False
    Ex:    sensitive(G,0,5,F) ==> (1, 3)
    """
    visited = [False] * V
    queue = [source]
    visited[source] = True
    while queue:
        # Variant: queue, visited
        # InVariant: G_f
        n = queue.pop(0)
        # then return true
        if n == destination:
            return True
        # Else, continue to do BFS
        for i in G_f[n]:
            # Variant: i
            # InVariant: G_f
            if visited[i] is False and G_f[n][i] != 0:
                queue.append(i)
                visited[i] = True
    return False


def sensitive(G, s, t, F):
    """
    Sig:   graph G(V,E), vertex, vertex, vertex[0..|V|-1, 0..|V|-1] ==> vertex, vertex
    Pre:   The graph is a directed graph and the capacities in the graph are non-negative.
    Post:  Returns an edge in the format of (u, v) if the edge between u, v is a sensitive edge. And will return None, None if it doesn't exist
    Ex:    sensitive(G,0,5,F) ==> (1, 3)
    """
    # G_f is the residual flow
    G_f = {}
    for node_i in F:
        # Variant: node_i, G_f
        # InVariant: F
        for node_j in F[node_i]:
            # Variant: node_j, G_f
            # InVariant: F, G
            flow = F[node_i][node_j]
            cap = G[node_i][node_j]["capacity"]
            residual = cap - flow
            if node_j not in G_f:
                G_f[node_j] = {}
            if node_i not in G_f:
                G_f[node_i] = {}
            G_f[node_j][node_i] = flow
            G_f[node_i][node_j] = residual

    S = []
    for i in G_f.keys():
        # Variant: i, S
        # InVariant: G_f
        if i == s:
            S.append(i)
            continue
        is_reachable = BFS_reachable(G_f=G_f, source=s, destination=i, V=len(G.nodes()))
        if is_reachable:
            S.append(i)

    S = set(S)
    T = set(G.nodes()) - S
    for u in S:
        # Variant: u, S, T
        # InVariant: G, F
        for v in T:
            # Variant: v, S, T
            # InVariant: G, F
            if (u, v) in G.edges():
                if F[u][v] != G[u][v]["capacity"]:
                    T.remove(v)
                    S.add(v)
            if (v, u) in G.edges():
                if F[v][u] != 0:
                    T.remove(v)
                    S.add(v)
    for u in S:
        # Variant: u
        # InVariant: S, T
        for v in T:
            # Variant: v
            # InVariant: S, T
            if (u, v) in G.edges():
                return u, v

    return None, None


class SensitiveSanityCheck(unittest.TestCase):
    """
    Test suite for the sensitive edge problem
    """
    def draw_graph(self, H, u, v, flow1, F1, flow2, F2):
        if not HAVE_PLT:
            return
        pos = nx.spring_layout(self.G)
        plt.subplot(1,2,1)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G,pos)
        nx.draw_networkx_edges(self.G,pos)
        nx.draw_networkx_labels(self.G,pos)
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={(u,v):'{}/{}'.format(
                  F1[u][v],
                  self.G[u][v]['capacity']
                ) for (u,v,data) in nx.to_edgelist(self.G)})
        plt.title('before: flow={}'.format(flow1))
        plt.subplot(1,2,2)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G,pos)
        nx.draw_networkx_edges(self.G,pos)
        nx.draw_networkx_edges(
            self.G, pos,
            edgelist=[(u,v)],
            width=3.0,
            edge_color='b')
        nx.draw_networkx_labels(self.G,pos)
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={(u,v):'{}/{}'.format(
                  F2[u][v],H[u][v]['capacity']
                ) for (u,v,data) in nx.to_edgelist(self.G)})
        plt.title('after: flow={}'.format(flow2))

    def setUp(self):
        """start every test with an empty directed graph"""
        self.G = nx.DiGraph()

    def run_test(self, s, t, draw=True):
        """standard tests to run for all cases

        Uses networkx to generate a maximal flow
        """
        H = self.G.copy()
        # compute max flow
        flow_g, F_g = max_flow(self.G, s, t)
        # find a sensitive edge
        u,v = sensitive(self.G, s, t, F_g)
        # is u a node in G?
        self.assertIn(u, self.G, "Invalid edge ({}, {})".format(u ,v))
        # is (u,v) an edge in G?
        self.assertIn(v, self.G[u], "Invalid edge ({}, {})".format(u ,v))
        # decrease capacity of (u,v) by 1
        H[u][v]["capacity"] = H[u][v]["capacity"] - 1
        # recompute max flow
        flow_h, F_h = max_flow(H, s, t)
        if draw:
            self.draw_graph(H, u, v, flow_g, F_g, flow_h, F_h)
        # is the new max flow lower than the old max flow?
        self.assertLess(
            flow_h,
            flow_g,
            "Returned non-sensitive edge ({},{})".format(u,v))

    def test_sanity(self):
        """Sanity check"""
        # The attribute on each edge MUST be called "capacity"
        # (otherwise the max flow algorithm in run_test will fail).
        self.G.add_edge(0, 1, capacity = 16)
        self.G.add_edge(0, 2, capacity = 13)
        self.G.add_edge(2, 1, capacity = 4)
        self.G.add_edge(1, 3, capacity = 12)
        self.G.add_edge(3, 2, capacity = 9)
        self.G.add_edge(2, 4, capacity = 14)
        self.G.add_edge(4, 3, capacity = 7)
        self.G.add_edge(3, 5, capacity = 20)
        self.G.add_edge(4, 5, capacity = 4)
        self.run_test(0, 5, draw=False)

    def test_sanity(self):
        self.G.add_edge(0, 2, capacity=49)
        self.G.add_edge(0, 3, capacity=41)
        self.G.add_edge(0, 5, capacity=92)
        self.G.add_edge(0, 6, capacity=10)
        self.G.add_edge(1, 0, capacity=75)
        self.G.add_edge(2, 1, capacity=20)
        self.G.add_edge(2, 5, capacity=68)
        self.G.add_edge(2, 6, capacity=26)
        self.G.add_edge(4, 0, capacity=2)
        self.G.add_edge(4, 5, capacity=54)
        self.G.add_edge(4, 6, capacity=166)
        self.G.add_edge(5, 1, capacity=102)
        self.G.add_edge(5, 6, capacity=33)
        self.G.add_edge(6, 1, capacity=30)

        self.run_test(4, 3, draw=False)
    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()

if __name__ == "__main__":
    unittest.main()
