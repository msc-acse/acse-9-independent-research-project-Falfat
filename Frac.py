import rhinoscriptsyntax as rs


class Fracture():
    """
    A class for fracture objects

    Attributes
    ----------
    fracture_name: str
        name of the fracture
    fracture_GUID: guid
        guid of fracture
    fracture_center: list
        center of fracture

    Methods
    -------
    intersect(other)
        checks if a fracture intersects another
    """
    fracture_name = None
    fracture_GUID = None
    fracture_center = None

    def Intersect(self, other):
        """
        function to check if a fracture intersects another

        Parameter
        -------
        other: guid
            guid of the second fracture
        """
        # inputs are frcature instances in fracture list
        curveA = self.fracture_GUID
        # check for intersection
        intersection = rs.IntersectBreps(curveA, other.fracture_GUID)
        # if no intersection
        if intersection is None:
            print('The fractures do not intersect')
        else:
            # go through the list of intersection
            for x in intersection:
                # check it's a line!
                if rs.IsLine(intersection[0]):
                    # get intersection length
                    length = rs.CurveLength(intersection[0])
                    # print a statement
                    print('Fracture intersect, the length of intersection\
                          is:', length)


def OldFracturesGuids(fracture_list):
    """
    Function to return the list of old guids of fractures in the domain
    before trimming

    Parameter
    --------
    fracture_list: list
        list of fracture objects
    """
    list = [fracture_list[i].fracture_GUID for i in range(len(fracture_list))]
    return list


def NewFracturesGuids(dom_new_fractures, fracture_list):
    """
    function to swap old guids to new ones in fracture objects
    and return new guids.
    Deletes previous fractures and swap the layers of new fractures
    with those of old ones

    Parameter
    --------
    fracture_list: list
        list of old fracture objects
    dom_new_fractures: list
        list of new fracture objects
    """
    # initialise list for guids
    guids = []
    for i in range(len(fracture_list)):
        # delete previous fractures
        rs.DeleteObject(fracture_list[i].fracture_GUID)
        # change the guid of our fracture instances
        fracture_list[i].fracture_GUID = dom_new_fractures[i]
        guids.append(dom_new_fractures[i])
        # put new fractures in old layers
        rs.ObjectLayer(dom_new_fractures[i], fracture_list[i].fracture_name)
    return guids
