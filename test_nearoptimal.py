# -*- coding: utf-8 -*-

"""

    >>> import scipy as sp
    >>> import numpy as np
    >>> import nearoptimal
    >>> from math import sqrt
    >>> from testfunc import epsilonCheck

Internal Tests:
====================

Let's make a hypercube for 2 dimensions.

    >>> dim = 2

To make some nice sidelengths, we cheat on omega

    >>> omega = 5 / sqrt(sqrt(dim))

    >>> m = nearoptimal.MultiDimHash(dim=dim, omega=omega, prob=0.8)

    >>> m.radius
    1.189207115002721
    >>> m.radiusSquared
    1.414213562373095

This gives us hypercube sidelength of

    >>> SIDELENGTH = sqrt(sqrt(2)) * omega
    >>> epsilonCheck(SIDELENGTH - 5)
    True

Define some points to work with

    >>> a = np.array([0, 0])
    >>> m._findHypercube(a)
    (array([0, 0]), array([0., 0.]))

    >>> b = np.array([0.14 + 3 * SIDELENGTH, .5])
    >>> m._findHypercube(b)
    (array([3, 0]), array([0.14, 0.5 ]))

    >>> c = np.array([.5, 42 * SIDELENGTH + 0.1])
    >>> m._findHypercube(c)
    (array([ 0, 42]), array([0.5, 0.1]))

    >>> d = np.array([-1 * SIDELENGTH + 0.1, 2 * SIDELENGTH + 0.1])
    >>> m._findHypercube(d)
    (array([-1,  2]), array([0.1, 0.1]))

Overwrite the balls of the hash to make test the ball intersection function

    >>> m.gridBalls = np.array([[.3, .3], [ 3., 3.]])

Tests for points within the hypercube [0, 1)^n

    >>> u, v = np.array([.29, .31]), np.array([2.9, 2.71])

We discard the first result, since it might trigger a compilation and thus
output some noise.

    >>> _ = m._findLocalBall(u)
    ...

    >>> m._findLocalBall(u)
    0

    >>> m._findLocalBall(v)
    1

Point outside of the hypercube don't return a result

    >>> m._findLocalBall(np.array([20, 0]))     # Returns None

As do points that are in not within any ball

    >>> m._findLocalBall(np.array([5.4, .9]))

Testing the composition of _findLocalBall and _findHypercube

    >>> m.findBall(u + np.array([2 * SIDELENGTH, 4 * SIDELENGTH]))
    ((2, 4), 0)

    >>> m.findBall(u + np.array([-2 * SIDELENGTH, 4 * SIDELENGTH]))
    ((-2, 4), 0)

    >>> m.findBall(u + np.array([-2 * SIDELENGTH, -4 * SIDELENGTH]))
    ((-2, -4), 0)

    >>> m.findBall(u + np.array([2 * SIDELENGTH, -4 * SIDELENGTH]))
    ((2, -4), 0)

    >>> m.findBall(v + np.array([2 * SIDELENGTH, 4 * SIDELENGTH]))
    ((2, 4), 1)

    >>> m.findBall(v + np.array([-2 * SIDELENGTH, 4 * SIDELENGTH]))
    ((-2, 4), 1)

    >>> m.findBall(v + np.array([-2 * SIDELENGTH, -4 * SIDELENGTH]))
    ((-2, -4), 1)

    >>> m.findBall(v + np.array([2 * SIDELENGTH, -4 * SIDELENGTH]))
    ((2, -4), 1)


Example Usage:
====================

    >>> m = nearoptimal.MultiDimHash(dim=2)
    >>> m.insert(np.array([0.9585762, 1.15822724]), 'red')
    >>> m.insert(np.array([1.02331605,  0.95385982]), 'red')
    >>> m.insert(np.array([0.80838576, 1.07507294]), 'red')
    >>> m.knn(np.array([0.9585762, 1.15822724]), 1)
    [(array([0.9585762 , 1.15822724]), 'red')]


"""
