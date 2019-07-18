import rhinoscriptsyntax as rs
#import typing as typ
#import math
#import random



class Fracture():
    fracture_name = None
    fracture_GUID = None
    fracture_center = None
   #def __init__(self):
        #pass
    def intersect(self, other):
        #inputs are frcature instances in fracture list
        curveA = self.fracture_GUID
        intersection = rs.IntersectBreps(curveA,other.fracture_GUID)
        if intersection == None:
            print('The fractures do not intersect')
        else:
           for x in intersection:
                #check it's a line!
                if rs.IsLine(intersection[0]):
                    length = rs.CurveLength(intersection[0])
                    print('Fracture intersect, the length of intersection is:', length)
                    
def old_fracture_guids(fracture_list):
    #initialize a list to store the GUIDs
    list = []
    #go through the fracture list containing instances of fracture class
    for i in range(len(fracture_list)):
        #store the GUID in each instance
        list.append(fracture_list[i].fracture_GUID)
    return list
    
    
def new_fracture_guids(dom_new_fractures, fracture_list):
    ##function to swap old guids to new ones and return new guids
    #deletes previous fractures and swap the layers of new fractures
    #with those of old ones
    guids = []
    for i in range(len(fracture_list)):
        #delete previous fractures
        rs.DeleteObject(fracture_list[i].fracture_GUID)
        #change the guid of our fracture instances
        fracture_list[i].fracture_GUID = dom_new_fractures[i]
        guids.append(dom_new_fractures[i])
        #put new fractures in old layers
        rs.ObjectLayer(dom_new_fractures[i],fracture_list[i].fracture_name)
    return guids
#        self.shape = shape
#        self.orientation_distribution = orientation_distribution
#        self.location_distribution = location_distribution
        
