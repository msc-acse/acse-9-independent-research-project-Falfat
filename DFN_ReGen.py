# Falola Yusuf, Github: falfat
import random
import rhinoscriptsyntax as rs
import DFN_Gen
import Domain
import Frac
import math

rs.EnableRedraw(False)
path = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/fracture_data.txt"
def RedrawNetwork(path):
    # open text file
    m = open(path,'r')
    # read first line of text file; length of the domain
    l = m.readline()
    # convert length to float
    length = float(l)
    # read the second line of the domain; shape of the fracture
    shape = m.readline().split()
    #corners = ([(0,0,0),(length,0,0),(length,length,0),(0,length,0),(0,0,length),(length,0,length),(length,length,length),(0,length,length)])
    #rs.AddBox(corners)
    # create the domain
    dom = Domain.Domain(length)
    # display the domain
    dom.Show()
    if shape[0] != 'polygon':
        # a list to store GUIDs of regenerated fractures
        frac_list = [] 
        # list to store the x_axis of the fracture plane 
        x_axis = []
        # list to store the y_axis of the fracture plane
        y_axis = []
        # list to store the origin of the fracture location 
        origin = []
        # list to store the size of fracture
        size = []
        # read file line by line
        for line in m:
            # split line by comma
            words = line.split(",")
            #if words[0] != 'circle':
            # append the origin, x_axis and y_axis values in each line
            origin.append(float(words[0]))
            origin.append(float(words[1]))
            origin.append(float(words[2]))
            x_axis.append(float(words[3]))
            x_axis.append(float(words[4]))
            x_axis.append(float(words[5]))
            y_axis.append(float(words[6]))
            y_axis.append(float(words[7]))
            y_axis.append(float(words[8]))
            size.append(float((words[9])))
            # if the shape is ellipse, we have two radii, so append the second radius
            if shape[0] == 'ellipse':
                size.append(float((words[10])))
        # close file
        m.close()       
        # display fractures if they are circles/disks 
        if shape[0] == 'circle':
            n=0
            # go through the lists of origin, x_axis and y_axis
            # we divide by 3, because the list contains 3 consecutive values
            # representing a single origin, x_axis or y_axis
            for i in range(int(len(origin)/3)):
                # lists to store the origin, x_axis and y_axis of each fracture
                o = []
                x = []
                y = []
                # append the origin, x_axis and y_axis of each fracture
                for j in range(3):
                    o.append(origin[n+j])
                    x.append(x_axis[n+j])
                    y.append(y_axis[n+j])
                # convert the origin, x_axis and y_axis to a plane
                plane=rs.PlaneFromFrame(o,x,y)
                # name the current layer
                # we are creating layers so that we can trim out of bounds fractures
                # the function that does this makes use of the layer names
                layer_name = "FRACTURE_" + str(i+1)
                # give the layer a color
                rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
                # make layer the current layer
                rs.CurrentLayer(layer_name)
                # draw fracture
                my_disk = rs.AddCircle(plane,size[i])
                # convert to a surface
                surf = rs.AddPlanarSrf(my_disk)
                #delete initial fracture drawn which is a curve
                rs.DeleteObject(my_disk)
                # append fracture
                frac_list.append(surf)
                # increment n used for parsing
                n+=3 
            # trim out of bounds fractures 
            # the function all creates new fractures at the locations of all
            # exixting fractures
            dom.RemoveSurfacesOutsideOfBox(length) 
            # delete all old fractures
            for frac in frac_list:
                rs.DeleteObject(frac)
            dom_frac = dom.my_fractures #get the fractures in the domain
            #print(dom_frac)
            #swap old guids with new ones and put new guids in old frac layers
            #new_frac_guids = Frac.NewFracturesGuids(dom_frac,frac_list) 
        
        # display fractures if they are ellipse        
        if shape[0] == 'ellipse':
            # lists to store the origin, x_axis and y_axis of each fracture
            n=0
            p = 0
            q = 1
            # go through the lists of origin, x_axis and y_axis
            # we divide by 3, because the list contains 3 consecutive values
            # representing a single origin, x_axis or y_axis
            for i in range(int(len(origin)/3)):
                o = []
                x = []
                y = []
                # append the origin, x_axis and y_axis of each fracture
                for j in range(3):
                    o.append(origin[n+j])
                    x.append(x_axis[n+j])
                    y.append(y_axis[n+j])
                # convert the origin, x_axis and y_axis to a plane
                plane=rs.PlaneFromFrame(o,x,y)
                # name the current layer
                # we are creating layers so that we can trim out of bounds fractures
                # the function that does this makes use of the layer names
                layer_name = "FRACTURE_" + str(i+1)
                # give the layer a color
                rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
                # make layer current layer
                rs.CurrentLayer(layer_name)
                # draw fracture
                my_frac = rs.AddEllipse(plane,size[i+p], size[i+q])
                # convert to a surface from curve
                surf = rs.AddPlanarSrf(my_frac)
                # delete initial fracture drawn which is a curve
                rs.DeleteObject(my_frac)
                # append fracture
                frac_list.append(surf)
                # increment varaiables used for parsing
                n+=3 
                p+=1
                q+=1
            # trim out of bounds fractures     
            dom.RemoveSurfacesOutsideOfBox(length)
            # delete old fractures
            for frac in frac_list:
                rs.DeleteObject(frac)
            dom_frac = dom.my_fractures 
    
    if shape[0] == 'polygon':
        # list to store origin
        origin = []
        # list to store number of sides of each polygon
        size = []
        # list to store the x_axis of the fracture plane 
        x_axis = []
        # list to store the y_axis of the fracture plane
        y_axis = []
        # list to store fractures
        frac_list = []
        # list to store points
        points = []
        for line in m:
            # split each line by comma
            words = line.split(",")
            # store the number of sides of the polygon
            size.append(float(words[-1]))
            # store the x axis
            x_axis.extend((float(words[-7]),float(words[-6]),float(words[-5])))
            
            y_axis.extend((float(words[-4]),float(words[-3]),float(words[-2])))
            # store the origin
            origin.extend((float(words[-10]),float(words[-9]),float(words[-8])))
            # length of all points on the line
            # this will ensure we capture lines with disparate points when
            # generating polygon of different sides
            ex = int(3 * (size[-1]+1))
            # store all points on the line
            points.extend((words[:ex]))
        # close file
        m.close()
        
        # variables to use for parsing
        n = 0
        m = 0
        # iterate for the number of fractures generated
        for i in range(len(size)):
            # list to store points and origin
            o = []
            x = []
            y = []
            p = []
            # get the origin and axes of the fracture
            for j in range(3):
                o.append(origin[n+j])
                x.append(x_axis[n+j])
                y.append(y_axis[n+j])
            # variable for parsing
            r = 0
            # get the points of fracture edges
            for k in range(int(size[i])+1):
                p.append([])
                for l in range(3):
                    p[k].append(float(points[m+l+r]))
                # increment r
                r+=3
            # increment parsing variables
            m+=((int(size[i])+1)*3)
            n+=3
            # name the current layer
            # we are creating layers so that we can trim out of bounds fractures
            # the function that does this makes use of the layer names
            layer_name = "FRACTURE_" + str(i+1)
            # give the layer a color
            rs.AddLayer(layer_name,rs.CreateColor(0,255,0))
            # make layer the current layer
            rs.CurrentLayer(layer_name)
            # joing the points
            poly = rs.AddPolyline(p)
            # get the plane
            plane = rs.PlaneFromFrame(o,x,y)
            # transform fracture to the plane
            cob = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
            shear2d = rs.XformIdentity()
            shear2d[0,2] = math.tan(math.radians(45.0))
            cob_inverse = rs.XformChangeBasis(plane, rs.WorldXYPlane())
            temp = rs.XformMultiply(shear2d, cob)
            xform = rs.XformMultiply(cob_inverse, temp)
            frac = rs.TransformObjects(poly, xform, False )
            # convert to a surface
            surf = rs.AddPlanarSrf(frac)
            #delete initial fracture drawn which is a curve
            rs.DeleteObject(frac)
            frac_list.append(surf)
        # trim out of bounds fractures 
        # the function all creates new fractures at the locations of all
        # exixting fractures
        dom.RemoveSurfacesOutsideOfBox(length) 
        # delete all old fractures
        for fr in frac_list:
            rs.DeleteObject(fr)
        dom_frac = dom.my_fractures 
    return dom_frac 
    
if __name__ == "__main__":  
    rs.EnableRedraw(False)
    RedrawNetwork(path)