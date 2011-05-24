# MIT license

import imp
imp.load_source("constantsscad", "constants.scad")
from constantsscad import *

deg = lambda angle: 360*angle/TAU

