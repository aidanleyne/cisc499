import os
import sys
import logging
import csv
import pandas as pd
import warnings
import mysql.connector as sql

###LOGGING SETUP###
logging.basicConfig(filename="dataLoader.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.DEBUG)
logger = logging.getLogger()

###PATH TO DATA####
PATH = 'data'

###SUPRESS WARNINGS###
warnings.simplefilter(action='ignore', category='FutureWarning')

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
        files = os.listdir(PATH)

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
Class for writing files to .csv format
"""
class CSVWriter:
    def __init__(self, data, path=PATH):
        #allow for path specification
        PATH = path

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
        PATH = path

        self.data = {}

        logger.debug("====START OF LOG====") #start of logging session

        files = self.get_files()
        logger.debug("Begining Import on " + str(len(files)) + " files...")

        for file in files:
            #read file into pandas df and append to dict
            self.data[file] = pd.read_csv(str(PATH + '/' + file), header=0, delimiter='\t')
            logger.debug("Read in file : " + str(file))

        logger.debug("All data in " + str(PATH) + " processed")
        logger.debug("Data-dictionary is of length : " + str(len(self.data)))

        logger.info("====END OF LOG==== \n")
        return

    """
    Gets all specified txt filenames from a directory
    Directory is set by global PATH variable
    Returns: files as list of strings
    Requires: N/A
    """
    def get_files(self):
        files = os.listdir(PATH)

        cleaned = []

        for file in files:
            if file.endswith('.txt'):
                cleaned.append(file)
                logger.debug("File retained : " + str(file))

            else:
                logger.debug("Incorrect file type removed. File : " + str(file))
            
        return cleaned

"""
Class for writing files to tab-delimited format
"""
class TSVWriter:
    def __init__(self, data, path=PATH):
        #allow for path specification
        PATH = path

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
class SQLReader():
    def __init__(self, server="localhost", db="mysql", username="root", psswd=""):
        logger.debug("====START OF LOG====") #start of logging session
        self.data = {}

        try:
            #try to connect to the db
            self.db = sql.connect(user=username, password=psswd, host=server, database=db)
            self.cursor = self.db.cursor()
            logger.info("Connected to database : " + str(db) + " --- on server : " + str(server))
        except:
            logger.exception("Issue connecting to database")
            return

        #get tables in db
        tables = self.get_tables()
        logger.info(str(len(tables)) + " were found in database : " + str(db))

        #append dict using <tablename, dataframe> with returned data
        for (tablename,) in tables:
            self.data[tablename] = self.get_data(tablename)

        logger.debug("All files loaded and appened to dict as <tablename, dataframe>...")
        logger.info("====END OF LOG====\n")
        return
        
    """
    Returns list of tablenames in database
    Requires: None
    Returns: list of tablenames
    """
    def get_tables(self):
        self.cursor.execute("SHOW TABLES;")
        return self.cursor.fetchall()
    
    """
    Returns SQL table as pandas df
    Requires: tablename (str)
    Returns: pandas df
    """
    def get_data(self, tablename):
        return pd.read_sql(str('SELECT * FROM ' + str(tablename)) + ';', con=self.db)
    
    """
    Closes the cursor and connection to the database.
    Requires: None
    Returns: None
    """
    def close(self):
        self.cursor.close()
        logger.info("**** Cursor Closed. *****")
        self.db.close()
        logger.info("**** Connection Closed. ****\n====END OF LOG====\n")
            
"""
Class for writing files to sql table
@TODO. This may require SQLAlchemy implementation.
"""
class SQLWriter:
    def __init__(self, server="localhost", db="mysql", username="root", psswd="", new=False):
        #create new db
        if new:
            try:
                #connect to the server & open cursor
                self.db = sql.connect(user=username, password=psswd, host=server)
                self.cursor = self.db.cursor()
                logger.info("Connected to %s" + str(server))
            except:
                logger.error("Cannot connect to databse : " + str(db))
                return

            try:
                self.cursor.execute('CREATE DATABASE IF NOT EXISTS ' + str(db) + ';')
                self.db.commit()
                logger.info("New database -" + str(db) + "- created succesfully...")
                self.cursor.execute('USE ' + str(db) + ';')
                logger.info("Switched to databse : " + str(db))
            except:
                logger.error("Could not create database : " + str(db))
                return

        #connect to existing db
        else:
            try:
                #connect to SQLServer & open a cursor
                self.db = sql.connect(user=username, password=psswd, host=server, database=db)
                self.cursor = self.db.cursor()
                logger.debug("Connected to databse : " + str(db))
            except:
                logger.error("Cannot connect to database : " + str(db))
                return
            
        return

    """
    Writes passed dataframe to open SQL database
    Requires: df - pandas dataframe, tablename - str for desired name of table, idx - indexing
    Returns: None
    """
    def write(self, df, tablename, idx=False):
        df.to_sql(tablename, if_exitsts='replace', index=idx)
        return
    
    """
    Closes the cursor and connection to the database.
    Requires: None
    Returns: None
    """
    def close(self):
        self.cursor.close()
        logger.info("**** Cursor Closed. *****")
        self.db.close()
        logger.info("**** Connection Closed. ****\n====END OF LOG====\n")

"""
Class for laoding .sql file to sql database
@TODO: does this even need to be implemented? Just do it server-side first
"""
class SQLLoader:
    def __init__(self):
        return

def main():
    if len(sys.argv) == 0:
        tsv = TSVReader()
    else:
        tsv = TSVReader(sys.argv[1])

    return

if __name__ == "__main__":
    main()