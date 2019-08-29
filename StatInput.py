# Falola Yusuf, Github: falfat
def ReadFile(file):
    """
    Function to read statistical data and returns orientation distribution,
    location distribution and size distribution

    Parameter
    --------
    file: str
        name of file containing data
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
            if line.find("orientation") == 0:
                # split the line
                line1 = line.split()
                # store the orientation distribution as string
                orientation_dist = line1[2]
            if line.find("location") == 0:
                # split the line
                line1 = line.split()
                # store the location distribution as string
                location_dist = line1[2]
            if line.find("size") == 0:
                # split the line
                line1 = line.split()
                # store the location distribution as string
                size_dist = line1[2]
        # close file
        file.close()
    # return variablea
    return orientation_dist, location_dist, size_dist
