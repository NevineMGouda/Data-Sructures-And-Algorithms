#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 1: Integer Sort

Team Number: 60
Student Names: Mona Mohamed Elamin, Nevine Gouda
'''
import unittest


def integer_sort(A, k):
    '''
    Sig: int array[1..n], int -> int array[1..n]
    Pre: A is a list of non-negative integers and each element in A is either less than or equal k
    Post: a non-decreasingly sorted version of array A
    Example: integer_sort([5, 3, 6, 7, 12, 3, 6, 1, 4, 7]), 12) =
                 [1, 3, 3, 4, 5, 6, 6, 7, 7, 12]
    '''
    try:
        Y = [0] * (k+1)
        for i in range(len(A)):
            #Variant: i
            #InVariant: elements of A never change.
            x = A[i]
            if x < 0:
                print "ValueError: Please enter a list of non-negative integers"
                return A
            Y[x] += 1
        j = 0
        for x in range(len(Y)):
            #Variant: x
            #InVariant: elements of Y never change.
            t = Y[x]
            if t == 0:
                continue
                
            for i in range(j,j+t):
                #Variant: i
                #InVariant: A[0..i-1] elements of A previously calculated never change.
                A[i] = x
            j += t
        return A
    except IndexError:
        print "IndexError: Insert a list of values less than or equal k"
        return A

class IntegerSortTest(unittest.TestCase):
    """Test Suite for integer sort problem
    
    Any method named "test_something" will be run when this file is 
    executed. Use the sanity check as a template for adding your own 
    tests if you wish. 
    (You may delete this class from your submitted solution.)
    """
    
    def test_sanity(self):
        """Sanity Test
        
        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """
        A = [5, 3, 6, 7, 12, 3, 6, 1, 4, 7]
        R = integer_sort(A, 12)
        self.assertEqual(R, [1, 3, 3, 4, 5, 6, 6, 7, 7, 12])

if __name__ == '__main__':
    unittest.main()
