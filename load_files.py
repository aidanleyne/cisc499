import os
import logging
import csv
import pandas as pd

###LOGGING SETUP###
logging.basicConfig(filename="dataLoad.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.DEBUG)
logger = logging.getLogger()

###PATH TO DATA####
PATH = 'data'

"""
Gets all specified csv filenames from a directory
Directory is set by global PATH variable
Returns: files as list of strings
Requires: N/A
"""
def get_files():
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
def get_headers(filename):
    with open(str(PATH + '/' + filename), newline='\n') as file:
        reader = csv.reader(file, delimiter=',')
        headers = []
        for row in reader:
            headers.append(row[0])
        
    headers.pop(0)

    return headers

"""
Converts csv to pandas df with appropriate headers
Returns: Pandas Dataframe of csv file
Requires: filename - csv file, headers - string list of column headers
"""
def get_data(filename, headers):
    return pd.read_csv(str(PATH + '/' + filename), names=headers, encoding='latin1', quotechar='"')

def main():
    logger.info(" ====START OF LOG====") #start of logging session

    #get files from the data directory
    files = get_files()
    logger.debug("FILENAMES :" +  str(files))

    #initialize new dictionary to store data based on name-df pair
    data = {}

    #loop through files
    for i in range(0, len(files), 2):
        #get headers for given file
        headers = get_headers(files[i+1])
        logger.debug("FOR : %s, HEADERS : %s", files[i], str(headers))

        #get data for given file
        file_data = get_data(files[i], headers)
        logger.debug

        #append to data dictionary
        data[files[i]] = file_data
        logger.debug("%s ==> DATA PROSESSED AND ADDED", files[i])

    logger.info("====END OF LOG==== \n")

if __name__ == "__main__":
    main()