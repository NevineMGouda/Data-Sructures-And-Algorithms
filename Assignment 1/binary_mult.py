#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 1: Binary Multiplication

Team Number: 60
Student Names: Mona Mohamed Elamin, Nevine Gouda
'''
import unittest


def shiftR(A, n):
    """
    Sig:     int[0..n-1], int n==> int[0..t+n-1]
    Pre:     n is a non negative integer
    Post:    returns the lists A with n zeros added on the left side
    Example: shiftR([1,0,1],2) = [0, 0, 1, 0, 1]
    """
    if len(A) == 0:
        return []
    ret = [0] * n
    return ret + A


def shiftL(A, n):
    """
    Sig:     int[0..n-1], int n==> int[0..t+n-1]
    Pre:     n is a non negative integer
    Post:    returns the lists A with n zeros added on the right side
    Example: shiftL([1,0,1],2) = [1, 0, 1, 0 ,0]
    """
    if len(A) == 0:
        return []
    ret = [0] * n
    return A + ret


def pad(A, B):
    """
    Sig:     int[0..n-1], int[0..m-1] ==> int[0..t-1]
    Pre:     A and B are two lists of non equal sized lists
    Post:    returns the lists A and B of the same size t
    Example: pad([1,0,1],[1,0]) = [1,0,1],[0,1,0]
             pad([0,1],[0,1,0]) = [0,0,1],[0,1,0]
    """
    # Padding if one number is shorter/longer than the other
    rA = A[::]
    rB = B[::]
    if len(A) > len(B):
        rB = shiftR(B, len(A) - len(B))
    if len(B) > len(A):
        rA = shiftR(A, len(B) - len(A))

    return rA, rB


def binary_add(A, B):
    """
    Sig:     int[0..n-1] int[0..n-1] ==> int[0..n-1]
    Pre:     A and B are two lists of same size n
    Post:    returns the addition of A and B of size n where n is the size of the input lists
    Example: binary_add([1,0,1],[0,1,0]) = [1, 1, 1]
    """
    if len(A) != len(B):
        A, B = pad(A, B)
    if sum(A) == 0:
        return B
    elif sum(B) == 0:
        return A
    ret = []
    carry = 0
    for i in range(len(A) - 1, -1, -1):
        #Variant: i
        #Invariant: A, B, ret[0..i-1] 
        if A[i] + B[i] + carry == 2:
            carry = 1
            ret.append(0)
        elif A[i] + B[i] + carry == 3:
            carry = 1
            ret.append(1)
        else:
            ret.append(A[i] + B[i] + carry)
            carry = 0

    if carry:
        ret.append(1)
    return ret[::-1]


def binary_mult(A, B):
    """
    Sig:     int[0..n-1], int[0..n-1] ==> int[0..2*n-1]
    Pre:     A and B are two lists of same size n
    Post:    returns a list of size 2n where n is the size of the input lists
    Var:     length(A) and length(B)
    Example: binary_mult([0,1,1],[1,0,0]) = [0,0,1,1,0,0]
    """

    # Padding if one number is shorter/longer than the other
    try:
        if len(A) == 0 or len(B) == 0:
            return []
        if len(A) != len(B):
            A, B = pad(A, B)

        # The base case
        if len(A) == 1:
            return [A[0] * B[0]]

        n = len(A)
        if n % 2:
            # Padding so that we can split number in two equal halves
            A = shiftR(A, 1)
            B = shiftR(B, 1)
            n += 1

        # Splitting the lists into 2 halves each
        Ah = A[0:n / 2]
        Al = A[n / 2:]
        Bh = B[0:n / 2]
        Bl = B[n / 2:]

        #Rercursive calls (Divide Stage)
        a = binary_mult(Ah, Bh)
        b = binary_mult(Ah, Bl)
        c = binary_mult(Al, Bh)
        d = binary_mult(Al, Bl)
        b = binary_add(b, c)
        a = shiftL(a, n)
        b = shiftL(b, n / 2)

        # Add the results upwards (Conquer Stage)
        temp = binary_add(a, b)
        ans = binary_add(temp, d)
        return shiftR(ans, (2 * n) - len(ans))[-2 * n:]
    except:
        print "An Error Occured, please check your input values"


class BinaryMultTest(unittest.TestCase):
    """Test Suite for binary multiplication problem

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
        A = [0, 1, 1, 0]
        B = [0, 0, 1, 0]
        answer = binary_mult(A, B)
        self.assertEqual(answer, [0, 0, 0, 0, 1, 1, 0, 0])

if __name__ == '__main__':
    unittest.main()
