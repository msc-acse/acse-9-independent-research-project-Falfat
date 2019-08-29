# Falola Yusuf, Github: falfat
# import necessary modules
import rhinoscriptsyntax as rs
import DFN_Gen
import Domain
import Input
import DFN_Gen
import Frac
import scriptcontext as sc

#sc.doc.Objects.Clear() 

#Avoid drawing whilst computing
rs.EnableRedraw(False) 

#read fracture network data
data = "DataFile.txt"
radius, boxlength, n, fracture_shape = Input.ReadFile(data)

#create an instance of domain
dom = Domain.Domain(boxlength) 

#draw domain
dom.Show() 

#insert n fractures in the domain
frac_list = DFN_Gen.FixedFractureGen(n)

#trims fractures outside the domain 
dom.RemoveSurfacesOutsideOfBox(dom.length)

#get the guids of new fractures in the domain after trimming
dom_frac = dom.my_fractures

# delete the old fractures 
# change the guid of Fracture object to the new ones
new_frac_guids = Frac.NewFracturesGuids(dom_frac,frac_list)



# -- uncomment below to test percolation and intersection matrix functions -- ##

# get list of boundaries to test for percolation 
#boundary_list = dom.CreateBoundary(boxlength)
## create the intersection matrix to test for percolation
#matrix = dom.IntersectionMatrix(boundary_list,new_frac_guids)
#
## check for percolation between the two opposite boundaries specified
#per = dom.Percolate(boundary_list[2],boundary_list[4],
#                    boundary_list,matrix,new_frac_guids)
#print(per)

# -- uncomment below for to test 3D analysis functions -- #

##print number of fractures in the domain
#Total_Fractures = dom.NumberOfFractures()
#print(Total_Fractures)
#
##check if the first Fracture_1 intersects Fracture_8
#frac_list[0].Intersect(frac_list[7])
#
## import analysis module
#import DFN_Analysis as da
#
## create an instance of IntersectionAnalysis class
#ia = da.IntersectionAnalysis()
#
## find total length of intersection
#l = ia.LengthOfIntersection(new_frac_guids)
#print(l)
#
## determine fracture intensity P32 
#domain_width, domain_length, domain_height = boxlength, boxlength, boxlength
#P_32 = ia.FractureIntensity_P32(new_frac_guids,domain_length, 
#                                domain_width, domain_height)
#print(P_32) 
#
## find total lengths of intersection per unit area
#inter_per_unit_area = ia.IntersectionsPerUnitArea(new_frac_guids, domain_length,
#                                               domain_width, domain_height)
#print(inter_per_unit_area)

# -- uncomment below for cutplane analysis, intersection matrix --#
# --and percolation functions -- #

## import analysis module
#import DFN_Analysis as da
#
## create an instance of the cutplane class
#cp = da.CutPlane('YZ', 20, 20.0)
#
## draw a plane inclined 0 degree in y-direction 
#plane = cp.DrawPlane(10,[0,1,0], 0)
#
## total length of fractures intersecting the plane
#length = cp.TotalLengthOfFractures(new_frac_guids, plane)
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
## get the list of fractures that crossed the plane
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

## -- test regen function -- ##

## import required module
#import DFN_ReGen as dr
#
## specify path where the text file is saved
#path = "~/Rhinoceros/6.0/scripts/text_files/fracture_data.txt"
#
## regenerate fracture network
#dr.RedrawNetwork(path)


# -- test postprocessing module -- ##
# NB: plots can only be done on IDE. The codes below is to get data for 
# postprocessing on an IDE

## import Processessing module
#import PostProcessing as pp
#
## save the lengths of intersecting lines 
#l = ia.LengthOfIntersection(new_fracture_guids)
#
## get the all lengths of intersection
#lengths = ia.lengths_of_intersection_lines 
