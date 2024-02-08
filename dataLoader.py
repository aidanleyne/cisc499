import os
import sys
import logging
import csv
import pandas as pd
import mysql.connector as sql

###LOGGING SETUP###
logging.basicConfig(filename="dataLoader.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.DEBUG)
logger = logging.getLogger()

###self._PATH TO DATA####
PATH = 'data'

"""
Class for loading files from .csv format
"""
class CSVReader:
    def __init__(self, path=PATH, autoload=True):
        #allow for path specification
        self._PATH = path

        #dict to store data based on <filename, df> pair 
        self.data = {}

        if autoload:
            logger.info("====START OF LOG====") #start of logging session

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
        files = os.listdir(self._PATH)

        cleaned = []

        for file in files:
            if file.endswith('.csv'):
                cleaned.append(file)
                logger.debug("File retained : " + str(file))

            else:
                logger.debug("Incorrect file type removed. File : " + str(file))
            
        return cleaned

    """
    Gets the header name from row value of first column
    Returns: headers as a list of strings
    Requires: filename (as a csv) 
    """
    def get_headers(self, filename):
        with open(str(self._PATH + '/' + filename), newline='\n') as file:
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
        return pd.read_csv(str(self._PATH + '/' + filename), names=headers, encoding='latin1', quotechar='"')

"""
Class for writing files to .csv format
"""
class CSVWriter:
    def __init__(self, data, path=PATH):
        #allow for path specification
        self._PATH = path

        self.info("====START OF LOG====") #start of logging session

        for table in data:
            df = data[table]
            logger.debug("Selected data for table : " + str(table))
            
            if not table.endswith('.csv'):
                table = table + '.csv'
                logger.debug("Added .csv to : " + str(table))

            try:
                df.to_csv(table, encoding='utf-8', index=False)
                logger.debug("Data successfully written to : " + str(table))
            except:
                logger.error("Issue writing data for : " + str(table))
                pass

        logger.info("====END OF LOG==== \n") 
        return

"""
Class for reading files from tab-delimited format
"""
class TSVReader:
    def __init__(self, path=PATH):
        #allow for path specification
        self._PATH = path

        self.data = {}

        logger.debug("====START OF LOG====") #start of logging session

        files = self.get_files()
        logger.debug("Begining Import on " + str(len(files)) + " files...")

        for file in files:
            #read file into pandas df and append to dict
            self.data[file] = self.load(file)
            #logger.debug("Read in file : " + str(file))

        #logger.debug("All data in " + str(self._PATH) + " processed")
        logger.debug("Data-dictionary is of length : " + str(len(self.data)))

        logger.info("====END OF LOG==== \n")
        return
    
    """
    Loads a file into a dataframe given a filename
    Requires: filename
    Returns: Pandas dataframe
    """
    def load(self, filename):
        try:
            return pd.read_csv(str(self._PATH + '/' + filename), header=0, delimiter='\t')
        except:
            logger.error("Could not parse file : " + filename)
            return None

    """
    Gets all specified txt filenames from a directory
    Directory is set by global self._PATH variable
    Returns: files as list of strings
    Requires: N/A
    """
    def get_files(self):
        files = os.listdir(self._PATH)

        cleaned = []

        for file in files:
            if file.endswith('.txt'):
                cleaned.append(file)
                #logger.debug("File retained : " + str(file))

            else:
                logger.debug("Incorrect file type removed. File : " + str(file))
            
        return cleaned

"""
Class for writing files to tab-delimited format
"""
class TSVWriter:
    def __init__(self, data, path=PATH):
        #allow for path specification
        self._PATH = path

        self.info("====START OF LOG====") #start of logging session

        for table in data:
            df = data[table]
            logger.debug("Selected data for table : " + str(table))
            
            if not table.endswith('.tsv'):
                table = table + '.tsv'
                logger.debug("Added .tsv to : " + str(table))

            try:
                df.to_csv(table, encoding='utf-8', sep='\t', index=False)
                logger.debug("Data successfully written to : " + str(table))
            except:
                logger.error("Issue writing data for : " + str(table))
                pass

        logger.info("====END OF LOG==== \n") 
        return

"""
Class for loading files from .sql format
"""
class SQLReader:
    def __init__(self, server="localhost", db="*", username="root", psswd="", path=PATH):
        #allow for path specification
        self._PATH = path

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

                self.data[db] = self.read_data()
            except:
                logger.error("Cannot connect to database : " + str(db))

    """
    Gets all specified sql filenames from a directory
    Directory is set by global self._PATH variable
    Returns: files as list of strings
    Requires: N/A
    """
    def get_files(self):
        files = os.listdir(self._PATH)

        cleaned = []

        for file in files:
            if file.endswith('.sql'):
                cleaned.append(file)
                logger.debug("File retained : " + str(file))

            else:
                logger.debug("Incorrect file type removed. File : " + str(file))
            
        return cleaned

    """
    Reads from existing db and adds the contents to data
    Requires: 
    Returns: 
    """
    def read_data(self, databse, filename):
        return

"""
Class for writing files to sql table
Also allows for database export to file
"""
class SQLWriter:
    def __init__(self):
        return
    
    def write(self):
        return
    
def main():
    if len(sys.argv) == 0:
        tsv = TSVReader()
    else:
        tsv = TSVReader(sys.argv[1])

if __name__ == "__main__":
    main()
