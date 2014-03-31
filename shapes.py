"""
  OpenSCAD Shapes Library (www.openscad.org)
  Copyright (C) 2009  Catarina Mota
  Copyright (C) 2010  Elmo Mäntynen

  License: LGPL 2.1 or later
"""

from openscad import *

# 2D Shapes
#ngon(sides, radius, center=False);

# 3D Shapes
#box(width, height, depth);
#roundedBox(width, height, depth, factor);
#cone(height, radius);
#ellipticalCylinder(width, height, depth);
#ellipsoid(width, height);
#tube(height, radius, wall, center = False);
#tube2(height, ID, OD, center = False);
#ovalTube(width, height, depth, wall, center = False);
#hexagon(height, depth);
#octagon(height, depth);
#dodecagon(height, depth);
#hexagram(height, depth);
#rightTriangle(adjacent, opposite, depth);
#equiTriangle(side, depth);
#twelvePtStar(height, depth);

#----------------------

# size is a vector [w, h, d]
def box(width, height, depth):
	return cube([width, height, depth], True)

# size is a vector [w, h, d]
def roundedBox(width, height, depth, radius):
	size=[width, height, depth]
	result = [
		cube(size - [2*radius,0,0], True),
		cube(size - [0,2*radius,0], True)
	]
	for x in [radius-size[0]/2, -radius+size[0]/2]:
		for y in [radius-size[1]/2, -radius+size[1]/2]:
			result.append(translate([x,y,0], cylinder(r=radius, h=size[2], center=True)))
	return union(result)

def cone(height, radius, center = False):
	return cylinder(height, radius, 0, center)

def ellipticalCylinder(w, h, height, center = False):
	return scale([1, h/w, 1], cylinder(h=height, r=w, center=center))

def ellipsoid(w, h, center = False):
	return scale([1, float(h)/w, 1], sphere(w/2))

# wall is wall thickness
def tube(height, radius, wall, center = False):
	return difference([
		cylinder(h=height, r=radius, center=center),
		cylinder(h=height, r=radius-wall, center=center)
	])

# wall is wall thickness
def tube2(height, ID, OD, center = False):
	return difference([
		cylinder(h=height, r=OD/2, center=center),
		cylinder(h=height, r=ID/2, center=center)
	])

# wall is wall thickness
def ovalTube(height, rx, ry, wall, center = False):
	return difference([
		scale([1, ry/rx, 1], cylinder(h=height, r=rx, center=center)),
		scale([(rx-wall)/rx, (ry-wall)/rx, 1], cylinder(h=height, r=rx, center=center))
	])

# The orientation might change with the implementation of circle...
def ngon(sides, radius, center=False):
	return rotate([0, 0, 360/sides/2], circle(r=radius, center=center).fn(sides))

# size is the XY plane size, height in Z
def hexagon(size, height):
	boxWidth = size/1.75
	return union([rotate([0, 0, r], cube([boxWidth, size, height], True)) for r in [-60, 0, 60]])

# size is the XY plane size, height in Z
def octagon(size, height):
	intersection([
		cube([size, size, height], True),
		rotate([0,0,45], cube([size, size, height], True))
	])

# size is the XY plane size, height in Z
def dodecagon(size, height):
	return intersection([
		hexagon(size, height),
		rotate([0,0,90], hexagon(size, height))
	])

# size is the XY plane size, height in Z
def hexagram(size, height):
	boxWidth=size/1.75;
	return union([intersection([
		rotate([0,0,60*v[0]], cube([size, boxWidth, height], True)),
		rotate([0,0,60*v[1]], cube([size, boxWidth, height], True))
	]) for v in [[0,1],[0,-1],[1,-1]]])

def rightTriangle(adjacent, opposite, height):
	return difference([
		translate([-adjacent/2,opposite/2,0], cube([adjacent, opposite, height], True)),
		translate([-adjacent,0,0],
			rotate([0,0,atan(opposite/adjacent)], dislocateBox(adjacent*2, opposite, height+2))
		)
	])

def equiTriangle(side, height):
	return difference([
		translate([-side/2,side/2,0], cube([side, side, height], True)),
		rotate([0,0,30], dislocateBox(side*2, side, height)),
		translate([-side,0,0],
			rotate([0,0,60], dislocateBox(side*2, side, height))
		)
	])

def twelvePtStar(size, height):
	starNum = 4
	starAngle = 360/starNum
	return union([rotate([0, 0, s*starAngle], cube([size, size, height], True)) for s in range(1, starNum)])

#-----------------------
#MOVES THE ROTATION AXIS OF A BOX FROM ITS CENTER TO THE BOTTOM LEFT CORNER
def dislocateBox(w, h, d):
	return translate([0,0,-d/2], cube([w,h,d]))

#-----------------------
# Tests
def test_ellipsoid():
	return ellipsoid(10, 5)

assemble(union([
	#test_ellipsoid(),
]))
