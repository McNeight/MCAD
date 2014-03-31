# Library: boxes.scad
# Version: 1.0
# Author: Marius Kintel
# Copyright: 2010
# License: BSD

from openscad import *
from numpy import array

# roundedBox([width, height, depth], float radius, bool sidesonly)

# size is a list [w, h, d]
def roundedBox(size, radius, sidesonly):
  rot = [[0,0,0], [90,0,90], [90,90,0]]
  result = []
  if sidesonly:
    result += [
      cube((array(size) - array([2*radius,0,0])).tolist(), True),
      cube((array(size) - array([0,2*radius,0])).tolist(), True)
    ]
    for x, y in [(x, y) \
      for x in [radius-size[0]/2, -radius+size[0]/2] \
      for y in [radius-size[1]/2, -radius+size[1]/2]]:
      result += [
        translate([x,y,0], cylinder(float(size[2]), radius, radius, True))
      ]
  else:
    result += [
      cube([float(size[0]), size[1]-radius*2, size[2]-radius*2], True),
      cube([size[0]-radius*2, float(size[1]), size[2]-radius*2], True),
      cube([size[0]-radius*2, size[1]-radius*2, float(size[2])], True)
    ]

    for axis in range(0,3):
      for x, y in [(x, y) \
        for x in [radius-size[axis]/2, -radius+size[axis]/2] \
        for y in [radius-size[(axis+1)%3]/2, -radius+size[(axis+1)%3]/2]]:
        result += [
          rotate(
            rot[axis], translate(
              [x,y,0],
              cylinder(float(size[(axis+2)%3]-2*radius), radius, radius, True)
            )
          )
        ]
    for x, y, z in [(x, y, z) \
      for x in [radius-size[0]/2, -radius+size[0]/2] \
      for y in [radius-size[1]/2, -radius+size[1]/2] \
      for z in [radius-size[2]/2, -radius+size[2]/2]]:
      result += [translate([x,y,z], sphere(radius))]
  return union(result)

def test_roundedBox():
  return roundedBox(array([20, 30, 40]), float(5), False)

# EXAMPLE USAGE:
#assemble(test_roundedBox())