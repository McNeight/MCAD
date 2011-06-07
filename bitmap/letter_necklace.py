"""
Parametric letters for for a necklace
Elmo Mäntynen <elmo.mantynen@iki.fi>
LGPL 2.1
"""

from bitmap import *

# change word, \n indicates a line break
word = "RepRaps\nForever"

# block size 1 will result in 8mm per letter
block_size = 2
# height is the Z height of each letter
height = 3

# Hole for the necklace
hole_diameter = 5

def letter(char, block_size, height, hole_diameter):
	return union([
		translate([0,0, hole_diameter*1.3],
			eight_bit_char(char, block_size, height)
		),
		translate([0,0,(hole_diameter*1.3)/2],
			color([0,0,1,1],
				difference([
					cube([block_size * 8, block_size * 8, hole_diameter+2], center = True),
					rotate([90, 0, 0], cylinder(h = block_size * 8 + 1, r = hole_diameter/2, center = True))
				])
			)
		)
	])

result = []
column = 0
rowreset = 0
for i in range(0, len(word)):
	if word[i] == '\n':
		column = column + 1
		rowreset = i+1
	else:
		result.append(translate([column*(block_size*1.1)*8, (i-rowreset)*(block_size*1.1)*8, 0],
			letter(word[i], block_size, height, hole_diameter)
		))
assemble(union(result))
