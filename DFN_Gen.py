import rhinoscriptsyntax as rs
import math
import random
import input
import sec
from Domain import Domain 
from Frac import Fracture

#import rhinoscriptsyntax as rs
#import math
#import random
#import input
#import sec
#import Domain
#from Frac import Fracture

name = "DataFile.txt"
radius, boxlength, n, orientation_dist, location_dist, fracture_shape = input.ReadFile(name)
#radius, boxlength, n, orientation_dist, location_dist, fracture_shape = input.ReadFile(name)
size_dist = 'uniform'
min_angle,max_angle = 0,3360


def generate_point(boxlength):
    if location_dist == 'uniform':
        x = random.uniform(0,boxlength)
        y = random.uniform(0,boxlength)   
        z = random.uniform(0,boxlength)
        return [x,y,z]
    
def fracture_size(size_dist,radius_min, radius_max):
    if size_dist == 'uniform':
        radius = random.uniform(radius_min, radius_max)
        
    return radius
    
def poly_orientation(min_angle,max_angle):
    return random.randint(min_angle,max_angle)
    
def InclinePlane(origin):
    """
    A function to get a plane for a circle, using its origin
    """
    if orientation_dist == 'uniform':
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
        
def FixedFractureGen(aspect_ratio=None,min_angle=None,max_angle=None,sides=None):
    """
    A function to add a fixed number of circles in a cube
    """
    if fracture_shape == 'circle':
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
            origin = generate_point(boxlength)
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
            #circle_list.append(my_circle)
            surf = rs.AddPlanarSrf(my_circle)
            #save fracture's GUID
            frac.fracture_GUID = surf[0]
            #append fracture into fracture list
            fracture_list.append(frac)
            
            
    elif fracture_shape == 'ellipse':
        #list to store fracture surface GUIDs
        fracture_list = []
        for i in range(n):
            layer_name = "FRACTURE_" + str(i+1)
            
            frac = Fracture()
            frac.fracture_name = layer_name
            #generate fracture origin
            origin = generate_point(boxlength)
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
            #make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            #append surface GUID to list of fracture surfaces
            frac.fracture_GUID = frac_surf[0]
            fracture_list.append(frac)
        
    elif fracture_shape == 'polygon':
            #list to store fracture surface GUIDs
        fracture_list = []
        for i in range(n):
            layer_name = "FRACTURE" + str(i+1)
            frac = Fracture()
            frac.fracture_name = layer_name
            #theta in radian
            theta_rad = (2*math.pi)/sides
            #theta in degree (interior angles)
            theta_deg = theta_rad*(180/math.pi)
            #generate origin
            origin = generate_point(boxlength)
            frac.fracture_center = origin
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
            layer_name = "FRACTURE_" + str(i+1)
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            rs.CurrentLayer(layer_name)
            #get GUID of created polygon
            polygon = rs.AddPolyline(points)
            #create an angle of rotation
            angle = random.randint(min_angle,max_angle)
            #rotate polygon about y-axis
            fracture = rs.RotateObject(polygon,origin,angle,[0,1,0])
            #make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            frac.fracture_GUID = frac_surf[0]
            fracture_list.append(frac)
            
    return fracture_list
 
def RandomFractureGen(frac_min, frac_max, radius_min, radius_max,aspect_min=None, aspect_max=None, polysize_min = None, polysize_max = None):
    #randomly determine the number of fractures to generate
    num_frac = random.randint(frac_min, frac_max)
    if fracture_shape == 'circle':
        #initialize list to store fractures
        fracture_list = []
        #loop to generate fractures
        for i in range(num_frac):
            #name the layer
            layer_name = "FRACTURE_" + str(i+1)
            #an instance of fracture object
            frac = Fracture()
            #get fracture name
            frac.fracture_name = layer_name
            #generate fracture center
            origin = generate_point(boxlength)
            #store fracture center
            frac.fracture_center = origin
            #convert the origin to a plane
            plane = InclinePlane(origin)
            #add layer and create color for it
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            #make layer current layer
            rs.CurrentLayer(layer_name)
            #generate fracture size
            radius = fracture_size(size_dist,radius_min, radius_max)
            #insert the circle in the domain
            my_circle = rs.AddCircle(plane,radius)
            #append the circle GUID to the list
            #circle_list.append(my_circle)
            surf = rs.AddPlanarSrf(my_circle)
            #surface_list.append(surf[0])
            frac.fracture_GUID = surf[0]
            fracture_list.append(frac)
            
    elif fracture_shape == 'ellipse':
        #initialize list to store fractures
        fracture_list = []
        for i in range(num_frac):
            #name the layer
            layer_name = "FRACTURE_" + str(i+1)
            #an instance of fracture object
            frac = Fracture()
            #get fracture name
            frac.fracture_name = layer_name
            #generate fracture center
            origin = generate_point(boxlength)
            #store fracture center
            frac.fracture_center = origin
            #plane for fracture
            plane = InclinePlane(origin)
            #randomly generate radius(rx)
            radius = fracture_size(size_dist,radius_min, radius_max)
            #randomly generate aspect ratio
            aspect_ratio = random.randint(aspect_min,aspect_max)
            #calculate r_y
            ry = radius/aspect_ratio
            #add layer with color
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            #make current layer
            rs.CurrentLayer(layer_name)
            #draw fracture
            fracture = rs.AddEllipse(plane,radius, ry)
            #make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            #append surface GUID to list of fracture surfaces
            frac.fracture_GUID = frac_surf[0]
            fracture_list.append(frac) 
            
    elif fracture_shape == 'polygon':
        #initialize list to store fractures
        fracture_list = []
        for i in range(n):
            #name the layer
            layer_name = "FRACTURE" + str(i+1)
            #an instance of fracture class
            frac = Fracture()
            #get farcture name
            frac.fracture_name = layer_name
            #randomly determine the sides of the polygon
            sides = random.randint(polysize_min,polysize_max)
            #theta in radian
            theta_rad = (2*math.pi)/sides
            #theta in degree (interior angles)
            theta_deg = theta_rad*(180/math.pi)
            #generate origin
            origin = generate_point(boxlength)
            #save fracture center
            frac.fracture_center = origin
            #randomly generate radius(rx)
            radius = fracture_size(size_dist,radius_min, radius_max)
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
            layer_name = "FRACTURE_" + str(i+1)
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            rs.CurrentLayer(layer_name)
            #get GUID of created polygon
            polygon = rs.AddPolyline(points)
            #create an angle of rotation
            angle = poly_orientation(min_angle,max_angle)
            #rotate polygon about y-axis
            fracture = rs.RotateObject(polygon,origin,angle,[0,1,0])
            #make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            frac.fracture_GUID = frac_surf[0]
            fracture_list.append(frac)
        
            
    return fracture_list 
 
def fracture_guids(fracture_list):
    list = []
    for i in range(len(fracture_list)):
        list.append(fracture_list[i].fracture_GUID)
    return list
    
def SeparatedFractureGen(threshold=None, aspect_ratio=None, min_angle=None, max_angle=None, sides=None):
    if fracture_shape == 'circle':
        ###########                                ###########
        #Generate a single fracture to initiate the comparism#
        ###########                                ###########
        #layer name for the frcature
        layer_name = "FRACTURE_1" 
        #create an istance of Fracture class
        frac = Fracture()
        #store fracture name
        frac.fracture_name = layer_name
        #generate origin for fracture
        origin = generate_point(boxlength)
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
        #circle_list.append(my_circle)
        surf = rs.AddPlanarSrf(my_circle)
        #save fracture's GUID
        frac.fracture_GUID = surf[0]
        #append fracture into fracture list
        fracture_list = [frac]
        
        nfrac = 1
        k = 0
        while nfrac < n:
            #generate origin for fracture
            origin = generate_point(boxlength)
            good_location = True
            for fracture in fracture_list:
                p = fracture.fracture_center
                dist = rs.Distance(p,origin)
                if dist <= threshold:
                    good_location = False
                    break
            if good_location:
                #layer name for the frcature
                layer_name = "FRACTURE_" + str(k+2)
                #create an istance of Fracture class
                frac = Fracture()
                #store fracture name
                frac.fracture_name = layer_name
                #generate origin for fracture
                origin = generate_point(boxlength)
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
                #circle_list.append(my_circle)
                surf = rs.AddPlanarSrf(my_circle)
                #save fracture's GUID
                frac.fracture_GUID = surf[0]
                #append fracture into fracture list
                fracture_list.append(frac)
                nfrac+=1
                k+=1
            
    return fracture_list    
    
if __name__ == "__main__":   
    rs.EnableRedraw(False) #Avoid drawing whilst computing 
    dom = Domain(boxlength)
    dom.show()
    #frac_list = FixedFractureGen(min_angle=5,max_angle =300, sides =5)
    frac_list = RandomFractureGen(20, 30, 1, 3,1,4, 4, 7)
    #print(Domain.fractures)
    #print(type(frac_list))
    #frac_list = SeparatedFractureGen()
    frac_guids = fracture_guids(frac_list)
    print('len is :', len(frac_guids))
    for frac in frac_guids:
        dom.add_fracture(frac)
    print(dom.fractures)
    print(dom.number_of_fractures())
    #print('box length is', dom.length)
    dom.RemoveSurfacesOutsideOfBox(dom.length)
    print(dom.my_fractures)
    #sec.LengthOfIntersection(frac_guids)
    #dom.number_of_fractures(frac_list)
    #print(num)
    #print(frac_list[0].fracture_name)
    
    #frac_list[0].intersect(frac_list[7])