"""
Profile object to identify user
"""
class Profile:
    def __init__(self, id='test'):
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
    def __init__(self, arr):
        self.arr = arr
        self.profile = None
