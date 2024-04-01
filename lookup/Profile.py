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
    

def main():
    pass

if __name__ == "__main__":
    main()