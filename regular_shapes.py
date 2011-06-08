"""
  OpenSCAD Shapes Library (www.openscad.org)
  Copyright (C) 2010-2011  Giles Bathgate

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License,
  LGPL version 2.1, or (at your option) any later version of the GPL.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""

from openscad import *
from math import sqrt, pow

# 2D regular shapes

def triangle(radius):
	o=radius/2		# equivalent to radius*sin(30)
	a=radius*sqrt(3)/2	# equivalent to radius*cos(30)
	polygon(points=[[-a, -o], [0, radius], [a, -o]], paths=[[0, 1, 2]])

def reg_polygon(sides, radius):
	dia = lambda r: sqrt(pow(r*2, 2)/2) # sqrt(r*2^2/2) if only we had an exponention op
	if sides<2:
		return square([radius, 0])
	if sides==3:
		return triangle(radius)
	if sides==4:
		return square([dia(radius), dia(radius)], center=True)
	if sides>4:
		return circle(radius).fn(sides)

def pentagon(radius):
	return reg_polygon(5, radius)

def hexagon(radius):
	return reg_polygon(6, radius)

def heptagon(radius):
	return reg_polygon(7, radius)

def octagon(radius):
	return reg_polygon(8, radius)

def nonagon(radius):
	return reg_polygon(9, radius)

def decagon(radius):
	return reg_polygon(10, radius)

def hendecagon(radius):
	return reg_polygon(11, radius)

def dodecagon(radius):
	return reg_polygon(12, radius)

def ellipse(width, height):
	return scale([1, height/width, 1], circle(width/2))

def egg_outline(width, length):
	return union([
		difference([
			ellipse(width, 2*length-width),
			translate([-length/2, 0, 0], square(length))
		]),
		circle(width/2)
	])

# 3D regular shapes

def cone(height, radius, center=False):
	return cylinder(height, radius, 0, center)

def oval_prism(height, rx, ry, center=False):
	return scale([1, rx/ry, 1], cylinder(h=height, r=ry, center=center))

def oval_tube(height, rx, ry, wall, center=False):
	return difference([
		scale([1, ry/rx, 1], cylinder(h=height, r=rx, center=center)),
		translate([0,0,-height/2], scale([(rx-wall)/rx, (ry-wall)/rx, 2], cylinder(h=height, r=rx, center=center)))
	])

# Tubifies any regular prism
def tubify(radius, wall, child):
	return difference([
		child,
		translate([0, 0, -0.1],
			scale([(radius-wall)/radius, (radius-wall)/radius, 2], child)
		)
	])

def cylinder_tube(height, radius, wall, center=False):
	return tubify(radius, wall, cylinder(h=height, r=radius, center=center))

def triangle_prism(height, radius):
	return linear_extrude(h=height, child=triangle(radius))

def triangle_tube(height, radius, wall):
	return tubify(radius, wall, triangle_prism(height, radius))

def pentagon_prism(height, radius):
	return linear_extrude(h=height, child=pentagon(radius))

def pentagon_tube(height, radius, wall):
	return tubify(radius, wall, pentagon_prism(height,radius))

def hexagon_prism(height, radius):
	return linear_extrude(h=height, child=hexagon(radius))

def heptagon_prism(height, radius):
	return linear_extrude(h=height, child=heptagon(radius))

def octagon_prism(height, radius):
	return linear_extrude(h=height, child=octagon(radius))

def nonagon_prism(height, radius):
	return linear_extrude(h=height, child=nonagon(radius))

def decagon_prism(height, radius):
	return linear_extrude(h=height, child=decagon(radius))

def hendecagon_prism(height, radius):
	return linear_extrude(h=height, child=hendecagon(radius))

def dodecagon_prism(height, radius):
	return linear_extrude(h=height, child=dodecagon(radius))

def torus(outerRadius, innerRadius):
	r=(outerRadius-innerRadius)/2
	return rotate_extrude(child=translate([innerRadius+r,0,0], circle(r)))

def triangle_pyramid(radius):
	o=radius/2		# equivalent to radius*sin(30)
	a=radius*sqrt(3)/2	# equivalent to radius*cos(30)
	return polyhedron([[-a, -o, -o], [a, -o, -o], [0, radius, -o], [0, 0, radius]],
		[[0, 1, 2], [1, 2, 3], [0, 1, 3], [0, 2, 3]])

def square_pyramid(base_x, base_y, height):
	w=base_x/2
	h=base_y/2
	return polyhedron([[-w, -h, 0], [-w, h, 0], [w, h, 0], [w, -h, 0], [0, 0, height]],
		[[0, 3, 2, 1], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]])

# Tests:
def test_square_pyramid():
	return square_pyramid(10, 20, 30)

assemble(union([
	#test_square_pyramid()
]))
