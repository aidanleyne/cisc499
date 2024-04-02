"""
Profile object to identify user
"""
class Profile:
    def __init__(self, id):
        self.vectors = []
        self.id = id

    """
    Creates link between vector and profile
    Returns: N/A
    Requires:
        vec - vector to be linked to profile
    """
    def add_vector(self, vec):
        self.vectors.append(vec)
        vec.profile = self
    
"""
Vector class to store output from model
"""
class Vector:
    def __init__(self, arr, str=False):
        if str:
            self.arr = self.populate(arr)
        else:
            self.arr = arr
        self.profile = None

    """
    Takes a comma seperated string of ints to populate the array
    Returns: int vector
    Requires:
        str - css of ints
    """
    def populate(self, str):
        return [float(x) for x in str.split(',')]
    
    """
    Compares two vectors. Defaults to self if only one passed
    Returns: true/false
    Requires:
        vec1 - vector to be compared
        Optional: vec2 - vector instead of this one
    """
    def isEqual(self, vec1, vec2=None):
        if vec2 == None:
            vec2 = self

        return vec1.arr == vec2.arr
    
    """
    Compares if a value is correct at a given position
    Returns: -1 if OOR, true/false otherwise
    Requires:
        value - value to be compared
        pos - position in the vector
        Optional: vec - vector object
    """
    def compare(self, value, pos, vec=None):
        if vec == None:
            vec = self
        
        if len(vec.arr) < pos or pos < 0:
            return -1
        
        return vec.arr[pos] == value