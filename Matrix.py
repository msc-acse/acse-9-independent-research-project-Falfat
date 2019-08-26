class Matrix:
    """
    A matrix class to handle intersection matrix appropriately

    Attributes
    ----------
    matrix: matrix
        intersection matrix
    rows: int
        number of rows of matrix
    cols: int
        number of column of matrix
    size: int
        matrix size

    Methods
    -------
    PrintMatrix()
        prints matrix in an appropriate form
    MatrixToFile()
        save matirx to text file
    ConvertObjectToIndex(object_type, object_guid, boundary_list,
                         domain_fractures)
        converts a object guid to its index in the matrix
    """
    def __init__(self, matrix):
        """
        matrix: matrix
            intersection matrix
        """
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.size = self.rows * self.cols

    def PrintMatrix(self):
        """
        prints matrix in an appropriate form

        Parameters
        ----------
        None
        """
        # loop through the rows
        for i in range(self.rows):
            # intialise the matrix
            mat = []
            # loop through the column
            for j in range(self.cols):
                # append matrix element
                mat.append(self.matrix[i][j])
            # print the matrix
            print(mat)

    def MatrixToFile(self):
        """
        function to save matirx to text file, returns none
        """
        # open text file
        file = open("intersection_matrix.txt", 'w')
        # write opening square bracket for matrix
        file.write("[")
        # use for loop to write in the matrix
        for i in range(self.rows):
            # square brackets to append in elements of a row of the matrix
            mat = []
            if i != 0:
                # separate each row with a comma
                file.write(",")
            for j in range(self.cols):
                # append elements of the row
                mat.append(self.matrix[i][j])
            # avoid having space as the first row in the text file
            if i != 0:
                file.write("\n")
            # write in the row
            file.write(str(mat))
        # write closing bracket for the matrix
        file.write("]")
        # close file
        file.close()
        return

    def ConvertObjectToIndex(self, object_type, object_guid,
                             boundary_list, domain_fractures):
        """
        function converts a object guid to its index in the matrix.
        Returns the index

        Parameters
        ----------
        object_type: str
            the type of object (either "boundary" of "fracture")
        object_guid: guid
            guid of the object
        boundary_list: list
            list of boundary guids
        domain_fractures: list
            list of fractures guids
        """
        if object_type == "boundary":
            # get index of init_guid in the boundary list
            p1 = [i for i in range(len(boundary_list)) if boundary_list[i] == object_guid]
            # row of init_guid in the matrix
            # len(intersection_matrix[1]) = matrix row
            # len(boundary_list)  = number of boundarues
            # p1[0] = index of initial guid in the list
            b_position = p1[0] + self.rows - len(boundary_list)
            return b_position
        # if the object is a fracture
        if object_type == "fracture":
            # get index of fracture in the fracture list
            p1 = [i for i in range(len(domain_fractures)) if domain_fractures[i] == object_guid]
            # fracture index in matix is same as in the list
            return p1[0]
