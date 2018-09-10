#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2: Search String Replacement

Team Number: 60
Student Names: Mona Mohamed Elamin, Nevine Gouda
'''
import unittest
# Sample matrix provided by us:
from string import ascii_lowercase


# Solution to part b:
def min_difference(u, r, R):
    """
    Sig:    string, string, int[0..|A|, 0..|A|] ==> int
    Pre:     Both strings should only be lowercased alphabetical letters, from a to z.
    Post:    Returns the number of differences between both strings
    Example: Let R be the resemblance matrix where every change and skip costs 1
             min_difference("dinamck","dynamic",R) ==> 3
    """
    # To get the resemblance between two letters, use code like this:
    # difference = R['a']['b']
    u = u.lower()
    r = r.lower()
    # Variant: i, j
    # InVariant: len(r), len(u)
    D = [[0 for i in range(len(r) + 1)] for j in range(len(u) + 1)]
    D[0][0] = R['-']['-']
    
    # Variant: i, D[i][0]
    # InVariant: len(u), D[i-1][1:]
    #initialize the base cases for the first column
    for i in range(1,len(u)+1):
        D[i][0] = D[i-1][0]+R[u[i-1]]['-']

    # Variant: j, D[0][j]
    # InVariant: len(r)
    #initialize the base cases for the first raw    
    for j in range(1, len(r)+1):
        D[0][j] = D[0][j-1] +  R['-'][r[j-1]]

    # Variant: i
    # InVariant: len(u)
    for i in range(1, len(u)+1):

        # Variant: j
        # InVariant: len(r), D[i][j]
        for j in range(1, len(r)+1):
            D[i][j] = min((D[i-1][j] + R[u[i-1]]['-']), (D[i][j-1]+ R['-'][r[j-1]] ), (D[i-1][j-1] + R[u[i-1]][r[j-1]]))

    return D[len(u)][len(r)]


# Solution to part c:
def min_difference_align(u, r, R):
    """
    Sig:     string, string, int[0..|A|, 0..|A|] ==> int, string, string
    Pre:     Both strings should only be lowercased alphabetical letters, from a to z.
    Post:    Returns the number of differences between both strings and the alginment for both strings, with "-" for each difference.
    Example: Let R be the resemblance matrix where every change and skip costs 1
             min_difference_align("dinamck","dynamic",R) ==>
                                    3, "dinam-ck", "dynamic-"
    """
    u = u.lower()
    r = r.lower()
    # Variant: i, j
    # InVariant: len(r), len(u)
    D = [[0 for i in range(len(r) + 1)] for j in range(len(u) + 1)]
    D[0][0] = R['-']['-']
    
    # Variant: i, D[i][0]
    # InVariant: len(u), D[i-1][1:]
    # initialize the base cases for the first column
    for i in range(1, len(u)+1):
        D[i][0] = D[i-1][0] + R[u[i-1]]['-']

    # Variant: j, D[0][j]
    # InVariant: len(u), D[1:][j-1]
    # initialize the base cases for the first row
    for j in range(1, len(r)+1):
        D[0][j] = D[0][j-1] + R['-'][r[j-1]]

    # Variant: i
    # InVariant: len(u)
    for i in range(1, len(u)+1):
        # Variant: j,  D[i][j]
        # InVariant: len(r)
        for j in range(1, len(r)+1):
            D[i][j] = min((D[i-1][j] + R[u[i-1]]['-']), (D[i][j-1]+ R['-'][r[j-1]] ), (D[i-1][j-1] + R[u[i-1]][r[j-1]]))
    
    diff = D[len(u)][len(r)]
    u_new = u
    r_new = r
    i = len(u)
    j = len(r)
    while i != 0 or j != 0:
        if i>0 and j> 0 and D[i-1][j-1] + R[u[i-1]][r[j-1]] == D[i][j]:
            i = i-1
            j = j-1
        elif i>0 and D[i-1][j]+R[u[i-1]]['-'] == D[i][j]:
            r_new = r_new[:j] + "-" + r_new[j:]
            i= i-1
        elif j>0 and D[i][j-1]+R['-'][r[j-1]] == D[i][j]:
            u_new = u_new[:i]+"-"+u_new[i:]
            j = j-1
    return diff, u_new, r_new


def qwerty_distance():
    """Generates a QWERTY Manhattan distance resemblance matrix

    Costs for letter pairs are based on the Manhattan distance of the
    corresponding keys on a standard QWERTY keyboard.
    Costs for skipping a character depends on its placement on the keyboard:
    adding a character has a higher cost for keys on the outer edges,
    deleting a character has a higher cost for keys near the middle.

    Usage:
        R = qwerty_distance()
        R['a']['b']  # result: 5
    """
    from collections import defaultdict
    import math
    R = defaultdict(dict)
    R['-']['-'] = 0
    zones = ["dfghjk", "ertyuislcvbnm", "qwazxpo"]
    keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for num, content in enumerate(zones):
        for char in content:
            R['-'][char] = num + 1
            R[char]['-'] = 3 - num
    for a in ascii_lowercase:
        rowA = None
        posA = None
        for num, content in enumerate(keyboard):
            if a in content:
                rowA = num
                posA = content.index(a)
        for b in ascii_lowercase:
            for rowB, contentB in enumerate(keyboard):
                if b in contentB:
                    R[a][b] = math.fabs(rowB - rowA) + math.fabs(posA - contentB.index(b))
    return R

class MinDifferenceTest(unittest.TestCase):
    """Test Suite for search string replacement problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own test
    cases if you wish.
    (You may delete this class from your submitted solution.)
    """

    def test_diff_sanity(self):
        """Difference sanity test

        Given a simple resemblance matrix, test that the reported
        difference is the expected minimum. Do NOT assume we will always
        use this resemblance matrix when testing!
        """
        alphabet = ascii_lowercase + '-'
        # The simplest (reasonable) resemblance matrix:
        R = dict( [ (
                     a,
                     dict([(b, (0 if a == b else 1)) for b in alphabet])) for a in alphabet])
        # Warning: we may (read: 'will') use another matrix!
        self.assertEqual(min_difference("dinamck", "dynamic", R), 3)


    def test_align_sanity(self):
        """Simple alignment

        Passes if the returned alignment matches the expected one.
        """
        # QWERTY resemblance matrix:
        R = qwerty_distance()
        diff, u, r = min_difference_align("polynomial", "exponential", R)
        #diff, u, r = min_difference_align("dinamck", "dynamic", R)
        # Warning: we may (read: 'will') use another matrix!
        self.assertEqual(diff, 15)
        # Warning: there may be other optimal matchings!
        self.assertEqual(u, '--polyn-om-ial')
        self.assertEqual(r, 'exp-o-ne-ntial')

if __name__ == '__main__':
    unittest.main()
