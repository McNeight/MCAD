"""
 A nema standard stepper motor module.
 
 Originally by Hans Häggström, 2010.
 Dual licenced under Creative Commons Attribution-Share Alike 3.0 and LGPL2 or later
"""

from openscad import *
from units import *
from materials import *
from numpy import interp

# Parameters: 
NemaModel = 0
NemaLengthShort = 1
NemaLengthMedium = 2
NemaLengthLong = 3
NemaSideSize = 4
NemaDistanceBetweenMountingHoles = 5
NemaMountingHoleDiameter = 6
NemaMountingHoleDepth = 7
NemaMountingHoleLip = 8
NemaMountingHoleCutoutRadius = 9
NemaEdgeRoundingRadius = 10
NemaRoundExtrusionDiameter = 11
NemaRoundExtrusionHeight = 12
NemaAxleDiameter = 13
NemaFrontAxleLength = 14
NemaBackAxleLength = 15
NemaAxleFlatDepth = 16
NemaAxleFlatLengthFront = 17
NemaAxleFlatLengthBack = 18

NemaParameters = range(0, 19)

NemaA = 1
NemaB = 2
NemaC = 3

NemaShort = NemaA
NemaMedium = NemaB
NemaLong = NemaC

# TODO: The small motors seem to be a bit too long, I picked the size specs from all over the place, is there some canonical reference?
Nema08 = [8, 33*mm, 43*mm, 43*mm, 20*mm, 15.4*mm, 2*mm, 1.75*mm, -1*mm, 0*mm, 2*mm, 16*mm, 1.5*mm, 4*mm, 13.5*mm, 9.9*mm, -1*mm, 0*mm, 0*mm]
Nema11 = [11, 32*mm, 40*mm, 52*mm, 28*mm, 23*mm, 2.5*mm, 2*mm, -1*mm, 0*mm, 2.5*mm, 22*mm, 1.8*mm, 5*mm, 13.7*mm, 10*mm, 0.5*mm, 10*mm, 9*mm]
Nema14 = [14, 26*mm, 28*mm, 34*mm, 35.3*mm, 26*mm, 3*mm, 3.5*mm, -1*mm, 0*mm, 5*mm, 22*mm, 1.9*mm, 5*mm, 18*mm, 10*mm, 0.5*mm, 15*mm, 9*mm]
Nema17 = [17, 33*mm, 39*mm, 47*mm, 42.20*mm, 31.04*mm, 4*mm, 4.5*mm, -1*mm, 0*mm, 7*mm, 22*mm, 1.9*mm, 5*mm, 18*mm, 15*mm, 0.5*mm, 15*mm, 14*mm]
Nema23 = [23, 39*mm, 54*mm, 76*mm, 56.4*mm, 47.14*mm, 4.75*mm, 5*mm, 4.95*mm, 9.5*mm, 2.5*mm, 38.10*mm, 1.52*mm, 6.36*mm, 18.80*mm, 15.60*mm, 0.5*mm, 16*mm, 14*mm]
Nema34 = [34, 66*mm, 96*mm, 126*mm, 85*mm, 69.58*mm, 6.5*mm, 5.5*mm, 5*mm, 17*mm, 3*mm, 73.03*mm, 1.9*mm, 0.5*inch, 37*mm, 34*mm, 1.20*mm, 25*mm, 25*mm]

motorWidth = lambda model: interp(NemaSideSize, NemaParameters, model)
motorLength = lambda model, size: interp(size, NemaParameters, model)

def motor(model=Nema23, size=NemaMedium, dualAxis=False, pos=[0,0,0], orientation = [0,0,0]):
	length = interp(size, NemaParameters, model)

	print "  Motor: Nema" + repr(interp(NemaModel, NemaParameters, model)) + ", length= " + repr(length) + "mm, dual axis=" + repr(dualAxis)

	stepperBlack = BlackPaint
	stepperAluminum = Aluminum

	side = interp(NemaSideSize, NemaParameters, model)

	cutR = interp(NemaMountingHoleCutoutRadius, NemaParameters, model)
	lip = interp(NemaMountingHoleLip, NemaParameters, model)
	holeDepth = interp(NemaMountingHoleDepth, NemaParameters, model)

	axleLengthFront = interp(NemaFrontAxleLength, NemaParameters, model)
	axleLengthBack = interp(NemaBackAxleLength, NemaParameters, model)
	axleRadius = interp(NemaAxleDiameter, NemaParameters, model) * 0.5

	extrSize = interp(NemaRoundExtrusionHeight, NemaParameters, model)
	extrRad = interp(NemaRoundExtrusionDiameter, NemaParameters, model) * 0.5

	holeDist = interp(NemaDistanceBetweenMountingHoles, NemaParameters, model) * 0.5
	holeRadius = interp(NemaMountingHoleDiameter, NemaParameters, model) * 0.5

	mid = side / 2

	roundR = interp(NemaEdgeRoundingRadius, NemaParameters, model)

	axleFlatDepth = interp(NemaAxleFlatDepth, NemaParameters, model)
	axleFlatLengthFront = interp(NemaAxleFlatLengthFront, NemaParameters, model)
	axleFlatLengthBack = interp(NemaAxleFlatLengthBack, NemaParameters, model)

	diff = [cube([side, side, length + extrSize])]

	# Corner cutouts
	if lip > 0:
		diff += [
			translate([0,    0,    lip], cylinder(h=length, r=cutR)),
			translate([side, 0,    lip], cylinder(h=length, r=cutR)),
			translate([0,    side, lip], cylinder(h=length, r=cutR)),
			translate([side, side, lip], cylinder(h=length, r=cutR))
		]
	# Rounded edges
	if roundR > 0:
		diff += [
			translate([mid+mid, mid+mid, length/2],
				rotate([0,0,45],
					cube([roundR, roundR*2, 4+length + extrSize+2], True)
				)
			),
			translate([mid-(mid), mid+(mid), length/2],
				rotate([0,0,45],
					cube([roundR*2, roundR, 4+length + extrSize+2], True)
				)
			),
			translate([mid+mid, mid-mid, length/2],
				rotate([0,0,45],
					cube([roundR*2, roundR, 4+length + extrSize+2], True)
				)
			),
			translate([mid-mid, mid-mid, length/2],
				rotate([0,0,45],
					cube([roundR, roundR*2, 4+length + extrSize+2], True)
				)
			)
		]
	
	# Bolt holes
	fs = openscad.fs
	openscad.fs = holeRadius/8
	diff.append(
		color(stepperAluminum, union([
			translate([mid+holeDist,mid+holeDist,-1*mm], cylinder(h=holeDepth+1*mm, r=holeRadius)),
			translate([mid-holeDist,mid+holeDist,-1*mm], cylinder(h=holeDepth+1*mm, r=holeRadius)),
			translate([mid+holeDist,mid-holeDist,-1*mm], cylinder(h=holeDepth+1*mm, r=holeRadius)),
			translate([mid-holeDist,mid-holeDist,-1*mm], cylinder(h=holeDepth+1*mm, r=holeRadius))
		]))
	)
	openscad.fs = fs

	# Grinded flat
	diff.append(color(stepperAluminum,
		difference([
			translate([-1*mm, -1*mm, -extrSize], 
				cube([side+2*mm, side+2*mm, extrSize + 1*mm])
			),
			translate([side/2, side/2, -extrSize - 1*mm], 
				cylinder(h=4*mm, r=extrRad)
			)
		])
	))
	
	diff2 = [cylinder(h=axleLengthFront + 1*mm , r=axleRadius).fs(axleRadius/10)]
	# Flat
	if axleFlatDepth > 0:
		diff2.append(translate([axleRadius-axleFlatDepth, -5*mm, -extrSize*mm-(axleLengthFront-axleFlatLengthFront)],
			cube([5*mm, 10*mm, axleLengthFront])
		))
	
	uni = [
		translate([-mid, -mid, 0], 
			difference(diff)
		),

		# Axle
		translate([0, 0, extrSize-axleLengthFront], color(stepperAluminum, difference(diff2))),
	]
	
	diff3 = [cylinder(h=axleLengthBack + 0*mm, r=axleRadius).fs(axleRadius/10)]
	# Flat
	if axleFlatDepth > 0:
		diff3.append(translate([axleRadius-axleFlatDepth, -5*mm, (axleLengthBack-axleFlatLengthBack)],
			cube([5*mm, 10*mm, axleLengthBack])
		))
	
	if dualAxis:
		uni += [
			translate([0, 0, length+extrSize], color(stepperAluminum, difference(diff3)))
		]

	return color(stepperBlack,
		translate(pos, rotate(orientation, union(uni)))
	)
	
def roundedBox(size, edgeRadius):
	return cube(size)

# Tests
def test_nema():
	result = []
	for size in [NemaShort, NemaMedium, NemaLong]:
		result += [
			translate([-100,size*100,0], motor(Nema34, size, dualAxis=True)),
			translate([0,size*100,0], motor(Nema23, size, dualAxis=True)),
			translate([100,size*100,0], motor(Nema17, size, dualAxis=True)),
			translate([200,size*100,0], motor(Nema14, size, dualAxis=True)),
			translate([300,size*100,0], motor(Nema11, size, dualAxis=True)),
			translate([400,size*100,0], motor(Nema08, size, dualAxis=True)),
		]
	return union(result)

assemble(union([
	#test_nema(),
]))