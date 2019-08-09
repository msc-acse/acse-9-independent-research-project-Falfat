import rhinoscriptsyntax as rs


class IntersectionAnalysis:
    no_of_fracture_intersections = 0 #should be run after lengthofinter
    lengths_of_intersection_lines = [] #plot histogram with this
    
    def LengthOfIntersection(self, fracture_guid_list):
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
                                #increase no of fracture intersections
                                self.no_of_fracture_intersections += 1
                                self.lengths_of_intersection_lines.append(rs.CurveLength(intersection[0]))
                                length += rs.CurveLength(intersection[0])
                else: continue       
        print length 
    
    def FracturesSurfaceArea(self, fracture_guid_list):
        # function to determine the surface area of all fractures in the domain
        # initialise fracturs surface area
        fractures_surface_area = 0
        #loop to sum all areas of fractures
        for fracture in fracture_guid_list:
            #get surface area of the fracture
            fracture_area = rs.SurfaceArea(fracture)
            # increment the fractures surface area
            fractures_surface_area += fracture_area[0]
        return fractures_surface_area
        
    def FractureIntensity_P32(self, fracture_guid_list, domain_length, domain_width, domain_height):
        #fractures_surface_area = 0
        domain_volume = domain_length * domain_width * domain_height
#        for fracture in fracture_guid_list:
#            fracture_area = rs.SurfaceArea(fracture)
#            fractures_surface_area += fracture_area
        # determine fractures surface area
        fractures_surface_area = self.FracturesSurfaceArea(fracture_guid_list)    
        return fractures_surface_area/domain_volume
     
    def Intersections_per_unit_area(self, fracture_guid_list, domain_length, domain_width, domain_height):
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
        self.GUID = None
        self.intersecting_fractures = []
    
    def draw_plane(self, dist, axis_of_rotation, angle_of_rotation):
        ##axis of rotation is a list 
        if self.plane == 'XY':
            #axis for plane to be drawn
            myplane = rs.WorldXYPlane()
            #add a rectangele in the XY plane
            rec = rs.AddRectangle(myplane, self.width, self.height)
            #save the GUID of the plane
            self.GUID = rec
            #move the plane "dist" away from the z-axis
            rs.MoveObject(rec, [0,0,dist]) #dist to move away from z-axis (origin)
            #rotate plane
            rs.RotateObject(rec, [self.height/2,self.width/2,dist], angle_of_rotation, axis_of_rotation)
            #return the GUID of the plane
            return rec
        if self.plane == 'YZ':
            myplane = rs.WorldYZPlane()
            rec = rs.AddRectangle(myplane, self.width, self.height)
            self.GUID = rec
            rs.MoveObject(rec, [dist, 0, 0]) #dist to move away from x-axis (origin)
            rs.RotateObject(rec, [dist,dist,self.height/2], angle_of_rotation, axis_of_rotation)
            return rec
        if self.plane == 'ZX':
            myplane = rs.WorldZXPlane()
            rec = rs.AddRectangle(myplane, self.width, self.height)
            self.GUID = rec
            rs.MoveObject(rec, [0, dist, 0]) #dist to move away from y-axis (origin)
            rs.RotateObject(rec, [dist,dist,self.height/2], angle_of_rotation, axis_of_rotation)
            return rec
        
    def length_of_fractures(self, fracture_guid_list, cut_plane):
        """
        Function to intersect fractures and return the total length of fractures in the cut plane
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
                        self.intersecting_fractures.append(intersection[0])
                        length += rs.CurveLength(intersection[0])    
        rs.DeleteObject(plane_surf)
        return length 
    
    def number_of_intersecting_fractures(self):
        return len(self.intersecting_fractures)
        
    def FractureIntensity_P21(self, length_of_fractures):
        return length_of_fractures/(self.width * self.height)
    
    def Plane_lines(self, plane_guid):
        ##returns a list of the four lines forming the plane
        return rs.ExplodeCurves(plane_guid)
        
    def IntersectionMatrix(self, boundary_list, intersected_fractures):
        #initialize Matrix
        mat = []
        #number of fractures
        num_frac = len(intersected_fractures)
        #number of rows and cols for matrix 
        n_row = num_frac + 4
        n_col = num_frac + 4
        #initialize matrix
        for i in range(n_row):
            mat.append([])
            for j in range(n_col):
                mat[i].append(j)
                mat[i][j] = 0
        #boundary to bounday taken care by the matrix initialization
        #fractures to fractures
        for i in range(num_frac):
            for j in range(num_frac):
                if i != j:
                    intersection = rs.CurveCurveIntersection(intersected_fractures[i],intersected_fractures[j])
                    if intersection is not None:
                        mat[i][j] = 1 
        #boundary-fractures
        for i in range(num_frac): #0 to number of fractures - 1
            for j in range(num_frac, n_col): #number of fractures to end of row/col
                intersection = rs.CurveCurveIntersection(intersected_fractures[i],boundary_list[j-num_frac])
                if intersection is not None:
                    mat[i][j] = 1
                    mat[j][i] = 1
        
        return mat

def Intersections_per_fracture(intersection_matrix):
    ## function to save the number of intersections per fracture in a file
    # change directory, so as to save text file in the designated folder
    os.chdir("/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files")
    # open text file to store all lengths of intersection for post processing 
    file = open("intersections_per_fracture.txt", 'w')
    # go through each row of the matrix
    for i in range(len(intersection_matrix)):
        #cinitialise number of intersection to be 0
        n = 0
        # go through all the columns of each row
        # avoid the last six elements, since they are boundary intersections
        for j in range(len(intersection_matrix[i][:-6])):
            #if the element is not 0, i.e it's an intersection
            if intersection_matrix[i][j] != 0:
                # increment the number of intersection
                n+=1
        # avoid space before the first integer
        # write to file
        if i != 0:
            file.write(" " + str(n))
        else:
            file.write(str(n))
    # close file
    file.close()
    return  None
            


#print(plane)
#print(rs.ObjectType(plane))