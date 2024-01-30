import os
import csv
import pandas as pd

PATH = 'data'

def get_files():
    files = os.listdir(PATH)

    for file in files:
        if '.csv' not in file:
            files.remove(file)

    return files

def get_headers(filename):
    with open(str(PATH + '/' + filename), newline='\n') as file:
        reader = csv.reader(file, delimiter=',')
        headers = []
        for row in reader:
            headers.append(row[0])
        
    headers.pop(0)
    print(headers)

    return headers

def get_data(filename, headers):
    return pd.read_csv(str(PATH + '/' + filename), names=headers, encoding='latin1', quotechar='"')

def main():
    files = get_files()

    for i in range(0, len(files), 2):
        print(files[i])
        get_data(files[i], get_headers(files[i+1]))

if __name__ == "__main__":
    main()