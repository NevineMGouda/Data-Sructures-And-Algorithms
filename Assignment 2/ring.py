#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2: Ring Detection

Team Number: 60
Student Names: Mona Mohamed Elamin, Nevine Gouda
'''
try:
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False
import unittest
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


def ring_detection(g, n, visited, parent):
    """
    Sig: graph G(node, edge), int, int[0..j-1], int ==> boolean
    Pre: n is a non-negative node, and the Graph consists of non negative integers nodes.
    Post: returns True if ring is detected in the graph.
    Example:
        ring_detection(g1, 0, [], -1) ==> False
        ring_detection(g1, 5, [], 4) ==> True
    """
    visited[n] = True
    #Variant: i, visited
    #InVariant: g
    for i in g.adjacency_list()[n]:
        if not visited[i]:
            if ring_detection(g, i, visited, n):
                return True
        else:
            if i != parent:
                return True
    return False


def ring(G):
    """
    Sig: graph G(node, edge) ==> boolean
    Pre: The graph consists of non negative integer nodes.
    Post: returns True if ring is detected in the graph.
    Example: 
        ring(g1) ==> False
        ring(g2) ==> True
    """
    visited_nodes = [False for i in range(G.number_of_nodes())]
    # this if to insure that it goes for all nodes if the graph not connected
    # Variant: i, visited_nodes
    # InVariant: g
    for i in range(G.number_of_nodes()):
        if not visited_nodes[i]:
            if ring_detection(G, i, visited_nodes, -1):
                return True
    return False


def ring_detection_extended(g, n, visited, parent, node_parent, ring, found):
    """
    Sig: graph G(node, edge), int, int[0..n-1], int, [0..m-1], int[0..j-1], boolean ==> boolean, int[0..j-1]
    Pre: The graph consists of non negative integer nodes.
    Post: Returns True if ring is detected in the graph and a list that consists of the ring's node values.
          But returns False and an empty list if no ring exists in the input graph.
    Example:
        ring_detection_extended(g1, 2, [1], 1, [0, 1], [], False) ==> False, []
        ring_detection_extended(g1, 1, [1, 2, 4], 4, [0, 1, 2, 4], [], True) ==> True, [1, 2, 4, 1]
    """
    visited[n] = True
    if n != 0:
        node_parent[n] += node_parent[parent]
        node_parent[n].append(parent)
    # Variant: i, visited
    # InVariant: g
    for i in g.adjacency_list()[n]:
        if not visited[i]:
            isring, ring_list,found = ring_detection_extended(g, i, visited, n, node_parent, ring, found)
            if isring is True and found is False:
                ring = node_parent[i]
                ring.append(i)
                ring += ring_list
                found = True
                return True, ring, found
            elif isring is True and found is True:
                return True, ring_list, found
        else:
            if i != parent:
                ring.append(i)
                return True, ring, found
    if not found:
        return False, [], found


def ring_extended(G):
    """
    Sig: graph G(node, edge) ==> boolean, int[0..j-1]
    Pre: The graph consists of non negative integer nodes.
    Post: Returns True if ring is detected in the graph and a list that consists of the ring's node values.
          But returns False and an empty list if no ring exists in the input graph.
    Example: 
        ring(g1) ==> False, []
        ring(g2) ==>  True, [1, 2, 4, 1]
    """
    # Variant: i, len(visited_nodes)
    # InVariant: G
    visited_nodes = [False for i in range(G.number_of_nodes())]
    # Variant: i, len(node_parent)
    # InVariant: G
    node_parent = [[] for i in range(G.number_of_nodes())]
    # this is to insure that it goes for all nodes if the graph not connected
    # Variant: i
    # InVariant: G
    ring = []
    for i in range(G.number_of_nodes()):
        if not visited_nodes[i]:
            isring, ring, found = ring_detection_extended(G, i, visited_nodes, -1, node_parent, ring, False)
            if isring:
                x = ring[-1]
                index = 0
                for j in range(len(ring)-2, -1, -1):
                    if ring[j] == x:
                        index = j
                        break
                return True, ring[index:]
    return False, ring
    
    
def draw_graph(G, r):
    """Draw graph and the detected ring
    """
    if not HAVE_PLT:
        return
    pos = nx.spring_layout(G)
    plt.axis('off')
    nx.draw_networkx_nodes(G,pos)
    nx.draw_networkx_edges(G,pos,style='dotted') # graph edges drawn with dotted lines
    nx.draw_networkx_labels(G,pos)
    
    # add solid edges for the detected ring
    if len(r) > 0:
        T = nx.Graph()
        T.add_path(r)
        for (a,b) in T.edges():
            if G.has_edge(a,b):
                T.edge[a][b]['color']='g' # green edges appear in both ring and graph
            else:
                T.edge[a][b]['color']='r' # red edges are in the ring, but not in the graph
        nx.draw_networkx_edges(
            T,pos, 
            edge_color=[edata['color'] for (a,b,edata) in T.edges(data=True)], 
            width=4)
    plt.show()


class RingTest(unittest.TestCase):
    """Test Suite for ring detection problem
    
    Any method named "test_something" will be run when this file is 
    executed. Use the sanity check as a template for adding your own test 
    cases if you wish.
    (You may delete this class from your submitted solution.)
    """
    def is_ring(self, graph, path):
        """Asserts that the nodes in path from a ring in graph"""
        traversed = nx.Graph()
        for v in range(len(path) - 1):
            self.assertTrue(
                path[v + 1] in graph.neighbors(path[v]), 
                "({},{}) is not an edge in the graph\ngraph: {}".format(
                    path[v],
                    path[v+1],
                    graph.edges())
                    )
            self.assertFalse(
                traversed.has_edge(path[v],path[v+1]), 
                "duplicated edge: ({},{})".format(path[v],path[v+1]))
            traversed.add_edge(path[v],path[v+1])
        self.assertEqual(
            path[0], path[-1], 
            "start and end not equal: {} != {}".format(path[0],path[-1]))

    def test_sanity(self):
        """Sanity Test
        
        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """
        testgraph = nx.Graph([(0,1),(0,2),(0,3),(2,4),(2,5),(3,6),(3,7),(7,8)])
        self.assertFalse(ring(testgraph))
        testgraph.add_edge(6,8)
        self.assertTrue(ring(testgraph))
        
    def test_extended_sanity(self):
        """sanity test for returned ring"""
        testgraph = nx.Graph([(0,1),(0,2),(0,3),(2,4),(2,5),(3,6),(3,7),(7,8),(6,8)])
        found, thering = ring_extended(testgraph)
        self.assertTrue(found)
        self.is_ring(testgraph, thering)
        # Uncomment to visualize the graph and returned ring:
        draw_graph(testgraph,thering)
    def test_extended_sanity_2(self):
        """sanity test for returned ring"""
        G = nx.Graph()
        G.add_node(0)
        G.add_node(1)
        G.add_node(2)
        G.add_node(3)
        G.add_node(4)
        G.add_node(5)
        G.add_edge(0, 3)
        found, thering = ring_extended(G)
        self.assertFalse(found)
        # Uncomment to visualize the graph and returned ring:
        draw_graph(G,thering)

    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()
if __name__ == '__main__':
    unittest.main()