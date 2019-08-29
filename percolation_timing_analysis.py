# falola yusuf, fyf17@ic.ac.uk, github: falfat
# code for timing percolation
import time

import rhinoscriptsyntax as rs
import Frac
import Domain
import DFN_Gen 
import DFN_Analysis
from DFN_Analysis import IntersectionAnalysis 
from Frac import Fracture
from DFN_Analysis import CutPlane
from Matrix import Matrix
import Input
import StatInput
import scriptcontext as sc
import math
import random

# read input from text files
data = "DataFile.txt"
radius, boxlength, n, fracture_shape = Input.ReadFile(data)
stat_data = "StatFile.txt"
orientation_dist, location_dist, size_dist = StatInput.ReadFile(stat_data)

def fractures(frac_list):
    # get GUID of fractures from the Fracture class
    f = []
    for frac in frac_list:
        f.append(frac.fracture_GUID)
    return f
 
# do not draw while computing
rs.EnableRedraw(False)

times = []
# range of number of farctures
for n in range(50,550,50):
    # iterate 10 times for each number of fracture
    for i in range(10):
        t = 0
        # generate fracture network
        dom = Domain.Domain(boxlength) 
        # draws domain
        d = dom.Show() 
        # insert fractures and get the fracture objects
        frac_list = DFN_Gen.FixedFractureGen(n)
        # extract the guid of fractures
        f = fractures(frac_list)
        # get list of boundaries to test for percolation
        boundary_list = dom.CreateBoundary(20)
        # start time
        start = time.time()
        ## create the intersection matrix to test for percolation
        matrix = dom.IntersectionMatrix(boundary_list,f)
        # end time
        end = time.time()
        # append time
        t+=(end-start)
        # clear screen before next iteration
        sc.doc.Objects.Clear()
    # append time after the 10 iterations
    times.append(t/10)
# print the timings       
print(times)

