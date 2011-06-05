"""
 Copyright 2010 D1plo1d

 This library is dual licensed under the GPL 3.0 and the GNU Lesser General Public License as per http://creativecommons.org/licenses/LGPL/2.1/ .
"""

from openscad import *
from mcadmath import *

# generates a motor mount for the specified nema standard #.
def stepper_motor_mount(nema_standard,slide_distance=0, mochup=True, tolerance=0):
	# dimensions from:
	# http://www.numberfactory.com/NEMA%20Motor%20Dimensions.htm
	if nema_standard == 17:
		return _stepper_motor_mount(
			motor_shaft_diameter = 0.1968*mm_per_inch,
			motor_shaft_length = 0.945*mm_per_inch,
			pilot_diameter = 0.866*mm_per_inch,
			pilot_length = 0.80*mm_per_inch,
			mounting_bolt_circle = 1.725*mm_per_inch,
			bolt_hole_size = 3.5,
			bolt_hole_distance = 1.220*mm_per_inch,
			slide_distance = slide_distance,
			mochup = mochup,
			tolerance=tolerance)
	if nema_standard == 23:
		return _stepper_motor_mount(
			motor_shaft_diameter = 0.250*mm_per_inch,
			motor_shaft_length = 0.81*mm_per_inch,
			pilot_diameter = 1.500*mm_per_inch,
			pilot_length = 0.062*mm_per_inch,
			mounting_bolt_circle = 2.625*mm_per_inch,
			bolt_hole_size = 0.195*mm_per_inch,
			bolt_hole_distance = 1.856*mm_per_inch,
			slide_distance = slide_distance,
			mochup = mochup,
			tolerance=tolerance)

# inner mehod for creating a stepper motor mount of any dimensions
def _stepper_motor_mount(
	motor_shaft_diameter,
	motor_shaft_length,
	pilot_diameter,
	pilot_length,
	mounting_bolt_circle,
	bolt_hole_size,
	bolt_hole_distance,
	slide_distance = 0,
	motor_length = 40, #arbitray - not standardized
	mochup = True,
	tolerance = 0):
	result = []

	# == centered mount points ==
	# mounting circle inset
	result += [
		translate([0,slide_distance/2,0], circle(pilot_diameter/2 + tolerance)),
		square([pilot_diameter,slide_distance], True),
		translate([0,-slide_distance/2,0], circle(pilot_diameter/2 + tolerance))
	]

	# todo: motor shaft hole
	
	# mounting screw holes
	for x in range(-1,2):
		for y in range(-1,2):
			result.append(translate([x*bolt_hole_distance/2,y*bolt_hole_distance/2,0], union([
				translate([0,slide_distance/2,0], circle(bolt_hole_size/2 + tolerance)),
				translate([0,-slide_distance/2,0], circle(bolt_hole_size/2 + tolerance)),
				square([bolt_hole_size+2*tolerance, slide_distance], True)
			])))

	# == motor mock-up ==
	# motor box
	if mochup == True:
		cyl = cylinder(h = 5, r = pilot_diameter/2)
		cub = cube([bolt_hole_distance+bolt_hole_size+5,bolt_hole_distance+bolt_hole_size+5,motor_length], center = True)
		shaft = cylinder(r=motor_shaft_diameter/2,h=motor_length+motor_shaft_length--1, center = True)
		shaft.background = cub.background = cyl.background = True
		
		result += [
			translate([0,0,-5], cyl),
			translate([0,0,-motor_length/2], cub),
			translate([0,0,-(motor_length-motor_shaft_length-2)/2], shaft)
		]
	
	return union(result)

def test_nema17():
	return stepper_motor_mount(17)

def test_nema23():
	return stepper_motor_mount(23)

assemble(union([
	#test_nema17(),
	#test_nema23()
]))
