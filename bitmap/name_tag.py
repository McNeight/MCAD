"""
Parametric Name Tag 
Tony Buser <tbuser@gmail.com>
http://tonybuser.com
http://creativecommons.org/licenses/by/3.0/
"""

from openscad import *
from bitmap import *

# change word
word = "REPRAP"

# block size 1 will result in 8mm per letter
block_size = 2
# height is the Z height of each letter
height = 3
# Append a hole fo a keyring, necklace etc. ?
key_ring_hole = True

result = [
	translate([0,-block_size*8*len(word)/2+block_size*8/2,3],
		eight_bit_str(word, block_size, height)
	),
	translate([0,0,float(3)/2],
		color([0,0,1,1],
			cube([block_size * 8, block_size * 8 * len(word), 3], center = True)
		)
	)
]
if key_ring_hole:
	result.append(
		translate([0, block_size * 8 * (len(word)+1)/float(2), 3/float(2)],
			difference([
				cube([block_size * 8, block_size * 8 , 3], center = True),
				cube([block_size * 4, block_size * 4 , 5], center = True)
			])
		)
	)
assemble(union(result))
#assemble(sphere(10))
