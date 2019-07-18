import rhinoscriptsyntax as rs

def LengthOfIntersection(fracture_guid_list):
    length = 0
    for i in range(len(fracture_guid_list)):
        curveA = fracture_guid_list[i]
        for j in range(len(fracture_guid_list)):
            if j != i:
                #print "Comparing " + str(rs.ObjectType(curveA)) + " and " + str(rs.ObjectType(surface_list[j]))
                intersection = rs.IntersectBreps(curveA,fracture_guid_list[j])
                #print intersection
                if intersection != None:
                    for x in intersection:
                        #check it's a line!
                        if rs.IsLine(intersection[0]):
                            length += rs.CurveLength(intersection[0])
            else: continue       
    print length 
    
def FractureIntensity(fracture_guid_list, domain_length, domain_width, domain_height):
    fractures_surface_area = 0
    domain_volume = domain_length * domain_width * domain_height
    for fracture in fracture_guid_list:
        fracture_area = rs.SurfaceArea(fracture)
        fractures_surface_area += fracture_area
        
    return fractures_surface_area/domain_volume
 
def Intersections_per_unit_area(fracture_guid_list, domain_length, domain_width, domain_height):
    domain_surface_area = 2((domain_length * domain_width) + (domain_length * domain_height) + (domain_width * domain_height))
    return LengthOfIntersection(fracture_guid_list)/domain_surface_area

class CutPlane:
    def __init__(self, plane, width, height):
    #point 1 starts from [0,0,L], then clockwise for horizontal plane
    #point 1 starts from [0,L,M], then clockwise for vertical plane
    #self.point1 = point1 
    #self.point2 = point2
    #self.point3 = point3
    #self.point4 = point4
        self.plane = plane #plane should be in uppercase
        self.width = width
        self.height = height
    
    def draw_plane(self, dist, axis_of_rotation, angle_of_rotation):
        ##axis of rotation is a list 
        if self.plane == 'XY':
            myplane = rs.WorldXYPlane()
            rec = rs.AddRectangle(myplane, self.width, self.height)
            rs.MoveObject(rec, [0,0,dist]) #dist to move away from z-axis (origin)
            rs.RotateObject(rec, [self.height/2,self.width/2,dist], angle_of_rotation, axis_of_rotation)
            return rec
        if self.plane == 'YZ':
            myplane = rs.WorldYZPlane()
            rec = rs.AddRectangle(myplane, self.width, self.height)
            rs.MoveObject(rec, [dist, 0, 0]) #dist to move away from x-axis (origin)
            rs.RotateObject(rec, [dist,dist,self.height/2], angle_of_rotation, axis_of_rotation)
            return rec
        if self.plane == 'ZX':
            myplane = rs.WorldZXPlane()
            rec = rs.AddRectangle(myplane, self.width, self.height)
            rs.MoveObject(rec, [0, dist, 0]) #dist to move away from y-axis (origin)
            rs.RotateObject(rec, [dist,dist,self.height/2], angle_of_rotation, axis_of_rotation)
            return rec
        
    def length_of_fractures(self, fracture_guid_list, cut_plane):
        """
        Function to return the total length of fractures in the cut plane
        """
        length = 0
        plane_surf = rs.AddPlanarSrf(cut_plane)
        for i in range(len(fracture_guid_list)):
            intersection = rs.IntersectBreps(fracture_guid_list[i],plane_surf)
            #print intersection
            if intersection != None:
                for x in intersection:
                    #check it's a line!
                    if rs.IsLine(intersection[0]):
                        length += rs.CurveLength(intersection[0])    
        rs.DeleteObject(plane_surf)
        return length 
        
 
m = CutPlane('ZX', 20, 20.0)
plane = m.draw_plane(10,[0,1,0], 0)
#print(plane)
#print(rs.ObjectType(plane))