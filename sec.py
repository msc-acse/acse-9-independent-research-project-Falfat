import rhinoscriptsyntax as  rs
import random
import math
#import remove_surfaces_outside_of_box


#radius = 2
#boxlength = 20

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
#box = rs.GetBox(mode=4)
# how to edit the GetBox function and automate the user input?
#if box: rs.AddBox(box)

#define the corners of the cube based on the box length entered
corners = ([(0,0,0),(boxlength,0,0),(boxlength,boxlength,0),(0,boxlength,0),(0,0,boxlength),(boxlength,0,boxlength),(boxlength,boxlength,boxlength),(0,boxlength,boxlength)])
#if box: rs.AddBox(box)
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
    

def CubePlusCircles(radius,boxlength):
    """
    A function that generates a 20x20x20 cube and inserts 
    a random number of circles into the cube
    """
    #generate a random number of circle to be put in the box
    n = random.randint(1, 50)
    #draw the box using the corners entered by the user
    rs.AddBox(corners)
    #Add circles
    AddSeparatedCircle(n,radius,boxlength)
        #something like: mysurf = Surface From Planar Curves (mycircle)
        
def AddCircle(n,radius,boxlength):
    """
    A function to add a fixed number of circles in a cube
    """
    #initialize a list to store circle GUIDs
    circle_list = []
    surface_list = []
    #a loop to insert the fixed number of circles
    for i in range(n):
        #store the random origin
        origin = generate_point(boxlength)
        #convert the origin to a plane
        plane = InclinePlane(origin)
        #make a layer
        layer_name = "FRACTURE_" + str(i)
        rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
        rs.CurrentLayer(layer_name)
        #rs.LayerColor(layer_name,[0,255,0])
        #insert the circle in the cube
        my_circle = rs.AddCircle(plane,radius)
        #append the circle GUID to the list
        circle_list.append(my_circle)
        surf = rs.AddPlanarSrf(my_circle)
        surface_list.append(surf[0])
    #print surface_list
    return surface_list
        


def AddSeparatedCircle(n,radius,boxlength):
    """
    A function to add circles whose origin are separated by at least 1m
    """
    #generate random origin
    origin = generate_point(boxlength)
    plane = InclinePlane(origin)
    #add as layer
    layer_name = "FRACTURE_0"
    rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
    rs.CurrentLayer(layer_name)
    mycircle = rs.AddCircle(plane,radius)
    #convert to surface
    surf = rs.AddPlanarSrf(mycircle)
    #get the U domain
    dom = rs.SurfaceDomain(surf,0)
    #append to domain_list
    domain_list=[[dom]]
    #list for layer names
    layers_list = [layer_name] 
    for i in range(n-1):
        k=i #set k to current iteration number
        origin = generate_point(boxlength)
        plane = InclinePlane(origin)
        layer_name = "FRACTURE_" + str(i+1)
        layers_list.append(layer_name)
        rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
        rs.CurrentLayer(layer_name)
        mycircle = rs.AddCircle(plane,radius)
        surf = rs.AddPlanarSrf(mycircle)
        dom = rs.SurfaceDomain(surf,0)
        #loop through the domain list
        for j in range(len(domain_list)):
            #calculate dist
            d = rs.Distance(dom,domain_list[j])
            if d <= 1:
                #delete previous layer
                rs.PurgeLayer(layers_list[j])
                #delete from list of layers
                del layers_list[j]
                i = k #do current iteration number
            
        domain_list.append([dom])
        
        
def LengthOfIntersection(surface_list):
    length = 0
    for i in range(len(surface_list)):
        curveA = surface_list[i]
        for j in range(len(surface_list)):
            if j != i:
                #print "Comparing " + str(rs.ObjectType(curveA)) + " and " + str(rs.ObjectType(surface_list[j]))
                intersection = rs.IntersectBreps(curveA,surface_list[j])
                #print intersection
                if intersection != None:
                    for x in intersection:
                        #check it's a line!
                        if rs.IsLine(intersection[0]):
                            length += rs.CurveLength(intersection[0])
            else: continue       
    print length 
    

if __name__ == "__main__":
    rs.EnableRedraw(False)
    
    rs.AddBox(corners)
    surface = AddCircle(n,radius,boxlength)
    
    #AddSeparatedCircle(n,radius,boxlength)
    #LengthOfIntersection(surface)
    #remove_surfaces_outside_of_box.RemoveSurfacesOutsideOfBox(boxlength)




    
               