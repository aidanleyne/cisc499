import numpy as np
import logging
import faiss
from Vector import Vector

class Database:
    def __init__(self, vectors=None):
        dimension = 256  # Assuming each vector has 256 floats
        self.index = faiss.IndexFlatL2(dimension)  # Using L2 distance for similarity
        
        # Convert Vector objects to a numpy array
        vector_arrays = np.array([vector.arr for vector in vectors]).astype('float32')
        
        # Adding the vectors to the index
        self.index.add(vector_arrays)

    def find(self, vec):
        vec_arr = np.array(vec.arr).astype('float32').reshape(1, -1)
        
        k = 1  # Number of nearest neighbors to find
        D, I = self.index.search(vec_arr, k)  # D is the distance, I is the index of the nearest neighbor
        
        return I[0][0], D[0][0]  # Returning index and distance of the most similar vector
    
    def insert(self, vec):
        # Convert the Vector object to a NumPy array
        new_vector_arr = np.array(vec.arr).astype('float32').reshape(1, -1)
        
        # Add the new vector to the FAISS index
        self.index.add(new_vector_arr)



def main():
    databse = Database()

if __name__ == "__main__":
    main()
