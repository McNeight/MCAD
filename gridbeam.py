"""
  OpenSCAD GridBeam Library (www.openscad.org)
  Copyright (C) 2009 Timothy Schmidt

  License: LGPL 2.1 or later

 zBeam(segments) - create a vertical gridbeam strut 'segments' long
 xBeam(segments) - create a horizontal gridbeam strut along the X axis
 yBeam(segments) - create a horizontal gridbeam strut along the Y axis
 topShelf(width, depth, corners) - create a shelf suitable for use in gridbeam structures width and depth in 'segments', corners == True notches corners
 bottomShelf(width, depth, corners) - like topShelf, but aligns shelf to underside of beams
 backBoard(width, height, corners) - create a backing board suitable for use in gridbeam structures width and height in 'segments', corners == True notches corners
 frontBoard(width, height, corners) - like backBoard, but aligns board to front side of beams
 translateBeam([x, y, z]) - translate gridbeam struts or shelves in X, Y, or Z axes in units 'segments'
"""

from openscad import *
from units import *

beam_width = inch * 1.5
beam_hole_radius = inch * 5/16
beam_is_hollow = True
beam_wall_thickness = inch * 1/8
beam_shelf_thickness = inch * 1/4
True
def zBeam(segments):
	diff = [cube([beam_width, beam_width, beam_width * segments])]
	for i in range(0, segments):
		diff += [
			translate([beam_width / 2, beam_width + 1, beam_width * i + beam_width / 2],
				rotate([90,0,0], cylinder(r=beam_hole_radius, h=beam_width + 2))
			),
			translate([-1, beam_width / 2, beam_width * i + beam_width / 2],
				rotate([0,90,0], cylinder(r=beam_hole_radius, h=beam_width + 2))
			)
		]

	if beam_is_hollow:
		diff.append(translate([beam_wall_thickness, beam_wall_thickness, -1],
			cube([beam_width - beam_wall_thickness * 2, beam_width - beam_wall_thickness * 2, beam_width * segments + 2])
		))
	return difference(diff)


def xBeam(segments):
	return translate([0,0,beam_width], rotate([0,90,0], zBeam(segments)))

def yBeam(segments):
	return translate([0,0,beam_width], rotate([-90,0,0], zBeam(segments)))

class translateBeam:
	def __init__(self, v):
		self.v = v
	def __enter__(self):
		return self
	# let any exception propogate
	def __exit__(self, type, value, traceback):
		return False
	def trans(self, child):
		return translate([x*beam_width for x in self.v], child)

def topShelf(width, depth, corners):
	diff = [cube([width * beam_width, depth * beam_width, beam_shelf_thickness])]

	if corners:
		diff += [
			translate([-1,  -1,  -1],
				cube([beam_width + 2, beam_width + 2, beam_shelf_thickness + 2])
			),
			translate([-1, (depth - 1) * beam_width, -1],
				cube([beam_width + 2, beam_width + 2, beam_shelf_thickness + 2])
			),
			translate([(width - 1) * beam_width, -1, -1],
				cube([beam_width + 2, beam_width + 2, beam_shelf_thickness + 2])
			),
			translate([(width - 1) * beam_width, (depth - 1) * beam_width, -1],
				cube([beam_width + 2, beam_width + 2, beam_shelf_thickness + 2])
			)
		]

	return difference(diff)


def bottomShelf(width, depth, corners):
	return translate([0,0,-beam_shelf_thickness],
		topShelf(width, depth, corners)
	)


def backBoard(width, height, corners):
	diff = [cube([beam_shelf_thickness, width * beam_width, height * beam_width])]

	if  corners:
		diff += [
			translate([-1,  -1,  -1],
				cube([beam_shelf_thickness + 2, beam_width + 2, beam_width + 2])
			),
			translate([-1, -1, (height - 1) * beam_width],
				cube([beam_shelf_thickness + 2, beam_width + 2, beam_width + 2])
			),
			translate([-1, (width - 1) * beam_width, -1],
				cube([beam_shelf_thickness + 2, beam_width + 2, beam_width + 2])
			),
			translate([-1, (width - 1) * beam_width, (height - 1) * beam_width],
				cube([beam_shelf_thickness + 2, beam_width + 2, beam_width + 2])
			)
		]

	return translate([beam_width, 0, 0], difference(diff))

def frontBoard(width, height, corners):
	return translate([-beam_width - beam_shelf_thickness, 0, 0],
		backBoard(width, height, corners)
	)

def test_xBeam():
	return xBeam(5)

def test_yBeam():
	return yBeam(5)

def test_zBeam():
	return zBeam(5)

def test_translateBeam():
	result = []
	with translateBeam([0, 0, 0]) as beam:
		result += [
			beam.trans(xBeam(5)),
			beam.trans(yBeam(5)),
			beam.trans(zBeam(5))
		]
	with translateBeam([1, 1, 1]) as beam:
		result += [
			beam.trans(xBeam(5)),
			beam.trans(yBeam(5)),
			beam.trans(zBeam(5))
		]
	return union(result)

def test_topShelf():
	return topShelf(30, 5, True)

def test_bottomShelf():
	return bottomShelf(20, 5, True)

def test_backBoard():
	return backBoard(30, 5, True)

def test_frontBoard():
	return frontBoard(20, 5, True)

assemble(union([
	#test_zBeam(),
	#test_xBeam(),
	#test_yBeam(),
	#test_translateBeam(),
	#test_topShelf(),
	#test_bottomShelf(),
	#test_backBoard(),
	#test_frontBoard(),
]))
