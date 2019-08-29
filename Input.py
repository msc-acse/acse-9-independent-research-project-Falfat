# Falola Yusuf, GitHub: Falfat


def ReadFile(file):
    """
    function to read file and return fracture parameters

    Parameters
    ----------
    file: str
        name of text file containing data
    """
    # open the file
    try:
        file = open(file, "r")
    # if file isn't found
    except FileNotFoundError:
        # print error
        print("The file can't be found in the current folder")
    # if there is any general error
    except Exception as err:
        # print that error
        print(err)
    else:
        # read the lines of the file
        f1 = file.readlines()
        for line in f1:
            # check for a line in which starts with "radius"
            if line.find("radius") == 0:
                # split the line
                line1 = line.split()
                # store the value of radius as a float
                radius = float(line1[2])
            # check for a line in which starts with "length"
            if line.find("length") == 0:
                # split the line
                line1 = line.split()
                # store the value of the box length as a float
                boxlength = float(line1[2])
            # check for a line in which starts with "numberof circles"
            if line.find("numberoffractures") == 0:
                # split the line
                line1 = line.split()
                # store the nuber of circles as an integer
                n = int(line1[2])
            if line.find("shape") == 0:
                # split the line
                line1 = line.split()
                # store the location distribution as string
                fracture_shape = line1[2]
                # print(type(fracture_shape))
        # close file
        file.close()
    # return variables
    return radius, boxlength, n, fracture_shape
