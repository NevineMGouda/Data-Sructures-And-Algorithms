#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3: Reliable Communications

Team Number: 60
Student Names: Mona Mohamed Elamin, Nevine Gouda
'''
import unittest
import sys
import math
import itertools
import heapq
import networkx as nx
"""IMPORTANT:
We're using networkx only to provide a reliable graph
object.  Your solution may NOT rely on the networkx implementation of
any graph algorithms.  You can use the node/edge creation functions to
create test data, and you can access node lists, edge lists, adjacency
lists, etc. DO NOT turn in a solution that uses a networkx
implementation of a graph traversal algorithm, as doing so will result
in a score of 0.
"""

try:
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False

class PriorityQueue:
    """Priority Queue

    An efficient priority queue implementation, as described in
    the heapq library of the python manual [1].

    [1]: http://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
    """
    def __init__(self):
        self.pqueue = []                  # list of entries arranged in a heap
        self.entry_finder = {}            # mapping of tasks to entries
        self.REMOVED = '<removed-task>'   # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pqueue, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pqueue:
            priority, count, task = heapq.heappop(self.pqueue)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

def minDistance(G, dist, visited):
    """
    Sig: graph G(V,E), dic, dic ==> vertex
    Pre: dist and visited consists of keys of vertices in G and distances are non-negatives values.
    Post: Returns the vertex with the minimum distance to reach it
    Example: Given the following edges: [('a', 'b', fp = 4), ('a', 'c', fp = 5.6), ('a', 'd', fp = 1)]
                                        => it will return 'd' since it has the lowest weight
    """
    # Initilaize minimum distance for next node
    min_distance = sys.maxint
    # Search not nearest vertex not in the
    # shortest path tree
    min_vertex = 0
    for v in G.nodes():
        # Variant: v
        # InVariant: dist, visited
        if (v in dist) and (dist[v] < min_distance) and visited[v] == False:
            min_distance = dist[v]
            min_vertex = v
    return min_vertex


def reliable(G, s, t):
    """
    Sig: graph G(V,E), vertex, vertex ==> vertex[0..k]
    Pre: The graph is an undirected connected graph, it doesn't contain self-loops and s is not the same as t.
    Post: Returns a path from s to t with the lowest failure probability
    Example: Test Case 1
    """
    assert(s in G.nodes() and t in G.nodes())
    path = []
    for u, v in G.edges():
        new_weight = -math.log(1-G[u][v]["fp"])
        G[u][v]["fp"] = new_weight
    dist = {}
    parent = {}
    visited = {}
    for node in G.nodes():
        # Variant: node, dist
        # InVariant: G
        if node == s:
            dist[node] = 0
        else:
            dist[node] = sys.maxint
        visited[node] = False

    for cout in range(len(G.nodes())):
        # Variant: cout, u, visited
        # InVariant: G
        u = minDistance(G, dist, visited)
        visited[u] = True
        for v in G.nodes():
            # Variant: v
            # InVariant: u, visited
            if v in G[u] and visited[v] is False and dist[v] > (dist[u] + G[u][v]["fp"]):
                dist[v] = dist[u] + G[u][v]["fp"]
                parent[v] = u
    i = t
    path.append(t)
    while i != s:
        # Variant: i, path
        # InVariant: parent
        path.append(parent[i])
        i = parent[i]
    return path[::-1]



class ReliableCommunicationsTest(unittest.TestCase):
    """Test suite for the reliable communications problem
    """
    def draw_mst(self, G, path, n):
        if not HAVE_PLT:
            return
        pos = nx.spring_layout(G) # positions for all nodes
        plt.subplot(120 + n)
        plt.title('Reliability %d' % n)
        plt.axis('off')
        # nodes
        nx.draw_networkx_nodes(G, pos, node_size = 700)
        # edges
        nx.draw_networkx_edges(G, pos, width = 6, alpha = 0.5,
                               edge_color = 'b', style = 'dashed')
        from itertools import izip
        l = [(a, b) for a, b in izip(path[0:-1], path[1:])]
        T = nx.Graph()
        T.add_edges_from(l)
        nx.draw_networkx_edges(T, pos, width = 6)
        # labels
        nx.draw_networkx_labels(G, pos, font_size = 20, font_family = 'sans-serif')
    def test_sanity1(self):
        G = nx.Graph()
        G.add_edge('a', 'b', fp = 0.6)
        G.add_edge('a', 'c', fp = 0.2)
        G.add_edge('c', 'd', fp = 0.1)
        G.add_edge('c', 'e', fp = 0.7)
        G.add_edge('c', 'f', fp = 0.9)
        G.add_edge('a', 'd', fp = 0.3)
        path = reliable(G, 'b', 'f')
        # 1-((1-0.6)*(1-0.2)*(1-0.9))
        self.assertEqual(path, ['b', 'a', 'c', 'f'], 'test 1 failed')
        self.draw_mst(G, path, 1)

    def test_sanity2(self):
        G = nx.Graph()
        G.add_edge('a', 'b', fp = 0.6)
        G.add_edge('a', 'c', fp = 0.9)
        G.add_edge('c', 'd', fp = 0.1)
        G.add_edge('c', 'e', fp = 0.7)
        G.add_edge('c', 'f', fp = 0.9)
        G.add_edge('a', 'd', fp = 0.3)
        path = reliable(G, 'b', 'f')

        self.assertEqual(path, ['b', 'a', 'd', 'c', 'f'], 'test 2 failed')
        self.draw_mst(G, path, 2)

    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show() # display

if __name__ == '__main__':
    unittest.main()
