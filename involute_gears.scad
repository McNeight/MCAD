# Parametric Involute Bevel and Spur Gears by GregFrost
# It is licensed under the Creative Commons - GNU LGPL 2.1 license.
# © 2010 by GregFrost, thingiverse.com/Amp
# http://www.thingiverse.com/thing:3575 and http://www.thingiverse.com/thing:3752

from math import pi, sin, cos, tan, sqrt, asin, atan2
from openscad import *

pi2=pi*2

# Simple Test:
#gear (circular_pitch=700*pi/180,
#	gear_thickness = 12,
#	rim_thickness = 15,
#	hub_thickness = 17,
#	circles=8)



#Complex Spur Gear Test:
#test_gears ()

# Meshing Double Helix:
#test_meshing_double_helix ()

def test_meshing_double_helix():
    return meshing_double_helix ()


# Demonstrate the backlash option for Spur gears.
#test_backlash ()

# Demonstrate how to make meshing bevel gears.
#test_bevel_gear_pair()

def test_bevel_gear_pair():
    return bevel_gear_pair ()


def test_bevel_gear():
	return bevel_gear()

#bevel_gear()


#==================================================
# Bevel Gears:
# Two gears with the same cone distance, circular pitch (measured at the cone distance)
# and pressure angle will mesh.

def bevel_gear_pair (
	gear1_teeth = 41,
	gear2_teeth = 7,
	axis_angle = 90,
	outside_circular_pitch=1000):

	outside_pitch_radius1 = gear1_teeth * outside_circular_pitch / pi2
	outside_pitch_radius2 = gear2_teeth * outside_circular_pitch / pi2
	pitch_apex1=outside_pitch_radius2 * sin(axis_angle) + (
		outside_pitch_radius2 * cos(axis_angle) + outside_pitch_radius1
		) / tan(axis_angle)
	cone_distance = sqrt (pow (pitch_apex1, 2) + pow (outside_pitch_radius1, 2))
	pitch_apex2 = sqrt (pow (cone_distance, 2) - pow (outside_pitch_radius2, 2))
	print("cone_distance " + str(cone_distance))
	pitch_angle1 = asin (outside_pitch_radius1 / cone_distance)
	pitch_angle2 = asin (outside_pitch_radius2 / cone_distance)
	print("pitch_angle1, pitch_angle2 " + str(pitch_angle1, pitch_angle2))
	print("pitch_angle1 + pitch_angle2 " + str(pitch_angle1 + pitch_angle2))

	return rotate([0,0,90],
		translate ([0,0,pitch_apex1+20],
			translate([0,0,-pitch_apex1],
				bevel_gear (
					number_of_teeth=gear1_teeth,
					cone_distance=cone_distance,
					pressure_angle=30*pi/180,
					outside_circular_pitch=outside_circular_pitch)
			) + 
			rotate([0,-(pitch_angle1+pitch_angle2),0],
				translate([0,0,-pitch_apex2],
					bevel_gear (
						number_of_teeth=gear2_teeth,
						cone_distance=cone_distance,
						pressure_angle=30*pi/180,
						outside_circular_pitch=outside_circular_pitch)
				)
			)
		)
	)

#Bevel Gear Finishing Options:
bevel_gear_flat = 0
bevel_gear_back_cone = 1

"""
module bevel_gear (
	number_of_teeth=11,
	cone_distance=100,
	face_width=20,
	outside_circular_pitch=1000,
	pressure_angle=30*pi/180,
	clearance = 0.2,
	bore_diameter=5,
	gear_thickness = 15,
	backlash = 0,
	involute_facets=0,
	finish = -1)
{
	echo ("bevel_gear",
		"teeth", number_of_teeth,
		"cone distance", cone_distance,
		face_width,
		outside_circular_pitch,
		pressure_angle,
		clearance,
		bore_diameter,
		involute_facets,
		finish);

	// Pitch diameter: Diameter of pitch circle at the fat end of the gear.
	outside_pitch_diameter  =  number_of_teeth * outside_circular_pitch / 180;
	outside_pitch_radius = outside_pitch_diameter / 2;

	// The height of the pitch apex.
	pitch_apex = sqrt (pow (cone_distance, 2) - pow (outside_pitch_radius, 2));
	pitch_angle = asin (outside_pitch_radius/cone_distance);

	echo ("Num Teeth:", number_of_teeth, " Pitch Angle:", pitch_angle);

	finish = (finish != -1) ? finish : (pitch_angle < 45) ? bevel_gear_flat : bevel_gear_back_cone;

	apex_to_apex=cone_distance / cos (pitch_angle);
	back_cone_radius = apex_to_apex * sin (pitch_angle);

	// Calculate and display the pitch angle. This is needed to determine the angle to mount two meshing cone gears.

	// Base Circle for forming the involute teeth shape.
	base_radius = back_cone_radius * cos (pressure_angle);

	// Diametrial pitch: Number of teeth per unit length.
	pitch_diametrial = number_of_teeth / outside_pitch_diameter;

	// Addendum: Radial distance from pitch circle to outside circle.
	addendum = 1 / pitch_diametrial;
	// Outer Circle
	outer_radius = back_cone_radius + addendum;

	// Dedendum: Radial distance from pitch circle to root diameter
	dedendum = addendum + clearance;
	dedendum_angle = atan (dedendum / cone_distance);
	root_angle = pitch_angle - dedendum_angle;

	root_cone_full_radius = tan (root_angle)*apex_to_apex;
	back_cone_full_radius=apex_to_apex / tan (pitch_angle);

	back_cone_end_radius =
		outside_pitch_radius -
		dedendum * cos (pitch_angle) -
		gear_thickness / tan (pitch_angle);
	back_cone_descent = dedendum * sin (pitch_angle) + gear_thickness;

	// Root diameter: Diameter of bottom of tooth spaces.
	root_radius = back_cone_radius - dedendum;

	half_tooth_thickness = outside_pitch_radius * sin (360 / (4 * number_of_teeth)) - backlash / 4;
	half_thick_angle = asin (half_tooth_thickness / back_cone_radius);

	face_cone_height = apex_to_apex-face_width / cos (pitch_angle);
	face_cone_full_radius = face_cone_height / tan (pitch_angle);
	face_cone_descent = dedendum * sin (pitch_angle);
	face_cone_end_radius =
		outside_pitch_radius -
		face_width / sin (pitch_angle) -
		face_cone_descent / tan (pitch_angle);

	// For the bevel_gear_flat finish option, calculate the height of a cube to select the portion of the gear that includes the full pitch face.
	bevel_gear_flat_height = pitch_apex - (cone_distance - face_width) * cos (pitch_angle);

//	translate([0,0,-pitch_apex])
	difference ()
	{
		intersection ()
		{
			union()
			{
				rotate (half_thick_angle)
				translate ([0,0,pitch_apex-apex_to_apex])
				cylinder ($fn=number_of_teeth*2, r1=root_cone_full_radius,r2=0,h=apex_to_apex);
				for (i = [1:number_of_teeth])
//				for (i = [1:1])
				{
					rotate ([0,0,i*360/number_of_teeth])
					{
						involute_bevel_gear_tooth (
							back_cone_radius = back_cone_radius,
							root_radius = root_radius,
							base_radius = base_radius,
							outer_radius = outer_radius,
							pitch_apex = pitch_apex,
							cone_distance = cone_distance,
							half_thick_angle = half_thick_angle,
							involute_facets = involute_facets);
					}
				}
			}

			if (finish == bevel_gear_back_cone)
			{
				translate ([0,0,-back_cone_descent])
				cylinder (
					$fn=number_of_teeth*2,
					r1=back_cone_end_radius,
					r2=back_cone_full_radius*2,
					h=apex_to_apex + back_cone_descent);
			}
			else
			{
				translate ([-1.5*outside_pitch_radius,-1.5*outside_pitch_radius,0])
				cube ([3*outside_pitch_radius,
					3*outside_pitch_radius,
					bevel_gear_flat_height]);
			}
		}

		if (finish == bevel_gear_back_cone)
		{
			translate ([0,0,-face_cone_descent])
			cylinder (
				r1=face_cone_end_radius,
				r2=face_cone_full_radius * 2,
				h=face_cone_height + face_cone_descent+pitch_apex);
		}

		translate ([0,0,pitch_apex - apex_to_apex])
		cylinder (r=bore_diameter/2,h=apex_to_apex);
	}
}

module involute_bevel_gear_tooth (
	back_cone_radius,
	root_radius,
	base_radius,
	outer_radius,
	pitch_apex,
	cone_distance,
	half_thick_angle,
	involute_facets)
{
//	echo ("involute_bevel_gear_tooth",
//		back_cone_radius,
//		root_radius,
//		base_radius,
//		outer_radius,
//		pitch_apex,
//		cone_distance,
//		half_thick_angle);

	min_radius = max (base_radius*2,root_radius*2);

	pitch_point =
		involute (
			base_radius*2,
			involute_intersect_angle (base_radius*2, back_cone_radius*2));
	pitch_angle = atan2 (pitch_point[1], pitch_point[0]);
	centre_angle = pitch_angle + half_thick_angle;

	start_angle = involute_intersect_angle (base_radius*2, min_radius);
	stop_angle = involute_intersect_angle (base_radius*2, outer_radius*2);

	res=(involute_facets!=0)?involute_facets:($fn==0)?5:$fn/4;

	translate ([0,0,pitch_apex])
	rotate ([0,-atan(back_cone_radius/cone_distance),0])
	translate ([-back_cone_radius*2,0,-cone_distance*2])
	union ()
	{
		for (i=[1:res])
		{
			assign (
				point1=
					involute (base_radius*2,start_angle+(stop_angle - start_angle)*(i-1)/res),
				point2=
					involute (base_radius*2,start_angle+(stop_angle - start_angle)*(i)/res))
			{
				assign (
					side1_point1 = rotate_point (centre_angle, point1),
					side1_point2 = rotate_point (centre_angle, point2),
					side2_point1 = mirror_point (rotate_point (centre_angle, point1)),
					side2_point2 = mirror_point (rotate_point (centre_angle, point2)))
				{
					polyhedron (
						points=[
							[back_cone_radius*2+0.1,0,cone_distance*2],
							[side1_point1[0],side1_point1[1],0],
							[side1_point2[0],side1_point2[1],0],
							[side2_point2[0],side2_point2[1],0],
							[side2_point1[0],side2_point1[1],0],
							[0.1,0,0]],
						triangles=[[0,1,2],[0,2,3],[0,3,4],[0,5,1],[1,5,2],[2,5,3],[3,5,4],[0,4,5]]);
				}
			}
		}
	}
}
"""
def gear(
	number_of_teeth=15,
	circular_pitch=False, diametral_pitch=False,
	pressure_angle=28*pi/180,
	clearance = 0.2,
	gear_thickness=5,
	rim_thickness=8,
	rim_width=5,
	hub_thickness=10,
	hub_diameter=15,
	bore_diameter=5,
	circles=0,
	backlash=0,
	twist=0,
	involute_facets=0,
	flat=False):

	if circular_pitch==False and diametral_pitch==False:
		print("MCAD ERROR: gear module needs either a diametral_pitch or circular_pitch")

	#Convert diametrial pitch to our native circular pitch
	if circular_pitch==False:
		circular_pitch=1.0/diametral_pitch

	# Pitch diameter: Diameter of pitch circle.
	pitch_diameter  =  number_of_teeth * circular_pitch / pi
	pitch_radius = pitch_diameter/2
	print ("Teeth:" + str(number_of_teeth) + " Pitch radius:" + str(pitch_radius))

	# Base Circle
	base_radius = pitch_radius*cos(pressure_angle)

	# Diametrial pitch: Number of teeth per unit length.
	pitch_diametrial = number_of_teeth / pitch_diameter

	# Addendum: Radial distance from pitch circle to outside circle.
	addendum = 1/pitch_diametrial

	#Outer Circle
	outer_radius = pitch_radius+addendum

	# Dedendum: Radial distance from pitch circle to root diameter
	dedendum = addendum + clearance

	# Root diameter: Diameter of bottom of tooth spaces.
	root_radius = pitch_radius-dedendum
	backlash_angle = backlash / float(pitch_radius)
	half_thick_angle = (2.0 * pi / number_of_teeth - backlash_angle) / 4;

	# Variables controlling the rim.
	rim_radius = root_radius - rim_width;

	# Variables controlling the circular holes in the gear.
	circle_orbit_diameter=hub_diameter/2+rim_radius
	circle_orbit_curcumference=pi*circle_orbit_diameter

	# Limit the circle size to 90% of the gear face.
	if circles>0:
		circle_diameter = min ( 0.70*circle_orbit_curcumference/circles,
			(rim_radius-hub_diameter/2)*0.9)

	geardisc = linear_extrude_flat_option(flat=flat, height=rim_thickness, convexity=10, twist=twist, child = 
		gear_shape(	number_of_teeth,
			pitch_radius = pitch_radius,
			root_radius = root_radius,
			base_radius = base_radius,
			outer_radius = outer_radius,
			half_thick_angle = half_thick_angle,
			involute_facets=involute_facets)	)

	if gear_thickness < rim_thickness:
		geardisc -= translate ([0,0,gear_thickness], 
			cylinder (r=rim_radius,h=rim_thickness-gear_thickness+1))

	if gear_thickness > rim_thickness:
		geardisc += linear_exturde_flat_option(flat=flat, height=gear_thickness, child=
				circle (r=rim_radius))

	if flat == False and hub_thickness > gear_thickness:
		geardisc +=translate ([0,0,gear_thickness], 
			linear_extrude_flat_option(flat=flat, height=hub_thickness-gear_thickness, child=circle(hub_diameter/2.0)))
	geardisc -= translate ([0,0,-1],
		linear_extrude_flat_option(flat =flat, height=2+max(rim_thickness,hub_thickness,gear_thickness), child=
		circle (bore_diameter/2)))

	if (circles>0):
		for i in range(circles):
			geardisc -= rotate([0,0,i*360/circles],
				translate([circle_orbit_diameter/2,0,-1],
					linear_extrude_flat_option(flat =flat, height=max(gear_thickness,rim_thickness)+3, child = circle(circle_diameter/2))))

	return geardisc

def linear_extrude_flat_option(child, flat =False, height = 10, center = False, convexity = 2, twist = 0):
	if flat == False:
		return linear_extrude(h = height, center = center, convexity = convexity, twist= twist, child=child)
	else:
		return child

def gear_shape (
	number_of_teeth,
	pitch_radius,
	root_radius,
	base_radius,
	outer_radius,
	half_thick_angle,
	involute_facets):

	c = circle(root_radius)
	c.fn=number_of_teeth*2

	return union([
		rotate(half_thick_angle, child=c)] + [
		rotate ([0,0,i*360/number_of_teeth],
			involute_gear_tooth(
				pitch_radius = pitch_radius,
				root_radius = root_radius,
				base_radius = base_radius,
				outer_radius = outer_radius,
				half_thick_angle = half_thick_angle,
				involute_facets=involute_facets)
		) for i in range(number_of_teeth)])

def involute_gear_tooth (
	pitch_radius,
	root_radius,
	base_radius,
	outer_radius,
	half_thick_angle,
	involute_facets):

	min_radius = max(base_radius,root_radius)

	pitch_point = involute (base_radius, involute_intersect_angle (base_radius, pitch_radius))

	pitch_angle = atan2 (pitch_point[1], pitch_point[0])
	centre_angle = pitch_angle + half_thick_angle

	start_angle = involute_intersect_angle (base_radius, min_radius)
	stop_angle = involute_intersect_angle (base_radius, outer_radius)

	res=((openscad.fn/4,5)[openscad.fn==0],involute_facets)[involute_facets!=0]
	
	pl1 = []
	pl2 = []
	for i in range(0,res+1):
		p = involute(base_radius,start_angle+(stop_angle - start_angle)*i/res)
		p = rotate_point (centre_angle, p)
		pl1.append( p )
		pl2.append( mirror_point( p ) )
	pl2.reverse()
	return polygon( [[0,0]] + pl1 + pl2 )

# Mathematical Functions
#===============

# Finds the angle of the involute about the base radius at the given distance (radius) from it's center.
#source: http://www.mathhelpforum.com/math-help/geometry/136011-circle-involute-solving-y-any-given-x.html

def involute_intersect_angle (base_radius, radius):
	return sqrt (pow (radius/float(base_radius), 2.0) - 1.0);

# Calculate the involute position for a given base radius and involute angle.

def rotated_involute(rotate, base_radius, involute_angle):
	return [
		cos (rotate) * involute (base_radius, involute_angle)[0] + sin (rotate) * involute (base_radius, involute_angle)[1],
		cos (rotate) * involute (base_radius, involute_angle)[1] - sin (rotate) * involute (base_radius, involute_angle)[0]
		]

def mirror_point (coord):
	return [
		coord[0],
		-coord[1]
		]

def rotate_point (rotate, coord):
	return [
		cos (rotate) * coord[0] + sin (rotate) * coord[1],
		cos (rotate) * coord[1] - sin (rotate) * coord[0]
		]

def involute(base_radius, involute_angle):
	return [
		base_radius*(cos (involute_angle) + involute_angle*sin (involute_angle)),
		base_radius*(sin (involute_angle) - involute_angle*cos (involute_angle))
		]



# Test Cases
#===============

def test_gears():
	return translate([17,-15],
		gear (number_of_teeth=17,
			circular_pitch=500*pi/180,
			circles=8) + rotate ([0,0,360*4/17],
			translate ([39.088888,0,0],
				gear (number_of_teeth=11,
					circular_pitch=500*pi/180,
					hub_diameter=0,
					rim_width=65) + translate ([0,0,8],
					gear (number_of_teeth=6,
						circular_pitch=300*pi/180,
						hub_diameter=0,
						rim_width=5,
						rim_thickness=6,
						pressure_angle=31*pi/180) +
					rotate ([0,0,360*5/6],
						translate ([22.5,0,1],
							gear (number_of_teeth=21,
								circular_pitch=300*pi/180,
								bore_diameter=2,
								hub_diameter=4,
								rim_width=1,
								hub_thickness=4,
								rim_thickness=4,
								gear_thickness=3,
								pressure_angle=31*pi/180)
						)
					)
				)
			)
		) + translate ([-61.1111111,0,0],
			gear (number_of_teeth=27,
				circular_pitch=500*pi/180,
				circles=5,
				hub_diameter=2*8.88888889) + translate([0,0,10],
				gear (
					number_of_teeth=14,
					circular_pitch=200*pi/180,
					pressure_angle=5*pi/180,
					clearance = 0.2,
					gear_thickness = 10,
					rim_thickness = 10,
					rim_width = 15,
					bore_diameter=5,
					circles=0) + translate ([13.8888888,0,1],
					gear (
						number_of_teeth=11,
						circular_pitch=200*pi/180,
						pressure_angle=5*pi/180,
						clearance = 0.2,
						gear_thickness = 10,
						rim_thickness = 10,
						rim_width = 15,
						hub_thickness = 20,
						hub_diameter=2*7.222222,
						bore_diameter=5,
						circles=0)
				)
			)
		) + rotate ([0,0,360*-5/17],
			translate ([44.444444444,0,0],
				gear (number_of_teeth=15,
					circular_pitch=500*pi/180,
					hub_diameter=10,
					rim_width=5,
					rim_thickness=5,
					gear_thickness=4,
					hub_thickness=6,
					circles=9)
			)
		) + rotate ([0,0,360*-1/17],
			translate ([30.5555555,0,-1],
				gear (number_of_teeth=5,
					circular_pitch=500*pi/180,
					hub_diameter=0,
					rim_width=5,
					rim_thickness=10)
			)
		)
	)

def meshing_double_helix():
	return test_double_helix_gear() + mirror ([0,1,0],
		translate ([175/3.0,0,0],
			test_double_helix_gear(teeth=13,circles=6)
		)
	)

def test_double_helix_gear(
	teeth=17,
	circles=8):

	#double helical gear
	twist=200
	height=20
	pressure_angle=30*pi/180

	return gear (number_of_teeth=teeth,
		circular_pitch=700*pi/180,
		pressure_angle=pressure_angle,
		clearance = 0.2,
		gear_thickness = height/2*0.5,
		rim_thickness = height/2,
		rim_width = 5,
		hub_thickness = height/2*1.2,
		hub_diameter=15,
		bore_diameter=5,
		circles=circles,
		twist=twist/teeth) + mirror([0,0,1],
		gear (number_of_teeth=teeth,
			circular_pitch=700*pi/180,
			pressure_angle=pressure_angle,
			clearance = 0.2,
			gear_thickness = height/2,
			rim_thickness = height/2,
			rim_width = 5,
			hub_thickness = height/2,
			hub_diameter=15,
			bore_diameter=5,
			circles=circles,
			twist=twist/teeth)
	)


def test_backlash():
	backlash = 2
	teeth = 15
	cyl = cylinder(r=backlash / float(4),h=25).fn(20)
	return translate([-29.166666,0,0],
		translate ([58.3333333,0,0],
			rotate ([0,0,-360/teeth/4],
				gear (
					number_of_teeth = teeth,
					circular_pitch=700*pi/180,
					gear_thickness = 12,
					rim_thickness = 15,
					rim_width = 5,
					hub_thickness = 17,
					hub_diameter=15,
					bore_diameter=5,
					backlash = backlash,
					circles=8)
			)
		) + rotate ([0,0,360/teeth/4],
			gear (
				number_of_teeth = teeth,
				circular_pitch=700*pi/180,
				gear_thickness = 12,
				rim_thickness = 15,
				rim_width = 5,
				hub_thickness = 17,
				hub_diameter=15,
				bore_diameter=5,
				backlash = backlash,
				circles=8)
		)
	) + color([0,0,128,0.5],
		translate([0,0,-5],
			cyl
		)
	)



assemble( 
#	test_meshing_double_helix ()
	test_backlash ()
)