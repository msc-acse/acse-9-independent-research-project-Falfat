## Script for trimming surfaces which are outside of a cubic domain
# Robin Thomas, April 2019

import rhinoscriptsyntax as rs

__commandname__ = "remove_surfaces_outside_of_box"

#Function for creating boundary surfaces
#It makes sure not to duplicate an existing boundary layer
#Takes the length of one side of the box
#Returns the six sides of the box
def CreateBoundary(box_side_length):
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
    bsurfs.append(rs.AddSrfPt([bps[4],bps[5],bps[6],bps[7]])) #s1
    bsurfs.append(rs.AddSrfPt([bps[0],bps[1],bps[4],bps[7]])) #s2
    bsurfs.append(rs.AddSrfPt([bps[1],bps[2],bps[5],bps[4]])) #s3
    bsurfs.append(rs.AddSrfPt([bps[2],bps[3],bps[6],bps[5]])) #s4
    bsurfs.append(rs.AddSrfPt([bps[3],bps[0],bps[7],bps[6]])) #s5
    
    #Remove points as they are not needed
    rs.DeleteObjects(bps)
    
    #Return these boundaries for use elsewhere
    return bsurfs

#Given a layer name, gets the surfaces inside it
#Use to make sure we always intersect surfaces with others
def GetSurfaceFromFractureLayer(layer_name):
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

#Polysurfaces are made by SplitBrep
#We can't use normal functions on them
#We can turn them back into seperate surfaces with ExplodePolysurfaces
#This function handles this for us
#Returns a list - the first item is always true or false
#False means the object was not a polysurface so no action was taken
#True means the object was a polysurface
#If true, The other item is a list of created surfaces
def ConvertPolysurfaceToSurface(polysurface):
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
        else:
            non_poly_surfaces.append(surf)
    
    #Delete the old polysurface 
    rs.DeleteObject(polysurface)
    
    return [True, non_poly_surfaces]

#A fairly basic way to check if a surface is outside of the boundary is to
#make a set of additional boundaries which go beyond the current boundaries
#This is not perfect as it cannot guarantee to get all the surfaces
#And requires many more intersection tests
def CreateSetOfExtendedBoundaries(boundaries):
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

#Checks if a surface intersects a boundary
#If so, it deletes it and any created intersections
#Could run this with any set of boundary surfaces
#Intended to run with the CreateSetOfExtendedBoundaries function
def RemoveSurfacesIfAnyIntersectBoundary(surf, boundaries):
    for boundary in boundaries:
        intersections = (rs.IntersectBreps(boundary,surf))
        if intersections is not None: #If there are intersections
            #Delete this surface
            rs.DeleteObject(surf)
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
def RemoveSurfacesOutsideOfBox(b_length):
    #Create boundary surfaces
    boundaries = CreateBoundary(b_length)
    
    #Go over all layers
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
                surfs = GetSurfaceFromFractureLayer(layer)
                for surf in surfs: #WHY THE FOR LOOP, WHEN SURF IS JUST A GUID
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
        if type(new_polysurfs) == list: #if the surface intersects the boundary
            boundaries_touched += 1
            for polysurf in new_polysurfs: #Because sometimes there are multiple surfaces
                new_surfs = self.ConvertPolysurfaceToSurface(polysurf)
                for new_surfs_i in new_surfs[1]:
                    all_new_surfaces.append(new_surfs_i) 
        if boundaries_touched == 0:
            #This means the fracture didn't intersect a boundary
            #Add it to the list as well, so the final layer has all the fracs
            copied_surf = rs.CopyObject(surf)
            rs.ObjectLayer(copied_surf, boundary_intersection_layer)
            all_new_surfaces.append(copied_surf)
    
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

#Run this command:
def RunCommand():
    rs.EnableRedraw(False) #Avoid drawing whilst computing
    print "Starting RemoveSurfacesOutsideOfBox"
    
    boundary_length = 20 #Set length of sides of boundaries
    RemoveSurfacesOutsideOfBox(boundary_length)
    
    print "Finished RemoveSurfacesOutsideOfBox"
    rs.EnableRedraw(True)
    return

RunCommand()