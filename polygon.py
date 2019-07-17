import rhinoscriptsyntax as rs
import math
import random
import sec

def ReadFile(file):
    #open the file
    file = open(file, "r")
    
    #read the lines of the file
    f1 = file.readlines()
    
    for line in f1:
        #check for a line in which starts with "radius"
        if line.find("radius") == 0:
            #split the line
            line1 = line.split()
            #store the value of radius as a float
            radius = float(line1[2])
        #check for a line in which starts with "length"
        if line.find("length") == 0:
            #split the line
            line1 = line.split()
            #store the value of the box length as a float
            boxlength = float(line1[2])
        #check for a line in which starts with "numberof circles"
        if line.find("numberofcircles") == 0:
            #split the line
            line1 = line.split()
            #stre the nuber of circles as an integer
            n = int(line1[2])
    return radius, boxlength, n

name = "DataFile.txt"
radius, boxlength, n = ReadFile(name)

#define the corners of the cube based on the box length entered
corners = ([(0,0,0),(boxlength,0,0),(boxlength,boxlength,0),(0,boxlength,0),(0,0,boxlength),(boxlength,0,boxlength),(boxlength,boxlength,boxlength),(0,boxlength,boxlength)])

def generate_point(boxlength):
    x = random.uniform(0,boxlength)
    y = random.uniform(0,boxlength)   
    z = random.uniform(0,boxlength)
    return [x,y,z]
    
def InclinePlane(origin):
    """
    A function to get a plane for a circle, using its origin
    """
    #initialise a list called norm
    norm = []
    #define a random vector
    vector = [random.uniform(2,18),random.uniform(2,18),random.uniform(2,18)]
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

def AddRandomPolygon(min_size, max_size, min_frac, max_frac):
    #number of fractures to be generated
    n = random.randint(min_frac, max_frac)
    #list to store fracture surface GUIDs
    fracture_surface = []
    for i in range(n):
        #radius of fractures
        radius = random.randint(1,2)
        #number of siides
        sides = random.randint(min_size, max_size)
        #theta in radian
        theta_rad = (2*math.pi)/sides
        #theta in degree (interior angles)
        theta_deg = theta_rad*(180/math.pi)
        #generate origin
        origin = generate_point(boxlength)
        #create a 3D point object which isn't visible to the rhino document
        pt_01 = rs.coerce3dvector([radius+origin[0],origin[1],origin[2]])
        #empty list to store all points
        points = []
        #a rotation axis 
        ax = rs.coerce3dvector([0,0,1])
        #loop to generate points for polygon vertices
        for j in range(sides):
            #rotation transform with rotation from the origin
            trans = rs.XformRotation2(theta_deg*j, ax, origin)
            #transform the original 3D point and append to list
            points.append(rs.PointTransform(pt_01,trans))
        #append the initial point to close the polygon
        points.append(pt_01)
        #create layer for fracture
        layer_name = "FRACTURE" + str(i+1)
        rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
        rs.CurrentLayer(layer_name)
        #get GUID of created polygon
        polygon = rs.AddPolyline(points)
        #create an angle of rotation
        angle = random.randint(0,360)
        #rotate polygon about y-axis
        frac = rs.RotateObject(polygon,origin,angle,[0,1,0],True)
        #make fracture a surface
        frac_surf = rs.AddPlanarSrf(frac)
        #append surface GUID to list of fracture surfaces
        fracture_surface.append(frac_surf[0])
            
    return fracture_surface       
  

def AddPolygon(min_angle,max_angle, sides):
    #NB: size should be entered through text
    #list to store fracture surface GUIDs
    fracture_surface = []
    for i in range(n):
        #theta in radian
        theta_rad = (2*math.pi)/sides
        #theta in degree (interior angles)
        theta_deg = theta_rad*(180/math.pi)
        #generate origin
        origin = generate_point(boxlength)
        #create a 3D point object which isn't visible to the rhino document
        pt_01 = rs.coerce3dvector([radius+origin[0],origin[1],origin[2]])
        #empty list to store all points
        points = []
        #a rotation axis 
        ax = rs.coerce3dvector([0,0,1])
        #loop to generate points for polygon vertices
        for j in range(sides):
            #rotation transform with rotation from the origin
            trans = rs.XformRotation2(theta_deg*j, ax, origin)
            #transform the original 3D point and append to list
            points.append(rs.PointTransform(pt_01,trans))
        #append the initial point to close the polygon
        points.append(pt_01)
        #create layer for fracture
        layer_name = "FRACTURE" + str(i+1)
        rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
        rs.CurrentLayer(layer_name)
        #get GUID of created polygon
        polygon = rs.AddPolyline(points)
        #create an angle of rotation
        angle = random.randint(min_angle,max_angle)
        #rotate polygon about y-axis
        frac = rs.RotateObject(polygon,origin,angle,[0,1,0])
        #make fracture a surface
        frac_surf = rs.AddPlanarSrf(frac)
        #append surface GUID to list of fracture surfaces
        fracture_surface.append(frac_surf[0])
            
    return fracture_surface        
    
if __name__ == "__main__":
    rs.EnableRedraw(False)
    
    rs.AddBox(corners)
    fractures = AddPolygon(10,80,5)
    #fractures = AddRandomPolygon(4,8,10,30)
    #sec.LengthOfIntersection(fractures)