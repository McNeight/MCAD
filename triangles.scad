"""
Simple triangles library

Authors:
   - Eero 'rambo' af Heurlin 2010-

License: LGPL 2.1
"""

from openscad import *
from math import sqrt, pow, tan

"""
Standard right-angled triangle

@param number o_len Lenght of the opposite side
@param number a_len Lenght of the adjacent side
@param number depth How wide/deep the triangle is in the 3rd dimension
@todo a better way ?
"""
def triangle(o_len, a_len, depth):
    return linear_extrude(h=depth,
        child=polygon([[0,0],[a_len,0],[0,o_len]], [[0,1,2]])
    )

"""
Standard right-angled triangle (tangent version)

@param number angle of adjacent to hypotenuse (ie tangent)
@param number a_len Lenght of the adjacent side
@param number depth How wide/deep the triangle is in the 3rd dimension
"""
def a_triangle(tan_angle, a_len, depth):
    return linear_extrude(h=depth,
        child=polygon([[0,0],[a_len,0],[0,tan(tan_angle) * a_len]], [[0,1,2]])
    )

# Tests:
def test_triangle():
    return triangle(5, 5, 5)

def test_a_triangle():
    return a_triangle(45, 5, 5)

def test_triangles():
    result = []
    # Generate a bunch of triangles by sizes
    for i in range(1, 11):
        result += [translate([i*7, -30, i*7],
            triangle(i*5, sqrt(i*5+pow(i,2)), 5)
        )]

    # Generate a bunch of triangles by angle
    for i in range(1, 90/5):
        result += [translate([i*7, 20, i*7],
            a_triangle(i*5, 10, 5)
        )]
    return union(result)

#openscad.result = test_triangles()