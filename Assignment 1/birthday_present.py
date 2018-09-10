#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 1: Birthday Present

Team Number: 60
Student Names: Mona Mohamed Elamin, Nevine Gouda
'''
import unittest


def birthday_present(P, n, t):
    '''
    Sig: int[0..n-1], int, int --> Boolean
    Pre: P is a list of non-negative integers and t >= 0
    Post: True if and only if a subset exists with summation equals t
    Example: P = [2, 32, 234, 35, 12332, 1, 7, 56]
             birthday_present(P, len(P), 299) = True
             birthday_present(P, len(P), 11) = False
    '''
    # Initialize the dynamic programming matrix, A
    # Type: Boolean[0..n][0..t]
    try:
        #Variant: i, j
        #Invariant: A[i-1][j-1] the previous calculated element in never change
        A = [[None for i in range(t + 1)] for j in range(n + 1)]
 
        for j in range(1, (t + 1)):
            #Variant: j
            #Invariant: A[1..n-1][0..t-1] all elements in A not row 0, never change
            A[0][j] = False

        for i in range(0, (n + 1)):
            #Variant: i
            #Invariant: A[0..n-1][1..t-1] all elements in A not column 0, never change.
            A[i][0] = True

        for i in range(1, (n + 1)):
            #Variant: i
            #Invariant: none
            for j in range(1, (t + 1)):
                #Variant: j
                #Invariant: A[0..i-1][0..j-1] all element in A previously calculated never change.
                if P[i - 1] > j:
                    A[i][j] = A[i - 1][j]
                else:
                    A[i][j] = A[i - 1][j - P[i - 1]] or A[i - 1][j]

        return A[n][t]
    except IndexError:
        print "IndexError: Insert a list of positive integers only"
        return False


def birthday_present_subset(P, n, t):
    '''
    Sig: int[0..n-1], int, int --> int[0..m]
    Pre: P is a list of non-negative integers and t >= 0
    Post: list of a subset with a summation equals t and is empty if no subset exists
    Example: P = [2, 32, 234, 35, 12332, 1, 7, 56]
             birthday_present_subset(P, len(P), 299) = [56, 7, 234, 2]
             birthday_present_subset(P, len(P), 11) = []
    '''
    try:
        A = [[None for i in range(t + 1)] for j in range(n + 1)]
        P_subset = []
        count = t
        for j in range(1, (t + 1)):
            #Variant: j
            #Invariant: A[1..n-1][0..t-1] all elements in A not in row 0, never change.
            A[0][j] = False

        for i in range(0, (n + 1)):
            #Variant: i
            #Invariant: A[0..n-1][1..t-1] all elements in A not column 0, never change.
            A[i][0] = True

        for i in range(1, (n + 1)):
            #Variant: i
            #Invariant: none
            for j in range(1, (t + 1)):
                #Variant: j
                #Invariant: A[0..i-1][0..j-1] all elements in A previously calculated never change.
                if P[i - 1] > j:
                    A[i][j] = A[i - 1][j]
                else:
                    A[i][j] = A[i - 1][j - P[i - 1]] or A[i - 1][j]

        if A[n][t] is True:
            i = n
            j = t
            while count != 0:
                #Variant: i
                #Invariant: P_subset previously appended elements never change.
                if i < 0:
                    break
                if A[i][j] is True and A[i - 1][j] is False:
                    P_subset.append(P[i - 1])
                    count = count - P[i - 1]
                    j = j - P[i - 1]
                    i = i - 1
                else:
                    i = i - 1
        return P_subset
    except IndexError:
        print "IndexError: Insert a list of positive integers only"
        return []


class BirthdayPresentTest(unittest.TestCase):
    """Test Suite for birthday present problem
    
    Any method named "test_something" will be run when this file is 
    executed. Use the sanity check as a template for adding your own 
    tests if you wish. 
    (You may delete this class from your submitted solution.)
    """

    def test_sat_sanity(self):
        """Sanity Test for birthday_present()
        
        This is a simple sanity check;
        passing is not a guarantee of correctness.
        """
        P = [2, 32, 234, 35, 12332, 1, 7, 56]
        n = len(P)
        t = 11
        self.assertFalse(birthday_present(P, n, t))

    def test_sol_sanity(self):
        """Sanity Test for birthday_present_subset()
        
        This is a simple sanity check;
        passing is not a guarantee of correctness.
        """
        P = [2, 32, 234, 35, 12332, 1, 7, 56]
        n = len(P)
        t = 299
        self.assertTrue(birthday_present(P, n, t))
        self.assertItemsEqual(birthday_present_subset(P, n, t), [56, 7, 234, 2])

        
if __name__ == '__main__':
 unittest.main()
