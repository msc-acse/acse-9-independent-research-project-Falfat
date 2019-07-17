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
    
    
def AddRandomEllipse(rx_min, rx_max, aspect_min, aspect_max):
    #generate random number of fractures
    n = random.randint(10,50)
    
    #list to store fracture surface GUIDs
    fracture_surface = []
    for i in range(n):
        #generate fracture origin
        origin = generate_point(boxlength)
        #plane for fracture
        plane = InclinePlane(origin)
        #radius of fracture(r_x)
        rx = random.uniform(rx_min, rx_max)
        #aspect ratio of fracture
        aspect_ratio = random.randint(aspect_min,aspect_max)
        #calculate r_y
        ry = rx/aspect_ratio
        #create layer for fracture
        layer_name = "FRACTURE" + str(i+1)
        rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
        rs.CurrentLayer(layer_name)
        #create ellipse
        frac = rs.AddEllipse(plane,rx, ry)
        #make fracture a surface
        frac_surf = rs.AddPlanarSrf(frac)
        #append surface GUID to list of fracture surfaces
        fracture_surface.append(frac_surf[0])
        
    return fracture_surface

def AddEllipse(rx, aspect_ratio):
    
    #list to store fracture surface GUIDs
    fracture_surface = []
    for i in range(n):
        #generate fracture origin
        origin = generate_point(boxlength)
        #plane for fracture
        plane = InclinePlane(origin)
        #calculate r_y
        ry = rx/aspect_ratio
        #create layer for fracture
        layer_name = "FRACTURE" + str(i+1)
        rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
        rs.CurrentLayer(layer_name)
        #draw ellipse
        frac = rs.AddEllipse(plane,rx, ry)
        #make fracture a surface
        frac_surf = rs.AddPlanarSrf(frac)
        #append surface GUID to list of fracture surfaces
        fracture_surface.append(frac_surf[0])
        
    return fracture_surface
        
            
    
if __name__ == "__main__":
    rs.EnableRedraw(False)
    
    rs.AddBox(corners)
    #fractures = AddRandomEllipse(2,4,1,2)
    fractures = AddEllipse(3,2)
    sec.LengthOfIntersection(fractures)
    #surface = AddCircle(n,radius,boxlength)