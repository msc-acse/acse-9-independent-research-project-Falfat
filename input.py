
def ReadFile(file):
    #open the file
    file = open(file, "r")
    
    #read the lines of the file
    f1 = file.readlines()
    
    for line in f1:
        #check for a line in which starts with "radius"
        if line.find("radius") == 0:
            #split the line
            line1 = line.split()
            #store the value of radius as a float
            radius = float(line1[2])
        #check for a line in which starts with "length"
        if line.find("length") == 0:
            #split the line
            line1 = line.split()
            #store the value of the box length as a float
            boxlength = float(line1[2])
        #check for a line in which starts with "numberof circles"
        if line.find("numberofcircles") == 0:
            #split the line
            line1 = line.split()
            #store the nuber of circles as an integer
            n = int(line1[2])
        if line.find("orientation") == 0:
            #split the line
            line1 = line.split()
            #store the orientation distribution as string
            orientation_dist = line1[2]
        if line.find("location") == 0:
            #split the line
            line1 = line.split()
            #store the location distribution as string
            location_dist = line1[2]
        if line.find("shape") == 0:
            #split the line
            line1 = line.split()
            #store the location distribution as string
            fracture_shape = line1[2]
            #print(type(fracture_shape))
    return radius, boxlength, n, orientation_dist, location_dist, fracture_shape
    
#name = "DataFile.txt"
#radius, boxlength, n, orientation_dist, location_dist, fracture_shape = ReadFile(name)
