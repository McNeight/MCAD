# -*- coding: utf-8 -*-
"""
 Bearing model.

 Originally by Hans Häggström, 2010.
 Dual licenced under Creative Commons Attribution-Share Alike 3.0 and LGPL2 or later
"""

from openscad import *
from units import *
from materials import *

BEARING_INNER_DIAMETER = 0
BEARING_OUTER_DIAMETER = 1
BEARING_WIDTH = 2

# Common bearing names
SkateBearing = 608

# Bearing dimensions
# [inner dia, outer dia, width] if model == XXX else \
bearingDimensions = lambda model: \
  [8*mm, 22*mm, 7*mm] if model == 608 else \
  [3*mm, 10*mm, 4*mm] if model == 623 else \
  [4*mm, 13*mm, 5*mm] if model == 624 else \
  [7*mm, 22*mm, 7*mm] if model == 627 else \
  [8*mm, 16*mm, 4*mm] if model == 688 else \
  [9*mm, 19*mm, 6*mm] if model == 698 else \
  [8*mm, 22*mm, 7*mm] # this is the default


bearingWidth = lambda model: bearingDimensions(model)[BEARING_WIDTH]
bearingInnerDiameter = lambda model: bearingDimensions(model)[BEARING_INNER_DIAMETER]
bearingOuterDiameter = lambda model: bearingDimensions(model)[BEARING_OUTER_DIAMETER]

def bearing(pos=[0,0,0], angle=[0,0,0], model=SkateBearing,
	outline=False, material=Steel, sideMaterial=Brass):
	# Common bearing names
	model = 608 if model == "Skate" else model

	w = bearingWidth(model)
	innerD = bearingInnerDiameter(model) if outline==False else 0
	outerD = bearingOuterDiameter(model)

	innerRim = innerD + (outerD - innerD) * 0.2
	outerRim = outerD - (outerD - innerD) * 0.2
	midSink = w * 0.1

	rings = [
		# Basic ring
		Ring([0,0,0], outerD, innerD, w, material, material)
	]
	if outline==False:
		# Side shields
		rings += [
			Ring([0,0,-epsilon], outerRim, innerRim,
				epsilon+midSink, sideMaterial, material),
			Ring([0,0,w-midSink], outerRim, innerRim,
				epsilon+midSink, sideMaterial, material),
		]
	return translate(pos, rotate(angle, 
		union([color(material, difference(rings))])
	))

def Ring(pos, od, id, h, material, holeMaterial):
	ofs = openscad.fs
	openscad.fs = 0.01
	result = color(material,
		translate(pos,
			difference([
				cylinder(h, od/2),
				color(holeMaterial,
					translate([0,0,-10*epsilon],
						cylinder(h+20*epsilon, id/2)
					)
				),
			])
		)
	)
	openscad.fs = ofs
	return result

def test_bearing():
	return union([
		bearing(),
		bearing(pos=[5*cm,0,0], angle=[90,0,0]),
		bearing(pos=[-2.5*cm,0,0], model=688),
	])

def test_bearing_hole():
	return difference([
		translate([0, 0, 3.5], cube([30, 30, 7-10*epsilon], center=True)),
		bearing(outline=True),
	])

# Example, uncomment to view
#openscad.result = test_bearing()
#openscad.result = test_bearing_hole()