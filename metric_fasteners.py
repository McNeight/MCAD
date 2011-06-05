"""
  OpenSCAD Metric Fastners Library (www.openscad.org)
  Copyright (C) 2010-2011  Giles Bathgate

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License,
  LGPL version 2.1, or (at your option) any later version of the GPL.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Pblic License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

from openscad import *

openscad.fn=50
apply_chamfer=True

def cap_bolt(dia,length):
	e=1.5*dia
	h1=1.25*dia
	return union([
		cylinder(r=dia/2,h=length),
		translate([0,0,-h1], cylinder(r=e/2,h=h1))
	])

def csk_bolt(dia,length):
	h1=0.6*dia
	h2=length-h1
	return union([
		cylinder(r=dia/2,h=h2),
		cylinder(r1=dia,r2=dia/2,h=h1)
	])

def washer(dia):
	t=0.1*dia
	return difference([
		cylinder(r=dia,h=t),
		translate([0,0,-t/2], cylinder(r=dia/2,h=t*2))
	])

def flat_nut(dia):
	m=0.8*dia
	e=1.8*dia
	c=0.2*dia
	diff = [
		cylinder(r=e/2,h=m).fn(6),
		translate([0,0,-m/2], cylinder(r=dia/2,h=m*2))
	]
	if apply_chamfer:
	    diff.append(translate([0,0,c], cylinder_chamfer(e/2,c)))
	return difference(diff)

def bolt(dia,length):
	e=1.8*dia
	k=0.7*dia
	c=0.2*dia
	diff = [cylinder(r=e/2,h=k).fn(6)]
	if apply_chamfer:
		diff.append(translate([0,0,c], cylinder_chamfer(e/2,c)))

	return union([
		difference(diff),
		cylinder(r=dia/2,h=length)
	])

def cylinder_chamfer(r1,r2):
	t=r1-r2
	p=r2*2
	return rotate_extrude(child=difference([
		translate([t,-p], square([p,p])),
		translate([t,0], circle(r2))
	]))

def chamfer(length,r):
	p=r*2
	return linear_extrude(h=length, child=difference([
		square([p,p]),
		circle(r)
	]))

assemble(union([
	#sphere(10),
	#csk_bolt(3,14),
	#washer(3),
	#flat_nut(3),
	#bolt(4,14),
	#cylinder_chamfer(8,1),
	#chamfer(10,2),
]))
