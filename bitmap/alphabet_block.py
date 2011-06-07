"""
Parametric Alphabet Block 
Tony Buser <tbuser@gmail.com>
http://tonybuser.com
http://creativecommons.org/licenses/by/3.0/
"""

from openscad import *
from bitmap import *

# change to any letter
letter = "A"

assemble(union([
	difference([
		cube(20),
		translate([2, 2, 17],
			cube([16, 16, 5])
		)
	]),
	translate([10, 10, 15],
		eight_bit_char(letter, 2, 5)
	)
]))
