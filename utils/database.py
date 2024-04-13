import numpy as np
import pandas as pd
import faiss
from utils.User import Vector, Profile
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

    """
    Imports the databases to their respective locations
    Returns: N/A
    Requires: N/A
    """
    def import_database(self):
        # Import vector data from MySQL
        reader = SQLReader(server="localhost", db="cisc499", uname="integration", psswd="cisc499")
        cursor = reader.cursor

        #read the database for salted vectors
        cursor.execute("SELECT position, user_id, array FROM salted_vectors")
        data = cursor.fetchall()

        for position, profile_id, array_str in data:
            arr = list(map(float, array_str.split(',')))
            vec = Vector(arr)
            self.salted_db[position] = vec
            pf = Profile(profile_id)
            pf.add_vector(vec)

        #read the database for unsalted vectors
        reader.connection.commit()
        cursor.execute("SELECT position, user_id, array FROM unsalted_vectors")
        data = cursor.fetchall()

        for position, profile_id, array_str in data:
            arr = list(map(float, array_str.split(',')))
            vec = Vector(arr)
            self.db[position] = vec
            pf = Profile(profile_id)
            pf.add_vector(vec)

        reader.close()

        #Load the FAISS index from a file
        try:
            self.faiss = faiss.read_index("data/faiss_database")
        except:
            print("No unsalted database present.")

        try:
            self.sfaiss = faiss.read_index("data/faiss_database_salted")
        except:
            print("No salted database present.")

    """
    Exports the databases to their respective locations
    Returns: N/A
    Requires: N/A
    """
    def export_database(self):
        writer = SQLWriter(server="localhost", db="cisc499", uname="integration", psswd="cisc499")
        conn = writer.connection
        cursor = writer.cursor

        for key, vec in self.salted_db.items():
            array_str = ','.join(map(str, vec.arr))
            query = "INSERT IGNORE INTO salted_vectors (position, user_id, array) VALUES (%s, %s, %s)"
            cursor.execute(query, (key, vec.profile.id, array_str))

        conn.commit()

        for key, vec in self.db.items():
            array_str = ','.join(map(str, vec.arr))
            query = "INSERT IGNORE INTO unsalted_vectors (position, user_id, array) VALUES (%s, %s, %s)"
            cursor.execute(query, (key, vec.profile.id, array_str))

        conn.commit()
        writer.close()
        
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
        S_D, S_I = self.sfaiss.search(vec_arr, k) # search salted database

        if k == 1:
            return (U_I[0][0], U_D[0][0]), (S_I[0][0], S_D[0][0])
        
        return (U_I[0], U_D[0]), (S_I[0], S_D[0]) # Returning index and distance of the most similar vector
    
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
        self.salted_db[self.sfaiss.ntotal] = vec

        # Convert the array to a NumPy array and ensure it is two-dimensional
        new_vector_arr = np.array(vec.arr).astype('float32').reshape(1, -1)
        
        # Add the new vector to the FAISS index
        self.faiss.add(new_vector_arr)
        self.sfaiss.add(new_vector_arr)
