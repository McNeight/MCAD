# License: LGPL 2.1

from openscad import *

rodsize = 6	# threaded/smooth rod diameter in mm
xaxis = 182.5	# width of base in mm
yaxis = 266.5	# length of base in mm

screwsize = 3		# bearing bore/screw diameter in mm
bearingsize = 10	# outer diameter of bearings in mm
bearingwidth = 4	# width of bearings in mm

rodpitch = rodsize / 6
rodnutsize = 0.8 * rodsize
rodnutdiameter = 1.9 * rodsize
rodwashersize = 0.2 * rodsize
rodwasherdiameter = 2 * rodsize
screwpitch = float(screwsize) / 6
nutsize = 0.8 * screwsize
nutdiameter = 1.9 * screwsize
washersize = 0.2 * screwsize
washerdiameter = 2 * screwsize
partthick = 2 * rodsize
vertexrodspace = 2 * rodsize

c = [0.3, 0.3, 0.3]
rodendoffset = rodnutsize + rodwashersize * 2 + partthick / 2
vertexoffset = vertexrodspace + rodendoffset

renderrodthreads = True
renderscrewthreads = True
fn = 36

def rod(length, threaded=False):
	if threaded and renderrodthreads:
		return linear_extrude(h = length, center = True, convexity = 10, twist = -360 * length / rodpitch, child=
			translate([rodsize * 0.1 / 2, 0, 0], circle(rodsize * 0.9 / 2).fn(fn))
		).fn(fn)
	else:
		return cylinder(h = length, r = rodsize / 2, center = True).fn(fn)

def screw(length, nutpos, washers=0, bearingpos = -1):
	result = [render(difference([
		translate([0, 0, screwsize / 2], cylinder(h = screwsize, r = screwsize, center = True).fn(fn)),
		translate([0, 0, screwsize], cylinder(h = screwsize, r = screwsize / 2, center = True).fn(fn))
	]))]
	if renderscrewthreads:
		t = linear_extrude(h = length, center = True, convexity = 10, twist = -360 * length / screwpitch, child=
			translate([screwsize * 0.1 / 2, 0, 0], circle(screwsize * 0.9 / 2).fn(fn))
		).fn(fn)
	else:
		t = cylinder(h = length, r = screwsize / 2, center = True).fn(fn)
	result.append(translate([0, 0, -length / 2], t))
	if washers > 0 and nutpos > 0:
		result.append(washer(nutpos))
		result.append(nut(nutpos+washersize))
	elif nutpos > 0:
		result.append(nut(nutpos))
	if bearingpos >= 0:
		result.append(bearing(bearingpos))
	return union(result)

def bearing(position=0):
	return render(translate([0, 0, -position - bearingwidth / 2], union([
		difference([
			cylinder(h = bearingwidth, r = bearingsize / 2, center = True).fn(fn),
			cylinder(h = bearingwidth * 2, r = bearingsize / 2 - 1, center = True).fn(fn)
		]),
		difference([
			cylinder(h = bearingwidth - 0.5, r = bearingsize / 2 - 0.5, center = True).fn(fn),
			cylinder(h = bearingwidth * 2, r = screwsize / 2 + 0.5, center = True).fn(fn)
		]),
		difference([
			cylinder(h = bearingwidth, r = screwsize / 2 + 1, center = True).fn(fn),
			cylinder(h = bearingwidth + 0.1, r = screwsize / 2, center = True).fn(fn)
		])
	])))

def nut(position=0, washers=0):
	result = [intersection([
		scale([1, 1, 0.5], sphere(1.05 * screwsize)),
		difference([
			cylinder(h = nutsize, r = nutdiameter / 2, center = True).fn(6),
			cylinder(r = screwsize / 2, h = nutsize + 0.1, center = True).fn(fn)
		])
	])]
	if washers > 0:
		result.append(washer(0))
	return render(translate([0, 0, -position - nutsize / 2], union(result)))


def washer(position=0):
	return render(translate([0, 0, -position - washersize / 2], difference([
		cylinder(r = washerdiameter / 2, h = washersize, center = True).fn(fn),
		cylinder(r = screwsize / 2, h = washersize + 0.1, center = True).fn(fn)
	])))

def rodnut(position=0, washers=0):
	result = [intersection([
		scale([1, 1, 0.5], sphere(1.05 * rodsize)),
		difference([
			cylinder (h = rodnutsize, r = rodnutdiameter / 2, center = True).fn(6),
			rod(rodnutsize + 0.1)
		])
	])]
	if washers == 1 or washers == 4:
		result.append(rodwasher((-1 if position > 0 else 1) * (rodnutsize + rodwashersize) / 2))
	if washers == 2 or washers == 4:
		result.append(rodwasher((1 if position > 0 else -1) * (rodnutsize + rodwashersize) / 2))

	return render(translate([0, 0, position], union(result)))

def rodwasher(position=0):
	return render(translate ([0, 0, position], difference([
		cylinder(r = rodwasherdiameter / 2, h = rodwashersize, center = True).fn(fn),
		rod(rodwashersize + 0.1)
	])))

def test_smooth_rod():
	return rod(20)

def test_threaded_rod():
	return translate([rodsize * 2.5, 0, 0], rod(20, True))

def test_screw():
	return translate([rodsize * 5, 0, 0], screw(10, 1, washers=1))

def test_bearing():
	return translate([rodsize * 7.5, 0, 0], bearing())

def test_rodnut():
	return translate([rodsize * 10, 0, 0], rodnut())

def test_rodwasher():
	return translate([rodsize * 12.5, 0, 0], rodwasher())

def test_nut():
	return translate([rodsize * 15, 0, 0], nut())

def test_washer():
	return translate([rodsize * 17.5, 0, 0], washer())

assemble(union([
	#test_smooth_rod(),
	#test_threaded_rod(),
	#test_screw(),
	#test_bearing(),
	#test_rodnut(),
	#test_rodwasher(),
	#test_nut(),
	#test_washer(),
]))
