import numpy as np
import pandas as pd
import faiss
from utils.User import Vector
from utils.DataLoader import SQLReader, SQLWriter

class Database:
    def __init__(self, dimension, arrs=None):
        self.db = {}
        self.salted_db = {}
        self.faiss = faiss.IndexFlatL2(dimension)  # Using L2 distance for similarity
        self.sfaiss = faiss.IndexFlatL2(dimension)

        #load in preset arrays
        if arrs:
            self.faiss.add(arrs)

    def import_database(self):
        # Import vector data from MySQL
        reader = SQLReader(server="localhost", db="your_db_name", username="your_username", password="your_password")
        
        for tablename, dataframe in reader.data.items():
            if tablename.startswith("vector_"):
                key = int(tablename.split("_")[1])  # Assuming the table name format is "vector_{key}"
                vec = dataframe.to_numpy().flatten()  # Assuming each table contains a single vector
                self.insert(vec)  # Reusing the insert method to add vectors to both self.db and self.faiss
        
        #Load the FAISS index from a file
        self.faiss = faiss.read_index("data/faiss_database")
        self.sfaiss.read_index("data/faiss_database_salted")

    def export_database(self):
        writer = SQLWriter(db="unsalted", username="root", password="root", host="your_host")
        for key, vec in self.db.items():
            df = pd.DataFrame(vec.arr if hasattr(vec, 'arr') else vec).T  # Ensure vec is convertible to DataFrame
            tablename = f'vector_{key}'
            writer.write(df, tablename)
        
        # Serialize FAISS index to disk
        faiss.write_index(self.faiss, "data/faiss_database")
        faiss.write_index(self.sfaiss, "data/faiss_database_salted")

    """
    Finds the closest k matches to the passed array
    Returns: index of closest n-matches and distance
    Requires:
        arr - array to match
        k - number of closest matches
    """
    def find(self, arr, k=1):
        vec_arr = np.array(arr).astype('float32').reshape(1, -1)
        U_D, U_I = self.faiss.search(vec_arr, k)  # D is the distance, I is the index of the nearest neighbor
        S_D, S_I = self.sfaiss.search(vec_arr, k) #search salted database

        if k == 1:
            return (U_I[0][0], U_D[0][0]), (S_D[0][0], S_I[0][0])
        
        return (U_I[0], U_D[0]), (S_D[0], S_I[0]) # Returning index and distance of the most similar vector
    
    """
    Inserts a new vector into the dict and faiss
    Returns: N/A
    Requires:
        arr - str arr to be added to db
    """
    def insert(self, arr, profile=None):
        #create new vector object based on arr-string
        vec = Vector(arr)
        if profile is not None:
            profile.add_vector(vec)

        #Add the new vector to the dict
        self.db[self.faiss.ntotal] = vec
        self.db[self.sfiass.ntotal] = vec

        # Convert the array to a NumPy array and ensure it is two-dimensional
        new_vector_arr = np.array(vec.arr).astype('float32').reshape(1, -1)
        
        # Add the new vector to the FAISS index
        self.faiss.add(new_vector_arr)
        self.sfaiss.add(new_vector_arr)

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
