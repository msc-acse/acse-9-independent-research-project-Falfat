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

rs.EnableRedraw(False)
sc.doc.Objects.Clear()

#input data
name = "DataFile.txt"
size_dist = 'uniform'
radius, boxlength, n, orientation_dist, location_dist, fracture_shape = input.ReadFile(name)

def fractures(frac_list):
    f = []
    for frac in frac_list:
        f.append(frac.fracture_GUID)
    return f
#Np = 0
#for i in range(50):
#dom = Domain.Domain(boxlength) 
## draws domain
#d = dom.show() 
#n =54
## NB: The arguments of FixedFractureGen() must be edited to suit the 
## shape type, For instance, sides, min_angle and max_angle should be 
## specified for a polygon
#frac_list = DFN_Gen.FixedFractureGen(n,0,0,360,4)
#f = fractures(frac_list)
#boundary_list = dom.CreateBoundary(20)
## create the intersection matrix to test for percolation
#matrix = dom.IntersectionMatrix(boundary_list,f)
##print(matrix)
## check for percolation between the two opposite boundaries specified
## boundary_list[2] & boundary_list[4] for horizontal facing 1
## boundary_list[3] & boundary_list[5] for horizontal facing 2
#per1 = dom.Percolate(boundary_list[2],boundary_list[4],boundary_list,matrix,f)
#print(per1)
#    if per1:
#        Np+=1
#    if not per1:
#        sc.doc.Objects.Clear()
#print(Np)



num_realisations = 100
Vex = 45.26
# list to store the percolation probability.
# percolation probability = Np/num_of realisations
# percolation probability is also the connectivity index 
percolation_probability = []
# list of fraction of open area
# fraction of open area = area of all fractures in the domain/area of domain
rho_p = []
# initialise fractures area for all realisations 
fractures_area = 0
# define path
#path1 = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/percolation_probability.txt"
#path2 = "C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files/open_area.txt"
#file1 = open(path1, 'w')
#file2 = open(path2, 'w')
for n in range(380,440,10): 
    # number of realisations that percolate
    Np = 0
    for j in range(num_realisations):
        # creates the domain
        dom = Domain.Domain(boxlength) 
        # draws domain
        d = dom.show() 
        # NB: The arguments of FixedFractureGen() must be edited to suit the 
        # shape type, For instance, sides, min_angle and max_angle should be 
        # specified for a polygon
        frac_list = DFN_Gen.FixedFractureGen(n,0,0,360,5) # inserts fractures and returns the GUIDs
        f = fractures(frac_list)
        #dom.RemoveSurfacesOutsideOfBox(dom.length) #trims fractures outside the domain
        #dom_frac = dom.my_fractures #get the fractures in the domain
        #swap old guids with new ones and put new guids in old frac layers
        #new_frac_guids = Frac.new_fracture_guids(dom_frac,frac_list) 
        # get list of boundaries to test for percolation 
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
            #return
        sc.doc.Objects.Clear()
    rho_prime = Vex*(n/8000)
    rho_p.append(rho_prime)
    percolation_probability.append(Np/num_realisations)
print(rho_p)
print(percolation_probability)
    
# write to file 
#file1.write(str(percolation_probability))
#file2.write(str(S_0))
# close file
#file1.close()
#file2.close()