# -*- coding: utf-8 -*-

# Parametric screw-like things (ball screws, augers)
# License: GNU LGPL 2.1 or later.
# © 2010 by Elmo Mäntynen

from curves import *

"""
common screw parameters
length
pitch = length/rotations: the distance between the turns of the thread
outside_diameter
inner_diameter: thickness of the shaft
"""

from openscad import *

def helix(pitch, length, obj, slices=500):
    rotations = length/pitch
    return linear_extrude(h=length, twist=360*rotations, convexity=10, slices=slices, center=False, child=obj)

def auger(pitch, length):
    return union([
        helix(pitch, length, polygon([[10,10],[100,1],[100,-1],[10,-10]], [[0,1,2,3]])),
        cylinder(length, 20)
    ])
 
def test_auger():
    return translate([300, 0, 0], auger(100, 300))
 
def ball_groove(pitch, length, diameter, ball_radius=10):
    return union([
        helix(pitch, length, translate([diameter, 0, 0], circle(ball_radius)), slices=100)
    ])
 
def test_ball_groove():
    return translate([0, 300, 0], ball_groove(100, 300, 10))
 
def ball_groove2(pitch, length, diameter, ball_radius, slices=200):
    rotations = length/pitch
    radius=diameter/2
    offset = length/slices;
    result = []
    for i in range(0, slices):
        z = i*offset
        result += [
            translate(helix_curve(pitch, radius, z), 
                sphere(ball_radius))
        ]
    return union(result)

def test_ball_groove2():
    return translate([0, 0, 0], ball_groove2(100, 300, 100, 10))

# Uncomment to see examples
assemble(union([
#	test_auger(),
#	test_ball_groove(),
#	test_ball_groove2()
]))