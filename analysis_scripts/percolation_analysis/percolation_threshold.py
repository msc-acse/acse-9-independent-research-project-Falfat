import rhinoscriptsyntax as rs
from DFN_Analysis import IntersectionAnalysis 
from Frac import Fracture
from DFN_Analysis import CutPlane
from Matrix import Matrix
import Input
import StatInput
import scriptcontext as sc
import math
import random
import Domain

rs.EnableRedraw(False)
sc.doc.Objects.Clear()

#input data
data = "DataFile.txt"
radius, boxlength, n, fracture_shape = Input.ReadFile(data)
stat_data = "StatFile.txt"
orientation_dist, location_dist, size_dist = StatInput.ReadFile(stat_data)

def fractures(frac_list):
    # get GUID of fractures from the Fracture class
    f = []
    for frac in frac_list:
        f.append(frac.fracture_GUID)
    return f

def GeneratePoint(boxlength):
    if location_dist == 'uniform':
        x = random.uniform(0, boxlength)
        y = random.uniform(0, boxlength)   
        z = random.uniform(0, boxlength)
        return [x,y,z]
    
def FractureSize(size_dist,radius_min, radius_max):
    try:
        if radius_min <= 0 or radius_max <= 0:
            raise ValueError
    except ValueError:
        print("The minimum and maximum radius should be greater than 0")
    else:
        if size_dist == 'uniform':
            radius = random.uniform(radius_min, radius_max)
        if size_dist == 'exponential':
            pass   
        return radius
        
def PolyOrientation(min_angle, max_angle):
    try:
        if min_angle < 0 or max_angle <= 0:
            raise ValueError
    except ValueError:
        print("The input values are not appropriate")
    else:
        return random.uniform(min_angle, max_angle)
    
def InclinePlane(origin):
    """
    A function to get a plane for a circle, using its origin
    """
    try:
        if (type(origin) != list):
            raise TypeError
    except TypeError:
        print("InclinedPlane() argument 'origin' should be a type list")
    else:
        if orientation_dist == 'uniform':
        # initialise a list called norm
            norm = []
            # define a random vector
            vector = [random.uniform(0,boxlength),random.uniform(0,boxlength),random.uniform(0,boxlength)]
            # a loop to store the difference between the origin and vector
            for i in range(3):
                norm.append(vector[i] - origin[i])
            # unitize the 3d vector
            normal = rs.VectorUnitize(norm)
            # convert the origin to a plane
            plane = rs.PlaneFromNormal(origin, normal)
            return plane

def FixedFractureGen(n, aspect_ratio=None,min_angle=None,max_angle=None,sides=None):
    """
    A function to add a fixed number of circles in a cube. It also writes data 
    to fracture data text file for regenerating fracture networks.
    """
    if fracture_shape == 'circle':
        # initialize a to store fractures
        fracture_list = []
        # a loop to insert the fixed number of fractures
        for i in range(n):
            # layer name for the frcature
            layer_name = "FRACTURE_" + str(i+1)
            # create an istance of Fracture class
            frac = Fracture()
            # store fracture name
            frac.fracture_name = layer_name
            # generate origin for fracture
            origin = GeneratePoint(boxlength)
            #store farcture center
            frac.fracture_center = origin
            # convert the origin to a plane
            plane = InclinePlane(origin)
            # add layer and color
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            # make current layer
            rs.CurrentLayer(layer_name)
            # insert the fracture in the domain
            my_circle = rs.AddCircle(plane,radius)
            # convert to surface
            surf = rs.AddPlanarSrf(my_circle)
            # delete initial fracture drawn which is a curve
            rs.DeleteObject(my_circle)
            # save fracture's GUID
            frac.fracture_GUID = surf[0]
            # append fracture into fracture list
            fracture_list.append(frac)
            
            
    elif fracture_shape == 'ellipse':
        # list to store fracture surface GUIDs
        fracture_list = []
        for i in range(n):
            # layer name for the frcature
            layer_name = "FRACTURE_" + str(i+1)
            # create an istance of Fracture class
            frac = Fracture()
            frac.fracture_name = layer_name
            # generate fracture origin
            origin = GeneratePoint(boxlength)
            frac.fracture_center = origin
            # plane for fracture
            plane = InclinePlane(origin)
            # calculate r_y
            ry = radius/aspect_ratio
            # create layer for fracture
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            rs.CurrentLayer(layer_name)
            # draw ellipse
            fracture = rs.AddEllipse(plane,radius, ry)
            # make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            # delete initial fracture drawn which is a curve
            rs.DeleteObject(fracture)
            # append surface GUID to list of fracture surfaces
            frac.fracture_GUID = frac_surf[0]
            fracture_list.append(frac)
        
    elif fracture_shape == 'polygon':
        # list to store fracture surface GUIDs
        fracture_list = []
        for i in range(n):
            layer_name = "FRACTURE_" + str(i+1)
            frac = Fracture()
            frac.fracture_name = layer_name
            # theta in radian
            theta_rad = (2*math.pi)/sides
            # theta in degree (interior angles)
            theta_deg = theta_rad*(180/math.pi)
            # generate origin
            origin = GeneratePoint(boxlength)
            frac.fracture_center = origin
            # create a 3D point object which isn't visible to the rhino document
            pt_01 = rs.coerce3dvector([radius+origin[0],origin[1],origin[2]])
            # empty list to store all points
            points = []
            # a rotation axis 
            ax = rs.coerce3dvector([0,0,1])
            # loop to generate points for polygon vertices
            for j in range(sides):
                # rotation transform with rotation from the origin
                trans = rs.XformRotation2(theta_deg*j, ax, origin)
                # transform the original 3D point and append to list
                points.append(rs.PointTransform(pt_01,trans))
            # append the first point to close the polygon   
            points.append(pt_01)
            # create new layer
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            # make current layer
            rs.CurrentLayer(layer_name)
            # get GUID of created polygon
            polygon = rs.AddPolyline(points)
            # create an angle of rotation
            angle = PolyOrientation(min_angle,max_angle)
            # rotate polygon about y-axis
            fracture = rs.RotateObject(polygon,origin,angle,[0,1,0])
            # make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            # delete initial fracture drawn which is a curve
            rs.DeleteObject(fracture)
            frac.fracture_GUID = frac_surf[0]
            fracture_list.append(frac)       
    return fracture_list

num_realisations = 500
Vex = 362
# list to store the percolation probability.
# percolation probability = Np/num_of realisations
# percolation probability is also the connectivity index 
percolation_probability = []
# list of fraction of open area
# fraction of open area = area of all fractures in the domain/area of domain
rho_p = []
# initialise fractures area for all realisations 
fractures_area = 0

for n in range(50,56,2): 
    # number of realisations that percolate
    Np = 0
    for j in range(num_realisations):
        # creates the domain
        dom = Domain.Domain(boxlength) 
        # draws domain
        d = dom.Show() 
        # NB: The arguments of FixedFractureGen() must be edited to suit the 
        # shape type, For instance, sides, min_angle and max_angle should be 
        # specified for a polygon
        frac_list = FixedFractureGen(n, 0, 0, 90, 4) # inserts fractures and returns the GUIDs
        f = fractures(frac_list)
        # get list of boundaries to test for percolation 
        boundary_list = dom.CreateBoundary(20)
        # create the intersection matrix to test for percolation
        matrix = dom.IntersectionMatrix(boundary_list,f)
        # check for percolation between the two opposite boundaries specified
        # boundary_list[2] & boundary_list[4] for horizontal facing 1
        # boundary_list[3] & boundary_list[5] for horizontal facing 2
        per1 = dom.Percolate(boundary_list[2],boundary_list[4],boundary_list,matrix,f)
        per2 = dom.Percolate(boundary_list[3],boundary_list[5],boundary_list,matrix,f)
        per3 = dom.Percolate(boundary_list[0],boundary_list[1],boundary_list,matrix,f)
        # if there is percolation
        if per1 or per2 or per3:
            # increase number of realisations that percolate
            Np+=1
            #return
        sc.doc.Objects.Clear()
    rho_prime = Vex*(n/8000)
    rho_p.append(rho_prime)
    percolation_probability.append(Np/num_realisations)
print(rho_p)
print(percolation_probability)
    