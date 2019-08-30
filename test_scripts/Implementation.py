# Falola Yusuf, Github: falfat

import rhinoscriptsyntax as rs
import DFN_Gen
import Domain
import Input
import DFN_Gen
import DFN_ReGen
import Frac
import DFN_Analysis

reload(DFN_ReGen)
reload(DFN_Analysis)

#Avoid drawing whilst computing
rs.EnableRedraw(False) 

#read fracture network data
data = "DataFile.txt"
radius, boxlength, n, fracture_shape = Input.ReadFile(data)
#
### --- The code block below was used to generate the fracture networks used for analysis in the report -- ###
##create an instance of domain
#dom = Domain.Domain(boxlength) 
#
##draw domain
#dom.Show() 
#
##insert n fractures in the domain
#frac_list = DFN_Gen.FixedFractureGen(50,aspect_ratio=2 sides =5)

#dom.RemoveSurfacesOutsideOfBox(dom.length)
### -- change the file path to the correct shape fracture data text file --###
# NB: specifically use the DFN_ReGen_Old for  this analysis only
# The structure of the input file for Polygon was changed after the report was prepared
# Hence the new GFN_Regen will not be able to work for the polygon text file
# for this analysis
path = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/fracture_circle_data.txt"
#
f = DFN_ReGen.RedrawNetwork(path)
##print(len(f))


## ---- uncomment the code below for intersection and percolation analysis --- ####

#import DFN_Analysis as da
#ia = da.IntersectionAnalysis()
##find total length of intersection
#l = ia.LengthOfIntersection(f)
##find P32
#P32 = ia.FractureIntensity_P32(f, 20, 20, 20)
#print(P32)
## intersection per unit area
##i_a = l/8000
#dom = Domain.Domain(boxlength) 
## draws domain
#d = dom.Show() 
#boundary_list = dom.CreateBoundary(20)
## create the intersection matrix to test for percolation
#matrix = dom.IntersectionMatrix(boundary_list,f)
## check for percolation between the two opposite boundaries specified
## boundary_list[2] & boundary_list[4] for horizontal facing 1
## boundary_list[3] & boundary_list[5] for horizontal facing 2
#per1 = dom.Percolate(boundary_list[2],boundary_list[4],boundary_list,matrix,f)
#per2 = dom.Percolate(boundary_list[3],boundary_list[5],boundary_list,matrix,f)
#per3 = dom.Percolate(boundary_list[0],boundary_list[1],boundary_list,matrix,f)
#print(per1)
#print(per2)
#print(per3)


## -- CUT PLANE ANALYSIS -- ##

#import analysis module
#import DFN_Analysis as da
#
## create an instance of the cutplane class
#cp = da.CutPlane('ZX', 20, 20.0)
#
## draw a plane inclined 0 degree in y-direction 
#plane = cp.DrawPlane(10,[0,1,0], 0)
#
## total length of fractures intersecting the plane
#length = cp.TotalLengthOfFractures(f, plane)
#print(length)
#
## number of intersecting fractures
#num = cp.NumberOfIntersectingFractures()
#print(num)
#
### fracture intensity P21
#P_21 = cp.FractureIntensity_P21(length)
#print(P_21)
#
# get the list of fractures that crossed the plane
#inter_frac = cp.intersecting_fractures
#
## break the plane into four lines for percolation analysis
#lines = cp.PlaneLines(cp.GUID)
#
## create the intersection matrix
#mat = cp.IntersectionMatrix(lines,inter_frac)
#
## check for percolation
#percolate = cp.Percolate(lines[0], lines[2], lines, mat, inter_frac)
#print(percolate)


#percolate1 = cp.Percolate(lines[1], lines[3], lines, mat, inter_frac)
#print(percolate)
#print(percolate1)

## --- POST PROCESSING -- ##

## -- histogram of lengths of intersection -- ##
#import DFN_Analysis as da
## create an instance of the analysis class
#ia = da.IntersectionAnalysis()
## find total length of intersection
#l = ia.LengthOfIntersection(f)
#
#print(ia.lengths_of_intersection_lines)

## -- color map of intersection matrix -- ##
#dom = Domain.Domain(boxlength) 
## draws domain
#d = dom.Show() 
## get list of boundaries for intersection analysis
#boundary_list = dom.CreateBoundary(20)
## create the intersection matrix to test for percolation
#matrix = dom.IntersectionMatrix(boundary_list,f)
#print(matrix)


## -- intersection per fracture --##
## import module
#import DFN_Analysis as da
#dom = Domain.Domain(boxlength) 
## draws domain
#d = dom.Show() 
## get list of boundaries for intersection analysis
#boundary_list = dom.CreateBoundary(20)
## create the intersection matrix to test for percolation
#matrix = dom.IntersectionMatrix(boundary_list,f)
#inter = da.IntersectionsPerFfracture(matrix)
#print(inter)

## import postprocessing module
#import DFN_PostProcessing as pp
#
## save the lengths of intersecting lines
#l = ia.LengthOfIntersection(new_fracture_guids)
#
## get all lengths of intersection
#lengths = ia.lengths_of_intersection_lines
#print(lengths)
#
## get the number of intersections per fracture
#inter_list = da.IntersectionsPerFfracture(mat)
#print(inter_list)


