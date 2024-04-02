import numpy as np
import faiss
from lookup.User import Vector

class Database:
    def __init__(self, dimension, arrs=None):
        self.db = {}
        self.faiss = faiss.IndexFlatL2(dimension)  # Using L2 distance for similarity

        #load in preset arrays
        if arrs:
            self.faiss.add(arrs)

    def import_database(self):
        pass

    def export_database(self):
        pass

    """
    Finds the closest k matches to the passed array
    Returns: index of closest n-matches and distance
    Requires:
        arr - array to match
        k - number of closest matches
    """
    def find(self, arr, k=1):
        vec_arr = np.array(arr).astype('float32').reshape(1, -1)
        D, I = self.faiss.search(vec_arr, k)  # D is the distance, I is the index of the nearest neighbor
        
        return I[0], D[0] # Returning index and distance of the most similar vector
    
    """
    Inserts a new vector into the dict and faiss
    Returns: N/A
    Requires:
        arr - str arr to be added to db
    """
    def insert(self, arr, str=False, profile=None):
        #create new vector object based on arr-string
        vec = Vector(arr, str)
        if profile:
            profile.add_vector(vec)

        #Add the new vector to the dict
        self.db[self.faiss.ntotal] = vec

        # Convert the array to a NumPy array and ensure it is two-dimensional
        new_vector_arr = np.array(vec.arr).astype('float32').reshape(1, -1)
        
        # Add the new vector to the FAISS index
        self.faiss.add(new_vector_arr)

def main():
    test = np.random.random((100000, 256)).astype('float32')

    #test database initialization
    database = Database(256)
    i = 1
    for arr in test:
        database.insert(arr)
        i+=1
    print("Database created")

    #print first vector in db
    print(database.db[0])

    #test find 10 matching vectors
    result = database.find(np.random.random((1, 256)).astype('float32'), 10)
    print(result)
    for item in result[0]:
        print('\t', 'rank :', database.db[item].arr)

if __name__ == "__main__":
    main()
