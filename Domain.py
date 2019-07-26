import rhinoscriptsyntax as  rs
import random
import math
#import remove_surfaces_outside_of_box
import input


#radius = 2
#boxlength = 20

name = "DataFile.txt"
radius, boxlength, n, orientation_dist, location_dist, fracture_shape = input.ReadFile(name)

class Domain:
    def __init__(self, length):
        self.length = length
        self.surface_area = 6*length**2
        self.volume = length**3
        self.type = 'cube'
        self.center = [length/2,length/2,length/2]
        self.fractures = []
        self.my_fractures = []
#        self.boundary_list = []
#        self.boundary_1 = None
#        self.boundary_2 = None
#        self.boundary_3 = None
#        self.boundary_4 = None  
#        self.boundary_5 = None
#        self.boundary_6 = None
        
    def show(self):
        corners = ([(0,0,0),(self.length,0,0),(self.length,self.length,0),(0,self.length,0),(0,0,self.length),(self.length,0,self.length),(self.length,self.length,self.length),(0,self.length,self.length)])
        return rs.AddBox(corners)
        
    def number_of_fractures(self):
        #print('number of fractures is:',len(fracture_list))
        return len(self.fractures)
        
    def boundary_guids(self):
        pass
        
    def add_fracture(self, frac):
        self.fractures.append(frac)
    
    #def new_fractures(self
        
    def CreateBoundary(self, box_side_length):
        try:
            if box_side_length <= 0:
                raise ValueError
        except ValueError:
            print("The box side length should be greater than 0")
        else:
            #Put boundary layers in a new layer
            boundary_layer_name = "Boundaries"
            
            #To make sure we do not overwrite existing boundary surfaces,
            #delete the old layer if it is there
            
            #To avoid error messages about deleting current layers:
            rs.AddLayer('Blank Layer')
            rs.CurrentLayer('Blank Layer')
            
            if rs.IsLayer(boundary_layer_name):
                rs.PurgeLayer(boundary_layer_name) #Deletes layer
            
            rs.AddLayer(boundary_layer_name)
            rs.CurrentLayer(boundary_layer_name)
            rs.LayerColor(boundary_layer_name, [0,0,0])
            
            L = box_side_length #/2 
            #L = distance from 0 to corner along each axis
            
            #Make corner points on boundaries
            #Delete them later
            bps = []
            bps.append(rs.AddPoint((0,0,0)))   #p0
            bps.append(rs.AddPoint((L,0,0)))  #p1
            bps.append(rs.AddPoint((L,L,0)))    
            bps.append(rs.AddPoint((0,L,0)))  
            bps.append(rs.AddPoint((L,0,L)))    #p4
            bps.append(rs.AddPoint((L,L,L)))   #p5
            bps.append(rs.AddPoint((0,L,L)))  #p6
            bps.append(rs.AddPoint((0,0,L)))   #p7
            
            #Make surfaces which are the boundaries
            bsurfs = []
            bsurfs.append(rs.AddSrfPt([bps[0],bps[1],bps[2],bps[3]])) #s0
            #self.boundary_1 = (rs.AddSrfPt([bps[0],bps[1],bps[2],bps[3]]))
            #self.boundary_list.append(self.boundary_1)
            bsurfs.append(rs.AddSrfPt([bps[4],bps[5],bps[6],bps[7]])) #s1
            #self.boundary_2 = (rs.AddSrfPt([bps[4],bps[5],bps[6],bps[7]]))
            #self.boundary_list.append(self.boundary_1)
            bsurfs.append(rs.AddSrfPt([bps[0],bps[1],bps[4],bps[7]])) #s2
            #self.boundary_3 = (rs.AddSrfPt([bps[0],bps[1],bps[4],bps[7]]))
            #self.boundary_list.append(self.boundary_1)
            bsurfs.append(rs.AddSrfPt([bps[1],bps[2],bps[5],bps[4]])) #s3
            #self.boundary_4 = (rs.AddSrfPt([bps[1],bps[2],bps[5],bps[4]]))
            #self.boundary_list.append(self.boundary_1)
            bsurfs.append(rs.AddSrfPt([bps[2],bps[3],bps[6],bps[5]])) #s4
            #self.boundary_5 = (rs.AddSrfPt([bps[2],bps[3],bps[6],bps[5]]))
            #self.boundary_list.append(self.boundary_1)
            bsurfs.append(rs.AddSrfPt([bps[3],bps[0],bps[7],bps[6]])) #s5
            #self.boundary_6 = (rs.AddSrfPt([bps[3],bps[0],bps[7],bps[6]]))
            #self.boundary_list.append(self.boundary_1)
            
            #Remove points as they are not needed
            rs.DeleteObjects(bps)
            #Return these boundaries for use elsewhere
            return bsurfs
    
    def GetSurfaceFromFractureLayer(self, layer_name):
        ##function to get surfaces from a layer
        surfs = [] #Will add found surfaces here 
        
        #Don't try ig the layer does not exist
        if rs.IsLayer(layer_name):
            #Get all identifiers for objects in the layer
            allobs = rs.ObjectsByLayer(layer_name) 
            for i in allobs: 
                if rs.IsSurface(i): #If this object is a surface
                    surfs.append(i) # Add to list
        
        return surfs
    
    def ConvertPolysurfaceToSurface(self, polysurface):
        #Confirm this is a polysurface
        if rs.ObjectType(polysurface) != 16:
            return [False, [polysurface]] #false, not a ploysurface
        #unjoins the polysurface and get identifiers of he separate surfaces
        surfaces = rs.ExplodePolysurfaces(polysurface) 
        
        #Sometimes, the function ExplodePolysurfaces makes polysurfaces.
        #If it did, call this function again on those surfaces!
        non_poly_surfaces = []
        for surf in surfaces:
            #check if polysurface was created instead of surface
            if rs.ObjectType(surf) == 16:
                #convert the object to surface using its GUID once more, incase polysurface was created ???
                additional_split_surfaces = ConvertPolysurfaceToSurface(surf)[1] #NB: RECURSIVE
                for new_surf in additional_split_surfaces:
                    non_poly_surfaces.append(new_surf)
                    #self.new_fractures.append(new_surf)
            else:
                non_poly_surfaces.append(surf)
                #self.new_fractures.append(surf)
        
        #Delete the old polysurface 
        rs.DeleteObject(polysurface)
        
        return [True, non_poly_surfaces]
    
    def CreateSetOfExtendedBoundaries(self, boundaries):
        #A fairly basic way to check if a surface is outside of the boundary is to
        #make a set of additional boundaries which go beyond the current boundaries
        #This is not perfect as it cannot guarantee to get all the surfaces
        #And requires many more intersection tests
        extended_boundary_surfaces = []
        
        #The boundaries are created by scaling up the other boundaries,
        #Using 0,0,0 as a reference point. Can make multiple different boundaries if
        #desired.
        distances = [1.001, 1.01, 1.1]
        
        for dist in distances:
            for boundary in boundaries:
                extended_boundary_surfaces.append(rs.ScaleObject(boundary,[10,10,10],[dist,dist,dist],True))
        
        return extended_boundary_surfaces
        
    def RemoveSurfacesIfAnyIntersectBoundary(self, surf, boundaries):
        #Checks if a surface intersects a boundary
        #If so, it deletes it and any created intersections
        #Could run this with any set of boundary surfaces
        #Intended to run with the CreateSetOfExtendedBoundaries function
        for boundary in boundaries:
            intersections = (rs.IntersectBreps(boundary,surf))
            if intersections is not None: #If there are intersections
                #Delete this surface
                rs.DeleteObject(surf)
                self.my_fractures.remove(surf) #delete the surface from domain fractures list
                #Delete all created intersections
                for inter in intersections:
                    rs.DeleteObject(inter)
                return True #WHY RETURN TRUE AND FALSE?
        return False
        
#Master function which calls the others, pruning the parts of the fractures
#which go outside of the box
#Takes the length of the boundary as an argument
#Assumes that the fractures are in layer(s) which start with "FRACTURE"
#Fractures can be in seperate layers or one single layer
#Key stratergy is to first intersect the fractures with the boundaries,
#using the function SplitBrep, which cuts the fractures when checking
#for intersections
#Then, to see if any fractures are outside of the domain, see if they 
#intersect a set of boundaries which are slightly larger than the external
#boundaries
    def RemoveSurfacesOutsideOfBox(self, b_length):
        try:
            if b_length <= 0:
                raise ValueError
        except ValueError:
            print("Value of boundary should be greater than 0")
        else:
            #Create boundary surfaces
            boundaries = self.CreateBoundary(b_length)
            
            #Get all layers in the document
            all_layers = rs.LayerNames()
            
            #Make a layer of intersections
            #To avoid error messages about deleting current layers:
            rs.AddLayer('Blank Layer')
            rs.CurrentLayer('Blank Layer')
            
            boundary_intersection_layer = "Boundary_Intersections"
            if rs.IsLayer(boundary_intersection_layer):
                rs.PurgeLayer(boundary_intersection_layer) #Deletes layer
            
            rs.AddLayer(boundary_intersection_layer)
            rs.CurrentLayer(boundary_intersection_layer)
            rs.LayerColor(boundary_intersection_layer, [200,0,0])
            
            #Make a polysurface of all the boundaries
            #This polysurf can be used with SplitBrep
            #If you compare surfaces individually, then fractures which intersect 
            #more than one surface (i.e. corners) do not get split correctly.
            box = rs.JoinSurfaces(boundaries)
            
            all_surfaces = [] 
            #Go over all the layers to find fractures 
            for layer in all_layers:
                #Only act if layer is a fracture layer
                #Some layers have short names, so ask for 1st letter first, then rest
                if layer[0] == 'F': 
                    if layer[0:8] == 'FRACTURE':
                        #Get surfaces in this layer
                        surfs = self.GetSurfaceFromFractureLayer(layer)
                        for surf in surfs: #BUT SURFS IS JUST A GUID
                            all_surfaces.append(surf)
            
            all_new_surfaces = [] #Store the split surfaces of the fractures
            print "Number of surfaces examined for splitting: ", len(all_surfaces)
            for surf in all_surfaces:
                #Run intersection test
                boundaries_touched = 0
                #for boundary in boundaries:
                #Use splitbrep here to split the fracture
                #surfaces by the boundaries directly
                #Brings back a polysurf which must be converted into a surface
                new_polysurfs = rs.SplitBrep(surf,box)
                if type(new_polysurfs) == list:
                    boundaries_touched += 1
                    for polysurf in new_polysurfs: #Because sometimes there are multiple surfaces
                        new_surfs = self.ConvertPolysurfaceToSurface(polysurf)
                        for new_surfs_i in new_surfs[1]:
                            all_new_surfaces.append(new_surfs_i)
                            self.my_fractures.append(new_surfs_i) #append to domain fracture list
                if boundaries_touched == 0:
                    #This means the fracture didn't intersect a boundary
                    #Add it to the list as well, so the final layer has all the fracs
                    copied_surf = rs.CopyObject(surf)
                    rs.ObjectLayer(copied_surf, boundary_intersection_layer)
                    all_new_surfaces.append(copied_surf)#ARE WE APPENDING THE FRAC OUTSIDE OR INSIDE
                    self.my_fractures.append(copied_surf) #append to domain fracture list
            
            print "Number of surfaces after splitting: ", len(all_new_surfaces)
            
            #Make extended boundary surfaces to check
            ext_boundaries = self.CreateSetOfExtendedBoundaries(boundaries)
            
            #Now, remove any surfaces which aren't inside the volume
            for surf in all_new_surfaces:
                self.RemoveSurfacesIfAnyIntersectBoundary(surf, ext_boundaries)
            
            #We don't need the extra boundaries anymore
            for boundary in ext_boundaries:
                rs.DeleteObject(boundary)
            for boundary in boundaries:
                rs.DeleteObject(boundary)
            rs.DeleteObject(box)
            
            return
        
        
        
    def PercolationMatrix(self, boundary_list, domain_fractures):
        try:
            if type(boundary_list != list) or type(domain_fractures != list):
                raise TypeError
        except TypeError:
            print("The two arguments should be type list")
        else: 
            #initialize Matrix
            mat = []
            #number of fractures
            num_frac = len(domain_fractures)
            #number of rows and cols for matrix 
            n_row = num_frac + 6
            n_col = num_frac + 6
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
                        intersection = rs.IntersectBreps(domain_fractures[i],domain_fractures[j])
                        if intersection is not None:
                            mat[i][j] = rs.CurveLength(intersection[0]) 
            #boundary-fractures
            for i in range(num_frac): #0 to number of fractures - 1
                for j in range(num_frac, n_col): #number of fractures to end of row/col
                    intersection = rs.IntersectBreps(domain_fractures[i],boundary_list[j-num_frac])
                    if intersection is not None:
                        mat[i][j] = rs.CurveLength(intersection[0]) 
                        mat[j][i] = rs.CurveLength(intersection[0]) 
            
            return mat

#    def Percolate(self, initial_guid, target_guid, domain_fractures):
#        #check if any fracture intersect initial guid
#        intersection_list = []
#        
#        for frac in domain_fractures:
#            #does frac intersect with initial guid
#            intersection = rs.IntersectBreps(frac,initial_guid)
#            if intersection is not None:
#                #append fracture in intersection list
#                intersection_list.append(frac)
#        #if the list is empty, which means no fracture intersects with the
#        #initial GUID, return False
#        if not intersection_list:
#            #no percolation
#            return False
#        #Now we have appended all fractures that intersected the initial GUID, let's check for percolation
#        finish = 0
#        while (finish != 1):
#            num_frac = len(intersection_list)
#            #check if any of the fractures intersect the traget guid, in case we have a very large fracture that does so
#            for frac in intersection_list:
#                #does frac intersect with target guid
#                intersection = rs.IntersectBreps(frac,target_guid)
#                #if any fracture does intersect
#                if intersection is not None:
#                    #end while loop
#                    return True
#                    
#                    #finish = True
#                    #return True
#                    
#                    
#            #check intersection between list of fractures and other fractures in the domain
#            for dom_frac in domain_fractures:
#                for frac in intersection_list: 
#                    if dom_frac not in intersection_list:
#                        #check if it intersects any of our fractures
#                        intersection = rs.IntersectBreps(frac,dom_frac)
#                        if intersection is not None:
#                            #append fracture in intersection list
#                            intersection_list.append(dom_frac)
#                        
#            #delete all previous fractures
#            del intersection_list[:num_frac]
#            #if list is empty, which means no more connections
#            if not intersection_list:
#                #end while loop
#                return False
#                
#                #finish = True
#                
                #no percolation
                
                




if __name__ == "__main__": 
    dom = Domain(boxlength)
    print(Domain.number_of_fractures)
    ids = dom.show()
    print(dom.type)
    #dom.CreateBoundary(-1)
    #print(dom.volume)
    #print(dom.center)
    #print(ids)
