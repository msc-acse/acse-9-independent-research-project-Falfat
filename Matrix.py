class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.size = self.rows * self.cols
        
    def PrintMatrix(self):
        for i in range(self.rows):
            l = []
            for j in range(self.cols):
                l.append(self.matrix[i][j])
            print(l)
            
    def MatrixToFile(self):
        #open text file
        file = open("intersection_matrix.txt", 'w')
        #write opening square bracket for matrix
        file.write("[")
        #use for loop to write in the matrix
        for i in range(self.rows):
            #square brackets to append in elements of a row of the matrix
            l = []
            if i != 0:
                #separate each row with a comma 
                file.write(",")
            for j in range(self.cols):
                #append elements of the row
                l.append(self.matrix[i][j])
            #avoid having space as the first row in the text file
            if i != 0:
                file.write("\n")
            #write in the row
            file.write(str(l))
        #write closing bracket for the matrix
        file.write("]")
        file.close()
        
    def ConvertObjectToIndex(self, object_type, object_guid, boundary_list, domain_fractures):
        if object_type == "boundary":
            #get index of init_guid in the boundary list
            p1 = [i for i in range(len(boundary_list)) if boundary_list[i] == object_guid]
            #row of init_guid in the matrix
            #len(intersection_matrix[1]) = matrix row
            #len(boundary_list)  = number of boundarues
            #p1[0] = index of initial guid in the list
            b_position = p1[0] + self.rows - len(boundary_list) 
            return b_position
        
        if object_type == "fracture":
            #get index of fracture in the fracture list
            p1 = [i for i in range(len(domain_fractures)) if domain_fractures[i] == object_guid]
            #fracture index in matix is same as in the list
            return p1[0]
           
                

#mat = [[1,2,3,4],[5,5,6,7],[4,5,6,7]]
#m = Matrix(mat)
#m.PrintMatrix()
#m.MatrixToFile()