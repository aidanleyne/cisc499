from dataLoader import TSVReader
import sys
import os

def get_files(self):
    files = os.listdir(self._PATH)

    cleaned = []

    for file in files:
        if file.endswith('.txt'):
            cleaned.append(file)
            #logger.debug("File retained : " + str(file))
        
    return cleaned    

data = {}

for file in get_files():
    data[file] = TSVReader(sys.argv[1], file)

print("completed")




