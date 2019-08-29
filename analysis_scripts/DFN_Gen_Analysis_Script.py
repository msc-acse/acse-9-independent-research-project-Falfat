import rhinoscriptsyntax as rs
import Frac
import Domain
import DFN_Gen 
import DFN_Analysis
from DFN_Analysis import IntersectionAnalysis 
from Frac import Fracture
from DFN_Analysis import CutPlane
from Matrix import Matrix
import input
import scriptcontext as sc
import math
import os

rs.EnableRedraw(False) #Avoid drawing whilst computing

#####                    ####
# computation is done below #
#####                    ####

#input data
name = "DataFile.txt"
size_dist = 'uniform'
radius, boxlength, n, orientation_dist, location_dist, fracture_shape = input.ReadFile(name)

######                                                              ####
## Script to get all the lengths of intersections and make a histogram #
## Uncomment the code block below                                      #
######                                                              ####
#
##list to store the lenghts of intersections for all iterations
#le = []
##number of iterations, here we specified 10
#n = 50
##change directory, so as to save text file in the designated folder
#os.chdir("/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files")
##open text file to store all lengths of intersection for post processing 
#file = open("3D_lengths_of_intersction.txt", 'w')
#for i in range(n):
#    dom = Domain.Domain(boxlength) #creates the domain
#    d = dom.show() #draws domain
#    frac_list = DFN_Gen.RandomFractureGen(60, 80, 1, 3,1,4, 4, 7) # inserts fractures and returns the GUIDs
#    dom.RemoveSurfacesOutsideOfBox(dom.length) # trims fractures outside the domain
#    dom_frac = dom.my_fractures #get the fractures in the domain
#    # swap old guids with new ones and put new guids in old frac layers
#    new_frac_guids = Frac.new_fracture_guids(dom_frac,frac_list) 
#    # create an instance for intersection analysis
#    ia = IntersectionAnalysis()
#    #total length of iteration
#    total_length_of_inter = ia.LengthOfIntersection(new_frac_guids)
#    # lengths of all lines of intersection
#    l = ia.lengths_of_intersection_lines
#    # add to list of all lengths
#    le += l
#    # clear screen before next iteration
#    sc.doc.Objects.Clear()
##write to file 
#file.write(str(le))
##close file
#file.close()

#####                                                          ####
# Script to determine critical functional open area for fractures #
# Uncomment the code block below                                  #
#####                                                          ####

def fractures(frac_list):
    f = []
    for frac in frac_list:
        f.append(frac.fracture_GUID)
    return f

num_realisations = 300
# list to store the percolation probability.
# percolation probability = Np/num_of realisations
# percolation probability is also the connectivity index 
percolation_probability = []
# list of fraction of open area
# fraction of open area = area of all fractures in the domain/area of domain
S_0 = []
# initialise fractures area for all realisations 
fractures_area = 0
# define path
#path1 = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/percolation_probability.txt"
#path2 = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/open_area.txt"
#file1 = open(path1, 'w')
#file2 = open(path2, 'w')
for i in range(5,55,5):
    # number of fractures to be generated, overites the number of fractures
    # from input file.
    n = i 
    #fractures_area = 0
    # number of realisations that percolate
    Np = 0
    for j in range(num_realisations):
        # creates the domain
        dom = Domain.Domain(boxlength) 
        # draws domain
        d = dom.show() 
        # set shape of farcture, so we don't have to change in file 
        #fracture_shape = 'circle' 
        # NB: The arguments of FixedFractureGen() must be edited to suit the 
        # shape type, For instance, sides, min_angle and max_angle should be 
        # specified for a polygon
        frac_list = DFN_Gen.FixedFractureGen(n,0,0,360,6) # inserts fractures and returns the GUIDs
        ##dom.RemoveSurfacesOutsideOfBox(dom.length) #trims fractures outside the domain
        ##dom_frac = dom.my_fractures #get the fractures in the domain
        #swap old guids with new ones and put new guids in old frac layers
        ##new_frac_guids = Frac.new_fracture_guids(dom_frac,frac_list) 
        # get list of boundaries to test for percolation 
        f = fractures(frac_list)
        boundary_list = dom.CreateBoundary(20)
        # create the intersection matrix to test for percolation
        matrix = dom.IntersectionMatrix(boundary_list,f)
        # check for percolation between the two opposite boundaries specified
        # boundary_list[2] & boundary_list[4] for horizontal facing 1
        # boundary_list[3] & boundary_list[5] for horizontal facing 2
        per1 = dom.Percolate(boundary_list[2],boundary_list[4],boundary_list,matrix,f)
        #per2 = dom.Percolate(boundary_list[3],boundary_list[5],boundary_list,matrix,new_frac_guids)
        # if there is percolation
        if per1:
            # increase number of realisations that percolate
            Np+=1
        # create an instance of intersection analysis
        ##ia = IntersectionAnalysis()
        # determine fractures surface area for the realisation
        ##frac_surf_area = ia.FracturesSurfaceArea(new_frac_guids)
        # increment fractures area for all realisations 
        # we do this because the areas will be a bit different for each 
        # realisation, due to trimming out of bounds fractures
        ##fractures_area += frac_surf_area
        # clear screen before next iteration
        sc.doc.Objects.Clear()
    # find the total surface area of the domain
    domain_area = 2400
    # determine the mean fractures surface area
    ##mean_fractures_area = fractures_area/num_realisations
    # append open area
    S_0.append((n*41.57)/domain_area)
    # append probablility
    percolation_probability.append(Np/num_realisations)
print(S_0)
print(percolation_probability)
    
# write to file 
#file1.write(str(percolation_probability))
#file2.write(str(S_0))
# close file
#file1.close()
#file2.close()
#we can then plot percolation_probability against S_0


#####                                                          ####
# Script to determine effect of fracture size on percolation state#
# Uncomment the code block below                                  #
#####                                                          ####

#size_list1 = [6, 5.75, 5.5, 5.25, 5, 4.75, 4.5, 4.25, 4, 3.75, 3.5, 3.25]
#size_list2 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]
##size_list2 = [0.25, 0.5]
##size_list1 = [6, 5.75]
#num_realisations = 50
#list_Np = []
#for i in range(len(size_list2)):
#    Np = 0
#    for j in range(num_realisations):
#        # creates the domain
#        dom = Domain.Domain(boxlength) 
#        # draws domain
#        d = dom.show() 
#        # set shape of farcture, so we don't have to change in file 
#        fracture_shape = 'circle' 
#        # generate fractures within the range of sizes specified
#        # here 30 fractures are being generated 
#        frac_list = DFN_Gen.RandomFractureGen(20, 20, size_list1[i] , size_list2[i])
#        dom.RemoveSurfacesOutsideOfBox(dom.length) # trims fractures outside the domain
#        dom_frac = dom.my_fractures # get the fractures in the domain
#        #swap old guids with new ones and put new guids in old frac layers
#        new_frac_guids = Frac.new_fracture_guids(dom_frac,frac_list) 
#        # get list of boundaries to test for percolation 
#        boundary_list = dom.CreateBoundary(20)
#        # create the intersection matrix to test for percolation
#        matrix = dom.IntersectionMatrix(boundary_list,new_frac_guids)
#        # check for percolation between the two opposite boundaries specified
#        # boundary_list[2] & boundary_list[4] for horizontal facing 1
#        # boundary_list[3] & boundary_list[5] for horizontal facing 2
#        per1 = dom.Percolate(boundary_list[2],boundary_list[4],boundary_list,matrix,new_frac_guids)
#        #per2 = dom.Percolate(boundary_list[3],boundary_list[5],boundary_list,matrix,new_frac_guids)
#        # if there is percolation
#        if per1:
#            # increase number of realisations that percolate
#            Np+=1
#            
#        # clear screen before next iteration
#        sc.doc.Objects.Clear()
#    list_Np.append(Np)
#    
#print(list_Np)

