# -*- coding: utf-8 -*-

# Parametric curves, to be used as paths
# Licensed under the MIT license.
# © 2010 by Elmo Mäntynen

from constants import *
from mcadmath import *
from math import cos, sin

"""
A circular helix of radius a and pitch 2πb is described by the following parametrisation:
x(t) = a*cos(t),
y(t) = a*sin(t),
z(t) = b*t
"""

b = lambda pitch: pitch/(TAU)
t = lambda pitch, z: z/b(pitch)

helix_curve = lambda pitch, radius, z: \
    [radius*cos(deg(t(pitch, z))), radius*sin(deg(t(pitch, z))), z]

