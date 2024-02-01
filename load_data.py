import os
import logging
import csv
import pandas as pd
import mysql.connector as sql

###LOGGING SETUP###
logging.basicConfig(filename="csvLoad.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.DEBUG)
logger = logging.getLogger()

###PATH TO DATA####
PATH = 'data'

"""
Class for loading files from .csv format
"""
class CSVReader:
    def __init__(self, path=PATH, autoload=True):
        #allow for path specification
        PATH = path

        #dict to store data based on <filename, df> pair 
        self.data = {}

        if autoload:
            self.info(" ====START OF LOG====") #start of logging session

            #get files from the data directory
            files = self.get_files()
            logger.debug("FILENAMES :" +  str(files))

            #loop through files
            for i in range(0, len(files), 2):
                #get headers for given file
                headers = self.get_headers(files[i+1])
                logger.debug("FOR : %s, HEADERS : %s", files[i], str(headers))

                #get data for given file
                file_data = self.get_data(files[i], headers)
                logger.debug

                #append to data dictionary
                self.data[files[i]] = file_data
                logger.debug("%s ==> DATA PROSESSED AND ADDED", files[i])

            logger.info("====END OF LOG==== \n")
            return

        return

    """
    Gets all specified csv filenames from a directory
    Directory is set by global PATH variable
    Returns: files as list of strings
    Requires: N/A
    """
    def get_files(self):
        files = os.listdir(PATH)

        for file in files:
            if '.csv' not in file:
                files.remove(file)
        return files

    """
    Gets the header name from row value of first column
    Returns: headers as a list of strings
    Requires: filename (as a csv) 
    """
    def get_headers(self, filename):
        with open(str(PATH + '/' + filename), newline='\n') as file:
            reader = csv.reader(file, delimiter=',')
            headers = []
            for row in reader:
                headers.append(row[0])
            
        headers.pop(0)

        return headers

    """
    @TODO: This is having issues with dimensions. Find a better way to specify.
    Converts csv to pandas df with appropriate headers
    Returns: Pandas Dataframe of csv file
    Requires: filename - csv file, headers - string list of column headers
    """
    def get_data(self, filename, headers):
        return pd.read_csv(str(PATH + '/' + filename), names=headers, encoding='latin1', quotechar='"')

"""
Class for loading files from .sql format
"""
class SQLReader:
    def __init__(self, server="localhost", db="*", username="root", psswd="", path=PATH):
        #allow for path specification
        PATH = path

        #dict to store data based on <filename, df> pair 
        self.data = {}

        #create new db
        if db == "*":
            #connect to the server & open cursor
            db = sql.connect(user=username, password=psswd, host=server)
            cursor = db.cursor()
            logger.info("Connected to %s" + str(server))

            files = self.get_files()
            for file in files:
                try:
                    self.load_sql()
                    logger.debug("Database created for " + str(file) + " on " + str(server))
                except:
                    logger.error("Failed to create database : " + file)

        #connect to existing db
        else:
            try:
                #connect to SQLServer & open a cursor
                db = sql.connect(user=username, password=psswd, host=server, database=db)
                cursor = db.cursor()
                logger.debug("Connected to databse : " + str(db))

                data[db] = self.read_data()
            except:
                logger.error("Cannot connect to database : " + str(db))

    """
    Gets all specified sql filenames from a directory
    Directory is set by global PATH variable
    Returns: files as list of strings
    Requires: N/A
    """
    def get_files(self):
        files = os.listdir(PATH)

        for file in files:
            if '.sql' not in file:
                logger.debug("Removing file : " + str(file))
                files.remove(file)

        return files

    """
    Reads from existing db and adds the contents to data
    Requires: 
    Returns: 
    """
    def read_data(self, databse, filename):
        return



def main():
    logger.info(" ====START OF LOG====") #start of logging session

    loader = CSVLoader()

    #get files from the data directory
    files = loader.get_files()
    logger.debug("FILENAMES :" +  str(files))

    #loop through files
    for i in range(0, len(files), 2):
        #get headers for given file
        headers = loader.get_headers(files[i+1])
        logger.debug("FOR : %s, HEADERS : %s", files[i], str(headers))

        #get data for given file
        file_data = loader.get_data(files[i], headers)
        logger.debug

        #append to data dictionary
        loader.data[files[i]] = file_data
        logger.debug("%s ==> DATA PROSESSED AND ADDED", files[i])

    logger.info("====END OF LOG==== \n")

if __name__ == "__main__":
    main()