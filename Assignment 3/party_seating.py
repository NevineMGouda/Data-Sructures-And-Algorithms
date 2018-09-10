#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3: Party seating problem

Team Number: 60
Student Names: Mona Mohamed Elamin, Nevine Gouda
'''
import unittest

# If your solution needs a queue, you can use this one:
from collections import deque
from decorator import append

def party(known):
    """
    Sig:    int[1..m, 1..n] ==> boolean, int[1..j], int[1..k]
    Pre:    known is a duplicate-free list
    Post:   If the input can be split into Two lists with no neighbours in the same list
            then it will return True and the two non-empty lists
            Otherwise it will return False and 2 empty lists
    Ex:     [[1,2],[0],[0]] ==> True, [0], [1,2]
    """
    table0 = []
    table1 = []
    assigned_table = [-1]*len(known)
    
    
    for n in range(len(known)):
        # Variant: n
        # InVariant: len(known)
        if assigned_table[n] == -1:
            nodes = []
            nodes.append(n)
            assigned_table[n] = 1
            while nodes:
                # Variant: nodes
                # InVariant: assigned_table
                g1 = nodes.pop()
                
                for g2 in known[g1]:
                    # Variant: g2,
                    # InVariant: assigned_table
                    if assigned_table[g2] == -1:
                        assigned_table[g2] = 1-assigned_table[g1]
                        nodes.append(g2)
                    
                    elif assigned_table[g2] == assigned_table[g1]:
                        return False, [], []
                    
    for i in range(len(assigned_table)):
        # Variant: i
        # InVariant: assigned_table
        if assigned_table[i] == 0:
            table0.append(i)
        elif assigned_table[i] == 1:
            table1.append(i)
       
    return True, table0, table1


class PartySeatingTest(unittest.TestCase):
    """Test suite for party seating problem
    """

    def test_sanity(self):
        """Sanity test

        A minimal test case.
        """
        K = [[1,2],[0],[0]]
        #K = [[], [], [4], [9, 4], [2, 3], [17], [], [14], [14], [3], [], [], [], [16], [8, 17, 7], [], [13], [5, 14], []]
        (found, A, B) = party(K)
        self.assertEqual(
            len(A) + len(B),
            len(K),
            "wrong number of guests: {!s} guests, tables hold {!s} and {!s}".format(
                len(K),
                len(A),
                len(B)
                )
            )
        for g in range(len(K)):
            self.assertTrue(
                g in A or g in B,
                "Guest {!s} not seated anywhere".format(g))
        for a1 in A:
            for a2 in A:
                self.assertFalse(
                    a2 in K[a1],
                    "Guests {!s} and {!s} seated together, and know each other".format(
                        a1,
                        a2
                        )
                    )
        for b1 in B:
            for b2 in B:
                self.assertFalse(
                    b2 in K[b1],
                    "Guests {!s} and {!s} seated together, and know each other".format(
                        b1,
                        b2
                        )
                    )

if __name__ == '__main__':
    unittest.main()
