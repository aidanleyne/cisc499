from dataLoader import TSVReader
import sys
import os

def get_files():
    files = os.listdir(sys.argv[1])

    cleaned = []

    for file in files:
        if file.endswith('.txt'):
            cleaned.append(file)
            #logger.debug("File retained : " + str(file))
        
    return cleaned    

data = {}

for file in get_files():
    print(file)
    reader = TSVReader()
    data[file] = reader.load(sys.argv[1], file)

print("completed")




