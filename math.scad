# MIT license

import imp
imp.load_source("constants.scad", "constants.scad")
from constants.scad import *

deg = lambda angle: 360*angle/TAU

