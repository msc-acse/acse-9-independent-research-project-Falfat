import rhinoscriptsyntax as rs
import Input

name = "DataFile.txt"
radius, boxlength, n, fracture_shape = Input.ReadFile(name)


class Domain:
    """
    A class to represent the farcture network domain.
    .....

   Attributes
   ----------
   length: float
       the length of the fracture domain.
   surface area: float
       total surface area of the fracture domain.
   type: str
       domain shape (default is cube)
   center: list
       center of the domain in 3D space.
   my_fractures: list
       GUIDs of all the fractures persent in the domain.

    Methods
    -------
    Show()
        displays the domain on Rhino interface
    NumberOfFractures()
        returns the total number of fractures in the domain
    CreateBoundary(box_side_length)
        creates boundary for trimming out of bounds fractures.
        An auxilliary method to trim extruding fractures.
    GetSurfaceFromFractureLayer(layer_name)
        gets surfaces from layer and returns the surfaces.
        An auxilliary method to trim extruding fractures.
    ConvertPolysurfaceToSurface(polysurface)
        converts polysurfaces to surface and returns False and surface
        if the argument is a polysurface. Returns True and the argument
        type if it is not a polysurface.
        An auxilliary method to trim extruding fractures.
    CreateSetOfExtendedBoundaries(boundaries)
        creates some extened boundaries to check for out of bounds fractures.
        An auxilliary method to trim extruding fractures.
    RemoveSurfacesIfAnyIntersectBoundary(surf, boundaries)
        checks if a surface intersects the boundary and deletes the surface
        An auxilliary method to trim extruding fractures.
    RemoveSurfacesOutsideOfBox(b_length)
        Main method which calls all auxilliary functions to trim out of bounds
        fractures.
    IntersectionMatrix(boundary_list, domain_fractures)
        method to create a square intersection matrix for fracture-fracture
        and fracture-boundary intersections. Returns the matrix.
    Percolate(initial_guid, target_guid, boundary_list, intersection_matrix,
              domain_fractures)
        method to determine percolation state of the domain. returns a bool.
    """
    def __init__(self, length):
        """
        Parameters
        ----------
        length: float
            the length of the fracture domain.
        """
        self.length = length
        self.surface_area = 6*length**2
        self.volume = length**3
        self.type = 'cube'
        self.center = [length/2, length/2, length/2]
        self.my_fractures = []

    def Show(self):
        """
        displays the domain on the Rhino user interface.

        Parameters
        ----------
        None
        """
        corners = ([(0, 0, 0), (self.length, 0, 0),
                    (self.length, self.length, 0), (0, self.length, 0),
                    (0, 0, self.length), (self.length, 0, self.length),
                    (self.length, self.length, self.length),
                    (0, self.length, self.length)])
        return rs.AddBox(corners)

    def NumberOfFractures(self):
        """
        returns the number of fractures in the domain

        Parameters
        ----------
        None
        """
        return len(self.my_fractures)

    def CreateBoundary(self, box_side_length):
        """
        creates some extened boundaries to check for out of bounds fractures.
        An auxilliary method to trim extruding fractures.

        Parameters
        ----------
        box_side_length: str
            the domain length

        Raises
        ------
        ValueError
            if the box length is not > 0.
        """
        try:
            if box_side_length <= 0:
                raise ValueError
        except ValueError:
            print("CreateBoundary(): The box side length should be\
                  greater than 0")
        else:
            # Put boundary layers in a new layer
            boundary_layer_name = "Boundaries"

            # To make sure we do not overwrite existing boundary surfaces,
            # delete the old layer if it is there

            # To avoid error messages about deleting current layers:
            rs.AddLayer('Blank Layer')
            rs.CurrentLayer('Blank Layer')
            if rs.IsLayer(boundary_layer_name):
                rs.PurgeLayer(boundary_layer_name)  # Deletes layer

            rs.AddLayer(boundary_layer_name)
            rs.CurrentLayer(boundary_layer_name)
            rs.LayerColor(boundary_layer_name, [0, 0, 0])

            L = box_side_length
            # L = distance from 0 to corner along each axis

            # Make corner points on boundaries
            # Delete them later
            bps = []
            bps.append(rs.AddPoint((0, 0, 0)))   # p0
            bps.append(rs.AddPoint((L, 0, 0)))  # p1
            bps.append(rs.AddPoint((L, L, 0)))  # p2
            bps.append(rs.AddPoint((0, L, 0)))  # p3
            bps.append(rs.AddPoint((L, 0, L)))    # p4
            bps.append(rs.AddPoint((L, L, L)))   # p5
            bps.append(rs.AddPoint((0, L, L)))  # p6
            bps.append(rs.AddPoint((0, 0, L)))   # p7

            # Make surfaces which are the boundaries
            bsurfs = []
            bsurfs.append(rs.AddSrfPt([bps[0], bps[1], bps[2], bps[3]]))  # s0
            bsurfs.append(rs.AddSrfPt([bps[4], bps[5], bps[6], bps[7]]))  # s1
            bsurfs.append(rs.AddSrfPt([bps[0], bps[1], bps[4], bps[7]]))  # s2
            bsurfs.append(rs.AddSrfPt([bps[1], bps[2], bps[5], bps[4]]))  # s3
            bsurfs.append(rs.AddSrfPt([bps[2], bps[3], bps[6], bps[5]]))  # s4
            bsurfs.append(rs.AddSrfPt([bps[3], bps[0], bps[7], bps[6]]))  # s5

            # Remove points as they are not needed
            rs.DeleteObjects(bps)
            # Return these boundaries for use elsewhere
            return bsurfs

    def GetSurfaceFromFractureLayer(self, layer_name):
        """
        gets surfaces from fracture layer and returns the surfaces.
        An auxilliary method to trim extruding fractures.

        Parameters
        ----------
        layer_name: str
            name of frature layer
        """
        surfs = []  # Will add found surfaces here

        # Don't try if the layer does not exist
        if rs.IsLayer(layer_name):
            # Get all identifiers for objects in the layer
            allobs = rs.ObjectsByLayer(layer_name)
            for i in allobs:
                if rs.IsSurface(i):  # If this object is a surface
                    surfs.append(i)  # Add to list
        return surfs

    def ConvertPolysurfaceToSurface(self, polysurface):
        """
        converts polysurfaces to surface and returns False and surface
        if the argument is a polysurface. Returns True and the argument
        type if it is not a polysurface. Polysurfaces are made by SplitBrep
        We can't use normal functions on them. So, we have to turn them
        into seperate surfaces with ExplodePolysurfaces. SplitBrep function is
        used in RemoveSurfacesOutsideOfBox().
        An auxilliary method to trim extruding fractures.

        Parameters
        ----------
        ploysurface: GUID
            guid of a Rhino surface
        """
        # Confirm this is a polysurface
        if rs.ObjectType(polysurface) != 16:
            return [False, [polysurface]]  # false, not a ploysurface
        # unjoins the polysurface and get identifiers of he separate surfaces
        surfaces = rs.ExplodePolysurfaces(polysurface)

        # Sometimes, the function ExplodePolysurfaces makes polysurfaces.
        # If it did, call this function again on those surfaces!
        non_poly_surfaces = []
        for surf in surfaces:
            # check if polysurface was created instead of surface
            if rs.ObjectType(surf) == 16:
                # convert the object to surface using its GUID once more,
                # incase polysurface was created
                # NB: RECURSIVE
                additional_split_surfaces = ConvertPolysurfaceToSurface(surf)[1]
                for new_surf in additional_split_surfaces:
                    non_poly_surfaces.append(new_surf)
                    # self.new_fractures.append(new_surf)
            else:
                non_poly_surfaces.append(surf)
                # self.new_fractures.append(surf)

        # Delete the old polysurface
        rs.DeleteObject(polysurface)

        return [True, non_poly_surfaces]

    def CreateSetOfExtendedBoundaries(self, boundaries, b_length):
        """
        creates some extened boundaries to check for out of bounds fractures.
        Returns the extended boundaries
        An auxilliary method to trim extruding fractures.
        
        Parameters
        ----------
        boundaries: list 
            list of boundaries to be extended
        """
        # A fairly basic way to check if a surface is outside of the boundary
        # is to make a set of additional boundaries which go beyond the
        # current boundaries. This is not perfect as it cannot guarantee
        # to get all the surfaces And requires many more intersection test
        extended_boundary_surfaces = []
        # The boundaries are created by scaling up the other boundaries
        distances = [1.001, 1.01, 1.1]
        origin = [b_length/2,b_length/2,b_length/2]
        for dist in distances:
            for boundary in boundaries:
                extended_boundary_surfaces.append(rs.ScaleObject(boundary, origin,[dist, dist, dist], True))

        return extended_boundary_surfaces
     
    def RemoveSurfacesIfAnyIntersectBoundary(self, surf, boundaries):
        """
        checks if a surface intersects the boundary and deletes the surface
        An auxilliary method to trim extruding fractures.
        
        Parameters
        ----------
        surf: GUID
            guid of a Rhino surface
        boundaries: list
            list of boundary guids
        """
        # Checks if a surface intersects a boundary
        # If so, it deletes it and any created intersections
        # Could run this with any set of boundary surfaces
        # Intended to run with the CreateSetOfExtendedBoundaries function
        for boundary in boundaries:
            intersections = (rs.IntersectBreps(boundary, surf))
            if intersections is not None:  # If there are intersections
                # Delete this surface
                rs.DeleteObject(surf)
                # delete the surface from domain fractures list
                self.my_fractures.remove(surf)
                # Delete all created intersections
                for inter in intersections:
                    rs.DeleteObject(inter)
                return True  # WHY RETURN TRUE AND FALSE?
        return False

    def RemoveSurfacesOutsideOfBox(self, b_length):
        """
        Main method which calls all auxilliary functions to trim out of bounds
        fractures.

        Parameter
        --------
        b_length: float
            length of domain/boundary
            
        Raises
        ------
        ValueError
            if boundary length is less than zero.
        """
        try:
            if b_length <= 0:
                raise ValueError
        except ValueError:
            print("Value of boundary should be greater than 0")
        else:
            # Create boundary surfaces
            boundaries = self.CreateBoundary(b_length)
            # Get all layers in the document
            all_layers = rs.LayerNames()
            # To avoid error messages about deleting current layers:
            # make a blank layer
            rs.AddLayer('Blank Layer')
            rs.CurrentLayer('Blank Layer')
            # Make a layer for intersecting fractures
            boundary_intersection_layer = "Boundary_Intersections"
            if rs.IsLayer(boundary_intersection_layer):
                rs.PurgeLayer(boundary_intersection_layer)  # Deletes layer
            # make boundary_intersection_layer the current layer
            rs.AddLayer(boundary_intersection_layer)
            rs.CurrentLayer(boundary_intersection_layer)
            rs.LayerColor(boundary_intersection_layer, [200, 0, 0])
            # Make a polysurface of all the boundaries
            # This polysurf can be used with SplitBrep
            # If you compare surfaces individually, then fractures which
            # intersect more than one surface (i.e. corners)
            # do not get split correctly.
            box = rs.JoinSurfaces(boundaries)
            all_surfaces = [] 
            # Go over all the layers to find fractures 
            for layer in all_layers:
                # Only act if layer is a fracture layer
                # Some layers have short names, so ask for 1st 
                # letter first, then rest
                if layer[0] == 'F': 
                    if layer[0:8] == 'FRACTURE':
                        # Get surfaces in this layer
                        surfs = self.GetSurfaceFromFractureLayer(layer)
                        for surf in surfs:  # BUT SURFS IS JUST A GUID
                            all_surfaces.append(surf)
            all_new_surfaces = []  # Store the split surfaces of the fractures
            # print "Number of surfaces examined for splitting: ",
            # len(all_surfaces)
            for surf in all_surfaces:
                # Run intersection test
                boundaries_touched = 0
                # for boundary in boundaries:
                # Use splitbrep here to split the fracture
                # surfaces by the boundaries directly
                # Brings back a polysurf which must be converted into a surface
                new_polysurfs = rs.SplitBrep(surf, box)
                if type(new_polysurfs) == list:
                    boundaries_touched += 1
                    for polysurf in new_polysurfs:
                        # Because sometimes there are multiple surfaces
                        new_surfs = self.ConvertPolysurfaceToSurface(polysurf)
                        for new_surfs_i in new_surfs[1]:
                            all_new_surfaces.append(new_surfs_i)
                            # append to domain fracture list
                            self.my_fractures.append(new_surfs_i)
                if boundaries_touched == 0:
                    # This means the fracture didn't intersect a boundary
                    # Add it to the list as well, so the final layer
                    # has all the fracs
                    copied_surf = rs.CopyObject(surf)
                    rs.ObjectLayer(copied_surf, boundary_intersection_layer)
                    # ARE WE APPENDING THE FRAC OUTSIDE OR INSIDE
                    all_new_surfaces.append(copied_surf)
                    # append to domain fracture list
                    self.my_fractures.append(copied_surf)
            # print "Number of surfaces after splitting: ",
            # len(all_new_surfaces)
            # Make extended boundary surfaces to check
            ext_boundaries = self.CreateSetOfExtendedBoundaries(boundaries, b_length)
            # Now, remove any surfaces which aren't inside the volume
            for surf in all_new_surfaces:
                self.RemoveSurfacesIfAnyIntersectBoundary(surf, ext_boundaries)
            # We don't need the extra boundaries anymore
            for boundary in ext_boundaries:
                rs.DeleteObject(boundary)
            for boundary in boundaries:
                rs.DeleteObject(boundary)
            rs.DeleteObject(box)
            return

    def IntersectionMatrix(self, boundary_list, domain_fractures):
        """
        method to create a square intersection matrix for fracture-fracture
        and fracture-boundary intersections. Returns the matrix.

        Parameters
        ----------
        boundary_list: list
            list of boundary guids
        domain_fractures: list
            list of fractures guids contained in the domain

        Raises
        -----
        TypeError
            if the arguments are not of type list
        """
        try:
            if type(boundary_list) != list or type(domain_fractures) != list:
                raise TypeError
        except TypeError:
            print("The two arguments should be of type list")
        else:
            # initialise a Matrix
            mat = []
            # number of fractures
            num_frac = len(domain_fractures)
            # number of rows and cols for matrix
            n_row = num_frac + 6
            n_col = num_frac + 6
            # append to matrix
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
                        intersection = rs.IntersectBreps(domain_fractures[i],domain_fractures[j])
                        if intersection is not None:
                            # set the matrix elements to be
                            # length of intersection
                            # since it is a symmetric matrix
                            # mat[i][j] == mat[j][i]
                            mat[i][j] = rs.CurveLength(intersection[0])
                            mat[j][i] = rs.CurveLength(intersection[0])
            # boundary-fractures
            for i in range(num_frac):  # 0 to number of fractures - 1
                # number of fractures to end of row/col
                for j in range(num_frac, n_col):
                    intersection = rs.IntersectBreps(domain_fractures[i], boundary_list[j-num_frac])
                    if intersection is not None:
                        # set the matrix elements to be length of intersection
                        # since it is a symmetric matrix mat[i][j] == mat[j][i]
                        mat[i][j] = rs.CurveLength(intersection[0])
                        mat[j][i] = rs.CurveLength(intersection[0])
            # return matrix
            return mat
    
    def Percolate(self, initial_guid, target_guid, boundary_list,
                  intersection_matrix, domain_fractures):
        """
        method to determine percolation state of the domain. returns a bool.
        
        Parameters
        ----------
        initial_guid: guid
            guid of the first side to check for percolation
        target_guid: guid
            guid of the second side to check for percolation
        boundary_list: list
            list of boundary guids
        intersection_matrix: matrix
            matrix of fracture-fracture and fracture-boundary intersections
        domain_fractures: list
            list of fractures guids contained in the domain
        """
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
        # print("B1 has no intersection",all_num_row_b1)
        # check if all elements in the target boundary row is zero
        all_num_row_b2 = all(elem == 0 for elem in intersection_matrix[b2][:])
        # return false if either of the check above is True
        # It meas no fracture intersect either of the
        # two boundaries we want to check perfoclation for
        if all_num_row_b1 or all_num_row_b2:
            return False
        # initialise a list to store fractures matrix index found
        # along the path we are checking percolation
        index_list = [b1]
        # initialise a list to store fractures found along the path
        # we are checking percolation
        frac_list = [initial_guid]
        # k moves through the list of column index
        k = 0
        # old_len stores the length after one complete phase.
        # A phase here is when all the columns of fractures added have
        # searched for intersection. For instance, the first pahse will
        # be when all the columns of fractures added
        # to the inital boundary have been searched
        old_len = len(frac_list)
        # This is updated after each phase, to track when a phase
        # has been completed
        it = 0
        while True:
            # iterate through the col of the matrix
            for i in range(len(intersection_matrix[0])):
                # if any col of the boundary/fracture row is > 0
                # and the corresponding fracture is
                # not in the fracture intersection list
                if (intersection_matrix[index_list[k]][i] > 0) and (obj_list[i] not in frac_list) and (obj_list[i] not in forbidden_list):
                    # append the fracture/boundary in the fracture
                    # intersection list
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


if __name__ == "__main__":
    dom = Domain(boxlength)
    print(Domain.number_of_fractures)
    ids = dom.Show()
    print(dom.type)
