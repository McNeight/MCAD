# -*- coding: utf-8 -*-
# From http://www.thingiverse.com/thing:3457
# © 2010 whosawhatsis 

"""
This script generates a teardrop shape at the appropriate angle to prevent overhangs greater than 45 degrees. The angle is in degrees, and is a rotation around the Y axis. You can then rotate around Z to point it in any direction. Rotation around Y or Z will cause the angle to be wrong.
"""

from openscad import *
from math import sin
from mcadmath import PI

def teardrop(radius, length, angle, fn=30):
	ofn = openscad.fn
	openscad.fn = fn
	result = rotate([0, angle, 0], union([
		linear_extrude(h = length, center = True, convexity = radius, twist = 0, child = \
			circle(radius)),
		linear_extrude(h = length, center = True, convexity = radius, twist = 0, child = \
			projection(cut_mode = False, child = \
				rotate([0, -angle, 0], translate([0, 0, radius * sin(PI/4) * 1.5], \
					cylinder(radius * sin(PI/4), radius * sin(PI/4), 0, center = True))))),
	]))
	openscad.fn = ofn
	return result


def test_teardrop():
	return union([
		translate([0, -15, 0], teardrop(5, 20, 90)),
		translate([0, 0, 0], teardrop(5, 20, 60)),
		translate([0, 15, 0], teardrop(5, 20, 45)),
	])


#openscad.result = test_teardrop()
