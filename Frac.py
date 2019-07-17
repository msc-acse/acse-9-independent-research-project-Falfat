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
#        self.shape = shape
#        self.orientation_distribution = orientation_distribution
#        self.location_distribution = location_distribution
        
