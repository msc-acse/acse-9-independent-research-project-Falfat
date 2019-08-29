# Falola Yusuf, Github: falfat
import rhinoscriptsyntax as rs
from imp import reload  # to reload modules
import math
import random
import Input
import StatInput
import Domain
import DFN_Analysis
from Frac import Fracture
from DFN_Analysis import CutPlane
from Matrix import Matrix
import scriptcontext as sc


data = "DataFile.txt"
radius, boxlength, n, fracture_shape = Input.ReadFile(data)
stat_data = "StatFile.txt"
orientation_dist, location_dist, size_dist = StatInput.ReadFile(stat_data)


# path to save text file
path = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/fracture_data.txt"
# open text file
file = open(path, 'w')
# write the domain length to file
file.write(str(boxlength))
# close file
file.close()

def GeneratePoint(boxlength):
    """
    Function to generate origin for fractures
    
    Parameter
    ---------
    boxlength: float
        domain size
    """
    # check the type of distribution specified
    if location_dist == 'uniform':
        x = random.uniform(0, boxlength)
        y = random.uniform(0, boxlength)
        z = random.uniform(0, boxlength)
        return [x, y, z]


def FractureSize(size_dist, radius_min, radius_max):
    """
    Function to determine size of fractures in case of random fractures
    generation
    
    Parameters
    ----------
    size_dist: str
        specified statistical distribution
    radius_min: float
        minimum radius for fractures
    radius_max: float
        maximum radius for fractures
        
    Raises
    ------
    ValueError
        if any of the radii is negative
    """
    try:
        if radius_min <= 0 or radius_max <= 0:
            raise ValueError
    except ValueError:
        print("FractureSize() The minimum and maximum radius should be greater than 0")
    else:
        # if uniform distribution is specified
        if size_dist == 'uniform':
            # dtdermine radius
            radius = random.uniform(radius_min, radius_max)
        if size_dist == 'exponential':
            pass
        # return radius
        return radius

    
def PolyOrientation(min_angle,max_angle):
    """
    function to dtermine angle of orientation for polygons
    
    min_angle: float
        minimum angle for fractures
    max_angle: float
        maximum angle for fractures 
    """
    return random.uniform(min_angle, max_angle)


def InclinePlane(origin, boxlength):
    """
    A function to get a plane for a circle, using its origin
    
    origin: list
        origin of the fracture
    boxlength: float
        domain lenght
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
            # find angles
            # we want to uniformly distributed points around a sphere
            theta_0 = 2*math.pi*random.uniform(0,1)
            theta_1 = math.acos(1-2*random.uniform(0,1))
            # determine the vectors
            vector = [boxlength*math.cos(theta_0),boxlength*math.sin(theta_0)*math.cos(theta_1),boxlength*math.sin(theta_0)*math.sin(theta_1)]
            # a loop to store the difference between the origin and vector
            for i in range(3):
                norm.append(vector[i] - origin[i])
            #xunitize the 3d vector
            normal = rs.VectorUnitize(norm)
            #xconvert the origin to a plane
            plane = rs.PlaneFromNormal(origin, normal)
            return plane
            
def FixedFractureGen(frac_num, aspect_ratio=None, sides=None):
    """
    A function to add a fixed number of circles in a cube. It also writes data
    to fracture data text file for regenerating fracture networks.
    
    Parameters
    ----------
    frac_num: int
        number of fractures to generate
    aspect_ratio: float
        aspect ratio for ellipse (Default:None)
    sides: int
        number of sides of polygon to generate (Default:None)
    """
    file = open(path, 'a')
    if fracture_shape == 'circle':
        # write the shape type
        file.write('\ncircle')
        # initialize a to store fractures
        fracture_list = []
        # a loop to insert the fixed number of fractures
        for i in range(frac_num):
            # layer name for the frcature
            layer_name = "FRACTURE_" + str(i+1)
            # create an istance of Fracture class
            frac = Fracture()
            # store fracture name
            frac.fracture_name = layer_name
            # generate origin for fracture
            origin = GeneratePoint(boxlength)
            # store farcture center
            frac.fracture_center = origin
            # convert the origin to a plane
            plane = InclinePlane(origin, boxlength)
            # add layer and color
            rs.AddLayer(layer_name, rs.CreateColor(0, 255, 0))
            # make current layer
            rs.CurrentLayer(layer_name)
            # insert the fracture in the domain
            my_circle = rs.AddCircle(plane, radius)
            # write the plane and radius to file for re-plotting
            file.write("\n" + str(plane[0]) + "," +  str(plane[1]) + "," +  str(plane[2]) + "," + str(radius))
            # circle_list.append(my_circle)
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
        # write the shape type
        file.write('\nellipse')
        for i in range(frac_num):
            # layer name for the frcature
            layer_name = "FRACTURE_" + str(i+1)
            # create an istance of Fracture class
            frac = Fracture()
            frac.fracture_name = layer_name
            # generate fracture origin
            origin = GeneratePoint(boxlength)
            frac.fracture_center = origin
            # plane for fracture
            plane = InclinePlane(origin, boxlength)
            # calculate r_y
            ry = radius/aspect_ratio
            # create layer for fracture
            rs.AddLayer(layer_name, rs.CreateColor(0, 255, 0))
            rs.CurrentLayer(layer_name)
            # draw ellipse
            fracture = rs.AddEllipse(plane, radius, ry)
            # write the plane, r_x and r_y to file for re-plotting
            file.write("\n" + str(plane[0])+","+str(plane[1])+","+str(plane[2])+","+str(radius)+","+str(ry))
            # make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            # delete initial fracture drawn which is a curve
            rs.DeleteObject(fracture)
            # set fracture guid into its objects
            frac.fracture_GUID = frac_surf[0]
            # append fracture into fracture list
            fracture_list.append(frac)
        
    elif fracture_shape == 'polygon':
        # list to store fracture surface GUIDs
        fracture_list = []
        # write the shape type
        file.write('\npolygon\n')
        for i in range(frac_num):
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
            # create a 3D point object which isn't visible
            # to the rhino document
            pt_01 = rs.coerce3dvector([radius+origin[0], origin[1], origin[2]])
            # empty list to store all points
            points = []
            # a rotation axis
            ax = rs.coerce3dvector([0, 0, 1])
            # loop to generate points for polygon vertices
            # file.write("\n")
            for j in range(sides):
                # rotation transform with rotation from the origin
                trans = rs.XformRotation2(theta_deg*j, ax, origin)
                # transform the original 3D point and append to list
                points.append(rs.PointTransform(pt_01, trans))
                # write to file
                if j == 0:
                    file.write(str(rs.PointTransform(pt_01, trans)[0])+","+str(rs.PointTransform(pt_01, trans)[1])+","+str(rs.PointTransform(pt_01, trans)[2])+",")
                if j != 0:
                    file.write(str(rs.PointTransform(pt_01, trans)[0])+","+str(rs.PointTransform(pt_01, trans)[1])+","+str(rs.PointTransform(pt_01, trans)[2])+",")
            # append the initial point to close the polygon
            points.append(pt_01)
            # write data to file
            file.write(str(pt_01[0])+","+str(pt_01[1])+","+str(pt_01[2])+",")
            # create layer for fracture
            # layer_name = "FRACTURE_" + str(i+1)
            rs.AddLayer(layer_name, rs.CreateColor(0, 255, 0))
            rs.CurrentLayer(layer_name)
            # get GUID of created polygon
            polygon = rs.AddPolyline(points)
            # get the plane
            plane = InclinePlane(origin, boxlength)
            # transform the polygon to the plane
            cob = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
            shear2d = rs.XformIdentity()
            shear2d[0,2] = math.tan(math.radians(45.0))
            cob_inverse = rs.XformChangeBasis(plane, rs.WorldXYPlane())
            temp = rs.XformMultiply(shear2d, cob)
            xform = rs.XformMultiply(cob_inverse, temp)
            fracture = rs.TransformObjects(polygon, xform, False )
            # write data to file for regeneration
            file.write(str(plane[0])+","+str(plane[1])+","+str(plane[2])+","+str(sides)+"\n")
            # make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            # delete initial fracture drawn which is a curve
            rs.DeleteObject(fracture)
            # set fracture guid into its objects
            frac.fracture_GUID = frac_surf[0]
            # append GUID into list
            fracture_list.append(frac)
    # close file
    file.close()
    # return racture list
    return fracture_list


def RandomFractureGen(frac_min, frac_max, radius_min, radius_max,
                      aspect_min=None, aspect_max=None, polysize_min=None,
                      polysize_max=None):
    """
    Funtions to generate fractures of random number and sizes
    
    Parameters
    ----------
    frac_min: int
        minimum number of fractures to generate
    frac_max: int
        maximum number of fractures to generate
    radius_min: float
        minimum size of fractures
    radius_max: float
        maximum number of fractures to generate
    aspect_min: float
        minimum aspect ratio fpr ellipses (Default:None)
    aspect_max: float
        maximum aspect ratio fpr ellipses (Default:None)
    polysize_min: int
        minimum size of polygon (Default:None)
    polysize_max: int
        maximum size of polygon (Default:None)
    """
    # randomly determine the number of fractures to generate
    num_frac = random.randint(frac_min, frac_max)
    # open file and append to it
    file = open(path, 'a')
    if fracture_shape == 'circle':
        # write the shape type
        file.write('\ncircle')
        # initialize list to store fractures
        fracture_list = []
        # loop to generate fractures
        for i in range(num_frac):
            # name the layer
            layer_name = "FRACTURE_" + str(i+1)
            # an instance of fracture object
            frac = Fracture()
            # get fracture name
            frac.fracture_name = layer_name
            # generate fracture center
            origin = GeneratePoint(boxlength)
            # store fracture center
            frac.fracture_center = origin
            # convert the origin to a plane
            plane = InclinePlane(origin, boxlength)
            # add layer and create color for it
            rs.AddLayer(layer_name, rs.CreateColor(0, 255, 0))
            # make layer current layer
            rs.CurrentLayer(layer_name)
            # generate fracture size
            radius = FractureSize(size_dist, radius_min, radius_max)
            # insert the circle in the domain
            my_circle = rs.AddCircle(plane, radius)
            # write the plane and radius to file for re-plotting
            file.write("\n" + str(plane[0]) + "," + str(plane[1]) + "," + str(plane[2]) + "," + str(radius))
            surf = rs.AddPlanarSrf(my_circle)
            # delete initial fracture drawn which is a curve
            rs.DeleteObject(my_circle)
            # set fracture guid into its object
            frac.fracture_GUID = surf[0]
            fracture_list.append(frac)
            
    elif fracture_shape == 'ellipse':
        # initialize list to store fractures
        fracture_list = []
        # write the shape type
        file.write('\nellipse')
        for i in range(num_frac):
            # name the layer
            layer_name = "FRACTURE_" + str(i+1)
            # an instance of fracture object
            frac = Fracture()
            # get fracture name
            frac.fracture_name = layer_name
            # generate fracture center
            origin = GeneratePoint(boxlength)
            # store fracture center
            frac.fracture_center = origin
            # plane for fracture
            plane = InclinePlane(origin, boxlength)
            # randomly generate radius(rx)
            radius = FractureSize(size_dist, radius_min, radius_max)
            # randomly generate aspect ratio
            aspect_ratio = random.randint(aspect_min, aspect_max)
            # calculate r_y
            ry = radius/aspect_ratio
            # add layer with color
            rs.AddLayer(layer_name, rs.CreateColor(0, 255, 0))
            # make current layer
            rs.CurrentLayer(layer_name)
            # draw fracture
            fracture = rs.AddEllipse(plane, radius, ry)
            # write the plane, r_x and r_y to file for re-plotting
            file.write("\n" + str(plane[0]) + "," + str(plane[1]) + "," + str(plane[2]) + "," + str(radius) + ","+ str(ry))
            # make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            # delete initial fracture drawn which is a curve
            rs.DeleteObject(fracture)
            # set fracture guid into its object
            frac.fracture_GUID = frac_surf[0]
            # append fracture guid to list
            fracture_list.append(frac)

    elif fracture_shape == 'polygon':
        # initialize list to store fractures
        fracture_list = []
        # write the shape type
        file.write('\npolygon\n')
        for i in range(num_frac):
            # name the layer
            layer_name = "FRACTURE" + str(i+1)
            # an instance of fracture class
            frac = Fracture()
            # get farcture name
            frac.fracture_name = layer_name
            # randomly determine the sides of the polygon
            sides = random.randint(polysize_min, polysize_max)
            # theta in radian
            theta_rad = (2*math.pi)/sides
            # theta in degree (interior angles)
            theta_deg = theta_rad*(180/math.pi)
            # generate origin
            origin = GeneratePoint(boxlength)
            # save fracture center
            frac.fracture_center = origin
            # randomly generate radius(rx)
            radius = FractureSize(size_dist, radius_min, radius_max)
            # create a 3D point object which isn't visible to the rhino document
            pt_01 = rs.coerce3dvector([radius+origin[0], origin[1], origin[2]])
            # empty list to store all points
            points = []
            # a rotation axis 
            ax = rs.coerce3dvector([0, 0, 1])
            # loop to generate points for polygon vertices
            for j in range(sides):
                # rotation transform with rotation from the origin
                trans = rs.XformRotation2(theta_deg*j, ax, origin)
                # transform the original 3D point and append to list
                points.append(rs.PointTransform(pt_01,trans))
                if j == 0:
                    file.write(str(rs.PointTransform(pt_01,trans)[0]) + "," + str(rs.PointTransform(pt_01,trans)[1]) +  "," + str(rs.PointTransform(pt_01,trans)[2])+  ",")
                if j != 0:
                    file.write(str(rs.PointTransform(pt_01,trans)[0]) + "," + str(rs.PointTransform(pt_01,trans)[1]) +  "," + str(rs.PointTransform(pt_01,trans)[2])+ ",")
            # append the initial point to close the polygon
            points.append(pt_01)
            file.write(str(pt_01[0]) + "," + str(pt_01[1]) + "," + str(pt_01[2])+ ",")
            # create layer for fracture
            layer_name = "FRACTURE_" + str(i+1)
            rs.AddLayer(layer_name, rs.CreateColor(0, 255, 0))
            rs.CurrentLayer(layer_name)
            # get GUID of created polygon
            polygon = rs.AddPolyline(points)
            # get the plane
            plane = InclinePlane(origin, boxlength)
            # transform the polygon to the plane
            cob = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
            shear2d = rs.XformIdentity()
            shear2d[0,2] = math.tan(math.radians(45.0))
            cob_inverse = rs.XformChangeBasis(plane, rs.WorldXYPlane())
            temp = rs.XformMultiply(shear2d, cob)
            xform = rs.XformMultiply(cob_inverse, temp)
            fracture = rs.TransformObjects(polygon, xform, False )
            # write to file
            #file.write(str(origin[0]) + "," + str(origin[1]) + "," + str(origin[2])+ "," )
            file.write(str(plane[0]) + "," + str(plane[1]) + "," + str(plane[2]) + "," + str(sides) + "\n")
            # make fracture a surface
            frac_surf = rs.AddPlanarSrf(fracture)
            # delete initial fracture drawn which is a curve
            rs.DeleteObject(fracture)
            # set fracture guid into its objects
            frac.fracture_GUID = frac_surf[0]
            # append fracture guid to list
            fracture_list.append(frac)
    # close file
    file.close()
    return fracture_list


def SeparatedFractureGen(threshold=None, aspect_ratio=None, min_angle=None,
                         max_angle=None, sides=None):
    """
    Function to generate fractures separated by a minimum threshold.
    
    Parameters
    ----------
    threshold: float
        the minimum amount of separations betwen fractures
    min_angle: float
        minimum angle of rotation for polygon (Default:None)
    max_angle: float
        maximum angle of rotation for polygon (Default:None)
    aspect_ratio: flaot
        aspect ratio for ellipses
    sides: int
        number of sides for polygon
    """
    if fracture_shape == 'circle':
        # Generate a single fracture to initiate the comparism
        # layer name for the frcature
        layer_name = "FRACTURE_1"
        # create an istance of Fracture class
        frac = Fracture()
        # store fracture name
        frac.fracture_name = layer_name
        # generate origin for fracture
        origin = GeneratePoint(boxlength)
        # store farcture center
        frac.fracture_center = origin
        # convert the origin to a plane
        plane = InclinePlane(origin, boxlength)
        # add layer and color
        rs.AddLayer(layer_name, rs.CreateColor(0, 255, 0))
        # make current layer
        rs.CurrentLayer(layer_name)
        # insert the fracture in the domain
        my_circle = rs.AddCircle(plane, radius)
        # circle_list.append(my_circle)
        surf = rs.AddPlanarSrf(my_circle)
        # save fracture's GUID
        frac.fracture_GUID = surf[0]
        # append fracture into fracture list
        fracture_list = [frac]
        nfrac = 1
        k = 0
        while nfrac < n:
            # generate origin for fracture
            origin = GeneratePoint(boxlength)
            good_location = True
            for fracture in fracture_list:
                p = fracture.fracture_center
                dist = rs.Distance(p, origin)
                if dist <= threshold:
                    good_location = False
                    break
            if good_location:
                # layer name for the frcature
                layer_name = "FRACTURE_" + str(k+2)
                # create an istance of Fracture class
                frac = Fracture()
                # store fracture name
                frac.fracture_name = layer_name
                # generate origin for fracture
                origin = GeneratePoint(boxlength)
                # store farcture center
                frac.fracture_center = origin
                # convert the origin to a plane
                plane = InclinePlane(origin, boxlength)
                # add layer and color
                rs.AddLayer(layer_name, rs.CreateColor(0, 255, 0))
                # make current layer
                rs.CurrentLayer(layer_name)
                # insert the fracture in the domain
                my_circle = rs.AddCircle(plane, radius)
                # circle_list.append(my_circle)
                surf = rs.AddPlanarSrf(my_circle)
                # save fracture's GUID
                frac.fracture_GUID = surf[0]
                # append fracture into fracture list
                fracture_list.append(frac)
                nfrac += 1
                k += 1
    # return list of fractures
    return fracture_list

if __name__ == "__main__":  
    # sc.doc.Objects.Clear() 
    rs.EnableRedraw(False)  # Avoid drawing whilst computing
    # reload(Frac)
    # reload(Domain)
    # reload(DFN_Analysis)
    # reload(Frac)
    # reload(Domain)
    dom = Domain.Domain(boxlength)
    dom.Show()
    #frac_list = FixedFractureGen(n,0,4)
    f = RandomFractureGen(10,11,2,4,0,0,4,5)
    # FixedFractureGen(n,aspect_ratio=2,min_angle=0,max_angle =360, sides =5)
    # frac_list = RandomFractureGen(20, 30, 1, 3,1,4, 4, 7)
#    # print(Domain.fractures)
#    # print(type(frac_list))
#    # frac_list = SeparatedFractureGen()
#    frac_guids = Frac.old_fracture_guids(frac_list)
#    # print('len is :', len(frac_guids))
#    for frac in frac_guids:
#        dom.add_fracture(frac)
#    print(dom.fractures)
#    # print(dom.number_of_fractures())
#    # print('box length is', dom.length)
#    dom.RemoveSurfacesOutsideOfBox(dom.length)
#    dom_frac = dom.my_fractures
#    print(dom_frac)
#    new_frac_guids = Frac.new_fracture_guids(dom_frac,frac_list)
#    ##print(new_frac_guids)
#    ##print(rs.ObjectType(frac_list[1].fracture_GUID))
#    #sec.LengthOfIntersection(frac_guids)
#    #dom.number_of_fractures(frac_list)
#    #print(num)
#    #print(frac_list[0].fracture_name)
    # frac_list[0].intersect(frac_list[7])
# #cut plane analysis 
#    m = CutPlane('YZ', 20, 20.0)
#    plane = m.draw_plane(10,[0,1,0], 30)
#    k = m.length_of_fractures(new_frac_guids, plane)
#    print("cut plane length is:", k)
#    inter_frac = m.intersecting_fractures
#    #print(m.GUID)
#    lines = m.Plane_lines(m.GUID)
#    mat = m.IntersectionMatrix(lines,inter_frac)
#    print(mat)
#    #a = m.number_of_intersecting_fractures()
#    #print(a)
#    #b = m.FractureIntensity_P21(k)
#    #print("P21 is:", b)
#    boundary_list = dom.CreateBoundary(20)


# #3D percolation Analysis
    # k = dom.IntersectionMatrix(boundary_list,new_frac_guids)
    # print(k)
    # per = dom.Percolate(boundary_list[0], boundary_list[1], boundary_list,
#                        k,new_frac_guids)
    # print(per)
    # m = Matrix(k)
    # m.PrintMatrix()
    # m.MatrixToFile()
