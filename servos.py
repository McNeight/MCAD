"""
 Servo outline library

 Authors:
   - Eero 'rambo' af Heurlin 2010-

 License: LGPL 2.1
"""

from openscad import *
from triangles import *

"""
 Align DS420 digital servo

 @param vector position The position vector
 @param vector rotation The rotation vector
 @param boolean screws If defined then "screws" will be added and when the module is differenced() from something if will have holes for the screws
 @param number axle_lenght If defined this will draw "backgound" indicator for the main axle
"""
def alignds420(position=[0, 0, 0], rotation=[0, 0, 0], screws = False, axle_length = 0):
	result = []
	# Main axle
	mac1 = cylinder(r=6, h=8)
	mac1.fn = 30
	mac2 = cylinder(r=2.5, h=10.5)
	mac2.fn = 20
	result.append(translate([0,0,17], union([mac1, mac2])))

	# Box and ears
	result.append(translate([-6,-6,0], union([
		cube([12, 22.8,19.5], False),
		translate([0,-5, 17], cube([12, 7, 2.5])),
		translate([0, 20.8, 17], cube([12, 7, 2.5]))
	])))
	if screws:
		ct = cylinder(r=1.8/2, h=6)
		ct.fn = 6
		ct.highlight = True
		result += [
			translate([0,(-10.2 + 1.8),11.5], ct),
			translate([0,(21.0 - 1.8),11.5], ct)
		]

	# The large slope
	result.append(
		translate([-6,0,19],
			rotate([90,0,90], triangle(4, 18, 12))
		)
	)

	# Render a cube for simplicity instead of the small slope on a cube
	result.append(translate([-6,-6,19.0], cube([12,6.5,4])))

	if axle_length > 0:
		c = cylinder(r=0.9, h=axle_length, center=True)
		c.fn = 8
		c.background = True
		result.append(c)
	return translate(position, rotate(rotation, union(result)))

# Tests:
def test_alignds420():
	return alignds420(screws=True)

#assemble(test_alignds420())
