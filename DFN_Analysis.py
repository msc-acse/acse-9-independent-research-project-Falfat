import rhinoscriptsyntax as rs


class IntersectionAnalysis:
    """
    A class for fracture network intersection analysis
    
    .....

    Attributes
    ----------
    no_of_fracture_intersections: int
        the number of fracture intersections in the network
    lengths_of_intersection_lines : list
        a list of all the length of intersections
    
    Methods
    -------
    LengthOfIntersection(fracture_guid_list)
        returns the sum of all length of intersections and helps to track
        the number of fracture intersections  
    FracturesSurfaceArea(fracture_guid_list)
        determines the total surface area of all fractures in the medium
    FractureIntensity_P32(fracture_guid_list, domain_length, domain_width,
                          domain_height)
        returns the P_32 fracture intensity
    IntersectionsPerUnitArea(fracture_guid_list, domain_length,
                                domain_width, domain_height)
        determines the length of intersections per unit area of the 3D medium
    """
    no_of_fracture_intersections = 0  # should be run after lengthofinter
    lengths_of_intersection_lines = []  # plot histogram with this

    def LengthOfIntersection(self, fracture_guid_list):
        """
        returns the sum of all length of intersections and helps to track
        the number of fracture intersections.
        
        Parameters
        ----------
        fracture_guid_list: list
            a list of fractures' guids in the network
        """
        # initialise length as 0
        length = 0
        # loop through all the fractures in the list
        for i in range(len(fracture_guid_list)):
            # fracture to test intersection against
            curveA = fracture_guid_list[i]
            # loop through all other fractures
            for j in range(len(fracture_guid_list)):
                # except the fractures we are testing against
                if j != i:
                    # test for intersection
                    intersection = rs.IntersectBreps(curveA, fracture_guid_list[j])
                    # if there is intersection
                    if intersection is not None:
                        for x in intersection:
                            # check it's a line!
                            if rs.IsLine(intersection[0]):
                                # increase no of fracture intersections
                                self.no_of_fracture_intersections += 1
                                # find the length of intersection
                                self.lengths_of_intersection_lines.append(rs.CurveLength(intersection[0]))
                                # increment the length
                                length += rs.CurveLength(intersection[0])
                # continue if i == j
                else:
                    continue
        return length

    def FracturesSurfaceArea(self, fracture_guid_list):
        """
        determines the total surface area of all fractures in the medium

        Parameters
        ----------
        fracture_guid_list: list
            a list of fractures' guids in the network
        """
        # function to determine the surface area of all fractures in the domain
        # initialise fracturs surface area
        fractures_surface_area = 0
        # loop to sum all areas of fractures
        for fracture in fracture_guid_list:
            # get surface area of the fracture
            fracture_area = rs.SurfaceArea(fracture)
            # increment the fractures surface area
            fractures_surface_area += fracture_area[0]
        return fractures_surface_area

    def FractureIntensity_P32(self, fracture_guid_list, domain_length, domain_width, domain_height):
        """
        function which returns the P_32 fracture intensity

        Parameters
        ---------
        fracture_guid_list: list
            a list of fractures' guids in the network
        domain_length: float
            length of the fracture medium
        domain_width: float
            width of the fracture medium
        domain_height: float
            height of the fracture medium
            
        Raises
        ------
        ValueError
            if the domain length, hright or width is not greater than 0.
        """
        # fractures_surface_area = 0
        try:
            if domain_length <= 0 or domain_width <= 0 or domain_height <= 0:
                raise ValueError
        except ValueError:
            print("FractureIntensity_P32(): The domain length, width\
                  and height should be greater than zero")
        else:
            domain_volume = domain_length * domain_width * domain_height
            # determine fractures surface area
            fractures_surface_area = self.FracturesSurfaceArea(fracture_guid_list)  
            return fractures_surface_area/domain_volume
         
    def IntersectionsPerUnitArea(self, fracture_guid_list, domain_length, domain_width, domain_height):
        """
        function to determine the length of intersections per unit area
            of the 3D medium
        
        Parameters
        ---------
        fracture_guid_list: list
            a list of fractures' guids in the network
        domain_length: float
            length of the fracture medium
        domain_width: float
            width of the fracture medium
        domain_height: float
            height of the fracture medium
        
        Raises
        ------
        ValueError
            if the domain length, hright or width is not greater than 0.
        """
        try:
            if domain_length <= 0 or domain_width <= 0 or domain_height <= 0:
                raise ValueError
        except ValueError:
            print("Intersections_per_unit_area(): The domain length, width\
                  and height should be greater than zero")
        else:
            domain_surface_area = 2((domain_length * domain_width) + (domain_length * domain_height) + (domain_width * domain_height))
            return self.LengthOfIntersection(fracture_guid_list)/domain_surface_area


class CutPlane:
    """
    A class for cur-plane analysis
    ......
    
    Attributes
    ----------
    plane: str
        desired plane for cut-plane analysis. should be uppercase
    width: float
        width of the cut-plane
    height: float
        height of the cut-plane
    GUID: guid
        guids of the cut plane
    intersecting_fractures: list
        list of fractures intersecting the cut plane

    Methods
    -------
    DrawPlane(dist, axis_of_rotation, angle_of_rotation)
        displays the cut plane on Rhino interface
    TotalLengthOfFractures(fracture_guid_list, cut_plane)
        returns sum of length of all fractures intersecting the plane
    NumberOfIntersectingFractures()
        returns the number of fractures on the plane
    FractureIntensity_P21(length_of_fractures)
        calculates and returns Fracture Intensity P_21
    PlaneLines(plane_guid)
        breaks the plane into lines and returns a list of guids of those
        lines
    IntersectionMatrix(boundary_list, intersected_fractures)
        prepares and returns the intersection matrix
    Percolate(initial_guid, target_guid, boundary_list,
              intersection_matrix, domain_fractures)
        determines the percolation state of the plane
    """
    def __init__(self, plane, width, height):
        """
        Parameters
        ----------
        plane: str
            desired plane for cut-plane analysis. should be uppercase
        width: float
            width of the cut-plane
        height: float
            height of the cut-plane
        """
        self.plane = plane  # plane should be in uppercase
        self.width = width
        self.height = height
        self.GUID = None
        self.intersecting_fractures = []
    
    def DrawPlane(self, dist, axis_of_rotation, angle_of_rotation):
        """
        function to draw the plane on Rhino interface. Returns the plane's
        Guid
        
        Parameters
        ----------
        dist: float
            dist to move away from y-axis (origin) if 'ZX' plane
            dist to move away from x-axis (origin) if 'YZ' plane
            dist to move away from z-axis (origin) if 'XY' plane
        axis_of_rotation: list
            list specifying axis of rotation on Rhino
            e.g. [1,0,0] is to rotate on x-axis
        angle_of_rotation: float
            angle to rotate the plane
        
        Raises
        ------
        ValueError
            if the argument 'dist' is less than than 0.
        """
        try:
            if dist < 0:
                raise ValueError
        except ValueError:
            print("draw_plane(): argument 'dist' should not be negative")
        else:
            if self.plane == 'XY':
                # axis for plane to be drawn
                myplane = rs.WorldXYPlane()
                # add a rectangle in the XY plane
                rec = rs.AddRectangle(myplane, self.width, self.height)
                # save the GUID of the plane
                self.GUID = rec
                # move the plane "dist" away from the z-axis
                # dist to move away from z-axis (origin)
                rs.MoveObject(rec, [0, 0, dist])
                # rotate plane
                rs.RotateObject(rec, [self.height/2, self.width/2, dist], angle_of_rotation, axis_of_rotation)
                # return the GUID of the plane
                return rec
            if self.plane == 'YZ':
                # axis for plane to be drawn
                myplane = rs.WorldYZPlane()
                # add a rectangle in the YZ plane
                rec = rs.AddRectangle(myplane, self.width, self.height)
                # save the GUID of the plane
                self.GUID = rec
                # dist to move away from x-axis (origin)
                rs.MoveObject(rec, [dist, 0, 0])
                # rotate plane
                rs.RotateObject(rec, [dist,dist,self.height/2], angle_of_rotation, axis_of_rotation)
                # return the GUID of the plane
                return rec
            if self.plane == 'ZX':
                # axis for plane to be drawn
                myplane = rs.WorldZXPlane()
                # add a rectangle in the XZ plane
                rec = rs.AddRectangle(myplane, self.width, self.height)
                # save the GUID of the plane
                self.GUID = rec
                # dist to move away from y-axis (origin)
                rs.MoveObject(rec, [0, dist, 0])
                # rotate plane
                rs.RotateObject(rec, [dist, dist, self.height/2], angle_of_rotation, axis_of_rotation)
                # return the GUID of the plane
                return rec
            
    def TotalLengthOfFractures(self, fracture_guid_list, cut_plane):
        """
        Function to intersect fractures and return the total length of
        fractures in the cut plane
        
        Parameters
        ----------
        fracture_guid_list: list
            list containing domain fractures' guids
        cut_plane: guid
            guid of the cut plane
        """
        # initialise length as 0
        length = 0
        # convert plane to a surface
        plane_surf = rs.AddPlanarSrf(cut_plane)
        # loop through the fractures' GUIDs
        for i in range(len(fracture_guid_list)):
            # perform intersection test
            intersection = rs.IntersectBreps(fracture_guid_list[i], plane_surf)
            # if there is intersection
            if intersection is not None:
                # go through the list
                for x in intersection:
                    # check it's a line!
                    if rs.IsLine(intersection[0]):
                        # add the GUID to class attribute
                        # 'intersecting_fractures'
                        self.intersecting_fractures.append(intersection[0])
                        # increment the length of intersecting fractures
                        length += rs.CurveLength(intersection[0])
        # delete the plane surface we added to Rhino interface
        rs.DeleteObject(plane_surf)
        # return the lotal lengths of intersection
        return length
    
    def NumberOfIntersectingFractures(self):
        """
        Function to return the number of fractures intersecting the cut plane
        
        parameters
        ----------
        None
        """
        return len(self.intersecting_fractures)
        
    def FractureIntensity_P21(self, length_of_fractures):
        """
        Function which calculates and returns Fracture Intensity P_21
        
        Parameters
        ----------
        length_of_fractures: float
            length of fractures intersecting the plane
        """
        return length_of_fractures/(self.width * self.height)
    
    def PlaneLines(self, plane_guid):
        """
        returns a list of GUIDs of the four lines forming the plane
        """
        return rs.ExplodeCurves(plane_guid)
        
    def IntersectionMatrix(self, boundary_list, intersected_fractures):
        """
        Function to perform fracture-fractrure intersection and 
        fracture-boundary intersection, then form an intersection matrix.
        
        Parameters
        ---------
        boundary_list: list
            list of GUIDs of the plane's boundaries
        intersected_fractures: list
            list of GUIDs of the intersecting fractures
        
        Raises
        ------
        TypeError
            if the arguments are not lists
        """
        try:
            if type(boundary_list) != list or type(intersected_fractures) != list:
                raise TypeError
        except TypeError:
                print("IntersectionMatrix(): The two arguments should\
                  be of type list")
        else:
            # initialize Matrix
            mat = []
            # number of fractures
            num_frac = len(intersected_fractures)
            # number of rows and cols for matrix
            n_row = num_frac + 4
            n_col = num_frac + 4
            # initialize matrix
            for i in range(n_row):
                mat.append([])
                for j in range(n_col):
                    mat[i].append(j)
                    mat[i][j] = 0
            # boundary to bounday taken care by the matrix initialization
            # fractures to fractures
            for i in range(num_frac):
                for j in range(num_frac):
                    if i != j:
                        intersection = rs.CurveCurveIntersection(intersected_fractures[i],intersected_fractures[j])
                        if intersection is not None:
                            mat[i][j] = 1
            # boundary-fractures
            for i in range(num_frac):  # 0 to number of fractures - 1
                # number of fractures to end of row/col
                for j in range(num_frac, n_col):
                    intersection = rs.CurveCurveIntersection(intersected_fractures[i],boundary_list[j-num_frac])
                    if intersection is not None:
                        # set the matrix elements to be 1
                        # since it is a symmetric matrix mat[i][j] == mat[j][i]
                        mat[i][j] = 1
                        mat[j][i] = 1
            # return the matrix
            return mat


def Percolate(self, initial_guid, target_guid, boundary_list, intersection_matrix, domain_fractures):
    """
    function to determine percolation state of the cut-palne (2D)
    
    Parameters
    ----------
    initial_guid: guid
        guid of the first boundary
    target_guid: guid
        guid of the second boundary
    intersection_matrix: matrix
        intersection matrix
    domain_fractures: list
        list of fractures intersecting the plane
        
    Raises
    ------
    TypeError
        if  arguments 'boundary_list' and 'domain_fractures' are not lists
    """
    try:
        if type(boundary_list) != list or type(domain_fractures) != list:
                raise TypeError
    except TypeError:
            print("Percolate(): arguments 'boundary_list' and 'domain_\
                  fractures' must be of type list")
    else:
        # object list
        obj_list = domain_fractures + boundary_list
        # list of other boundary guids other than the target ones.
        # This is necessary because of a case whereby, we are testing
        # percolation between boundaries A and B and a fracture inersects
        # boundaries A & C, another fracture intersects boundaries B & C
        # The function will return percolation as True, which is not
        # so we need to avoid adding the boundries to the list of fractures
        forbidden_list = [frac for frac in boundary_list if (frac != initial_guid and frac != target_guid)]
        # get index of init_guid in the boundary list
        p1 = [i for i in range(len(boundary_list)) if boundary_list[i] == initial_guid]
        # row of init_guid in the matrix
        # len(intersection_matrix[1]) = matrix row
        # len(boundary_list)  = number of boundarues
        # p1[0] = index of initial guid in the list
        b1 = p1[0] + len(intersection_matrix[1]) - len(boundary_list)
        # get index of target_guid in the boundary list
        p2 = [i for i in range(len(boundary_list)) if boundary_list[i] == target_guid]
        # row of init_guid in the matrix
        b2 = p2[0] + len(intersection_matrix[1]) - len(boundary_list)
        # check if all elements in the initial boundary row is zero
        all_num_row_b1 = all(elem == 0 for elem in intersection_matrix[b1][:])
        # check if all elements in the target boundary row is zero
        all_num_row_b2 = all(elem == 0 for elem in intersection_matrix[b2][:])
        # return false if either of the check above is True
        # It meas no fracture intersect either of the two
        # boundaries we want to check perfoclation for
        if all_num_row_b1 or all_num_row_b2:
            return False
        # initialise a list to store fractures matrix index
        # found along the path we are checking percolation
        index_list = [b1]
        # initialise a list to store fractures found along
        # the path we are checking percolation
        frac_list = [initial_guid]
        # k moves through the list of column index
        k = 0
        # old_len stores the length after one complete phase.
        # A phase here is when all the columns of fractures added have
        # searched for intersection. For instance, the first pahse
        # will be when all the columns of fractures added
        # to the inital boundary have been searched
        old_len = len(frac_list)
        # This is updated after each phase, to track when
        # a phase has been completed
        it = 0
        while True:
            # iterate through the col of the matrix
            for i in range(len(intersection_matrix[0])):
                # if any col of the boundary/fracture row is > 0
                # and the corresponding fracture is
                # not in the fracture intersection and forbidden list
                if (intersection_matrix[index_list[k]][i] > 0) and (obj_list[i] not in frac_list) and (obj_list[i] not in forbidden_list):
                    # append the fracture/oboundary in the
                    # fracture intersection list
                    frac_list.append(obj_list[i])
                    # append the index of the fracture added
                    index_list.append(i)
            # do for each phase
            if it == k:
                # track the number of fracture added
                num_added = len(frac_list) - old_len
                # if no fracture is added
                if num_added == 0:
                    # return False
                    return False
                # if fractures are added, increment "it" to track when
                # the phase is complete
                it += num_added
                # increment old_len to know the number of fractures
                # added after the phase
                old_len += num_added
            # if the target_guid(i.e second coundary) has been
            # appended in the frac intersection list
            # which indicates percolation
            if target_guid in frac_list:
                # return True
                return True
            # increment k
            k += 1


def IntersectionsPerFfracture(intersection_matrix):
    """
    function to print the number of intersections per fracture

    Parameter
    ---------
    intersection_matrix: matrix
        intersection matrix
    """
    # initilalise list
    inter_list = []
    # go through each row of the matrix and avoid boundaries
    for i in range(len(intersection_matrix)-6):
        # initialise number of intersection to be 0
        n = 0
        # go through all the columns of each row
        # avoid the last six elements, since they are boundary intersections
        for j in range(len(intersection_matrix[i][:-6])):
            # if the element is not 0, i.e it's an intersection
            if intersection_matrix[i][j] != 0:
                # increment the number of intersection
                n += 1
        # append the number of intersection for the fracture
        inter_list.append(n)
    # return the intersetion per fracture list
    return inter_list
