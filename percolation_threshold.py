import rhinoscriptsyntax as rs
import Frac
import Domain
import DFN_Gen 
import DFN_Analysis
from DFN_Analysis import IntersectionAnalysis 
from Frac import Fracture
from DFN_Analysis import CutPlane
from Matrix import Matrix
import Input
import StatInput
import scriptcontext as sc
import math
import random

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
#Np = 0
#for i in range(50):
#dom = Domain.Domain(boxlength) 
## draws domain
#d = dom.Show() 
#n =54
## NB: The arguments of FixedFractureGen() must be edited to suit the 
## shape type, For instance, sides, min_angle and max_angle should be 
## specified for a polygon
#frac_list = DFN_Gen.FixedFractureGen(n,1.5,0,360,4)
#f = fractures(frac_list)
#boundary_list = dom.CreateBoundary(20)
## create the intersection matrix to test for percolation
#matrix = dom.IntersectionMatrix(boundary_list,f)
##print(matrix)
## check for percolation between the two opposite boundaries specified
## boundary_list[2] & boundary_list[4] for horizontal facing 1
## boundary_list[3] & boundary_list[5] for horizontal facing 2
#per1 = dom.Percolate(boundary_list[2],boundary_list[4],boundary_list,matrix,f)
#print(per1)
#    if per1:
#        Np+=1
#    if not per1:
#        sc.doc.Objects.Clear()
#print(Np)
def GeneratePoint(boxlength):
    if location_dist == 'uniform':
        x = random.uniform(0,boxlength)
        y = random.uniform(0,boxlength)   
        z = random.uniform(0,boxlength)
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
            radius = random.ex   
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
        #initialise a list called norm
            norm = []
            #define a random vector
            vector = [random.uniform(0,boxlength),random.uniform(0,boxlength),random.uniform(0,boxlength)]
            #a loop to store the difference between the origin and vector
            for i in range(3):
                norm.append(vector[i] - origin[i])
            #store the norm as normal
            #normal = norm
            #unitize the 3d vector
            normal = rs.VectorUnitize(norm)
            #convert the origin to a plane
            plane = rs.PlaneFromNormal(origin, normal)
            return plane
def FixedFractureGen(n, aspect_ratio=None,min_angle=None,max_angle=None,sides=None):
    """
    A function to add a fixed number of circles in a cube. It also writes data 
    to fracture data text file for regenerating fracture networks.
    """
    ##file = open(path,'a')
    if fracture_shape == 'circle':
        #write the shape type
        file.write('\ncircle')
        #initialize a to store fractures
        fracture_list = []
        #a loop to insert the fixed number of fractures
        for i in range(n):
            #layer name for the frcature
            layer_name = "FRACTURE_" + str(i+1)
            #create an istance of Fracture class
            frac = Fracture()
            #store fracture name
            frac.fracture_name = layer_name
            #generate origin for fracture
            origin = GeneratePoint(boxlength)
            #store farcture center
            frac.fracture_center = origin
            #convert the origin to a plane
            plane = InclinePlane(origin)
            #add layer and color
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            #make current layer
            rs.CurrentLayer(layer_name)
            #insert the fracture in the domain
            my_circle = rs.AddCircle(plane,radius)
            # write the plane and radius to file for re-plotting
            ##file.write("\n" + str(plane[0]) + "," +  str(plane[1]) + "," +  str(plane[2]) + "," + str(radius))
            #circle_list.append(my_circle)
            surf = rs.AddPlanarSrf(my_circle)
            #delete initial fracture drawn which is a curve
            rs.DeleteObject(my_circle)
            #save fracture's GUID
            frac.fracture_GUID = surf[0]
            #append fracture into fracture list
            fracture_list.append(frac)
            
            
    elif fracture_shape == 'ellipse':
        #list to store fracture surface GUIDs
        fracture_list = []
        #write the shape type
        ##file.write('\nellipse')
        for i in range(n):
            #layer name for the frcature
            layer_name = "FRACTURE_" + str(i+1)
            #create an istance of Fracture class
            frac = Fracture()
            frac.fracture_name = layer_name
            #generate fracture origin
            origin = GeneratePoint(boxlength)
            frac.fracture_center = origin
            #plane for fracture
            plane = InclinePlane(origin)
            #calculate r_y
            ry = radius/aspect_ratio
            #create layer for fracture
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            rs.CurrentLayer(layer_name)
            #draw ellipse
            fracture = rs.AddEllipse(plane,radius, ry)
            # write the plane, r_x and r_y to file for re-plotting
            ##file.write("\n" + str(plane[0]) + "," +  str(plane[1]) + "," +  str(plane[2]) + "," + str(radius) + ","+ str(ry))
            #make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            #delete initial fracture drawn which is a curve
            rs.DeleteObject(fracture)
            #append surface GUID to list of fracture surfaces
            frac.fracture_GUID = frac_surf[0]
            fracture_list.append(frac)
        
    elif fracture_shape == 'polygon':
        #list to store fracture surface GUIDs
        fracture_list = []
        #write the shape type
        ##file.write('\npolygon\n')
        for i in range(n):
            layer_name = "FRACTURE_" + str(i+1)
            frac = Fracture()
            frac.fracture_name = layer_name
            #theta in radian
            theta_rad = (2*math.pi)/sides
            #theta in degree (interior angles)
            theta_deg = theta_rad*(180/math.pi)
            #generate origin
            origin = GeneratePoint(boxlength)
            frac.fracture_center = origin
            #create a 3D point object which isn't visible to the rhino document
            pt_01 = rs.coerce3dvector([radius+origin[0],origin[1],origin[2]])
            #empty list to store all points
            points = []
            #a rotation axis 
            ax = rs.coerce3dvector([0,0,1])
            #loop to generate points for polygon vertices
            #file.write("\n")
            for j in range(sides):
                #rotation transform with rotation from the origin
                trans = rs.XformRotation2(theta_deg*j, ax, origin)
                #transform the original 3D point and append to list
                points.append(rs.PointTransform(pt_01,trans))
                ##if j == 0:
                    ##file.write(str(rs.PointTransform(pt_01,trans)[0]) +  "," + str(rs.PointTransform(pt_01,trans)[1]) +  "," + str(rs.PointTransform(pt_01,trans)[2])+  ",")
                ##if j != 0:
                    ##file.write(str(rs.PointTransform(pt_01,trans)[0]) +  "," + str(rs.PointTransform(pt_01,trans)[1]) +  "," + str(rs.PointTransform(pt_01,trans)[2])+ ",")
            #append the initial point to close the polygon
            points.append(pt_01)
            ##file.write(str(pt_01[0]) + "," + str(pt_01[1]) + "," + str(pt_01[2])+ ",")
            #create layer for fracture
            #layer_name = "FRACTURE_" + str(i+1)
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            rs.CurrentLayer(layer_name)
            #get GUID of created polygon
            polygon = rs.AddPolyline(points)
            #create an angle of rotation
            angle = PolyOrientation(min_angle,max_angle)
            #rotate polygon about y-axis
            fracture = rs.RotateObject(polygon,origin,angle,[0,1,0])
            ##file.write(str(origin[0]) + "," + str(origin[1]) + "," + str(origin[2]) + "," +  str(angle) + "," + str(sides) + "\n")
            #make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            #delete initial fracture drawn which is a curve
            rs.DeleteObject(fracture)
            frac.fracture_GUID = frac_surf[0]
            fracture_list.append(frac)
    ##file.close()        
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
# define path
#path1 = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/percolation_probability.txt"
#path2 = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/open_area.txt"
#file1 = open(path1, 'w')
#file2 = open(path2, 'w')
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
        #dom.RemoveSurfacesOutsideOfBox(dom.length) #trims fractures outside the domain
        #dom_frac = dom.my_fractures #get the fractures in the domain
        #swap old guids with new ones and put new guids in old frac layers
        #new_frac_guids = Frac.new_fracture_guids(dom_frac,frac_list) 
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
    
# write to file 
#file1.write(str(percolation_probability))
#file2.write(str(S_0))
# close file
#file1.close()
#file2.close()