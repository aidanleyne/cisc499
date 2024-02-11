"""
Generates images for all desktop data files in the /data folder.
"""
import sys
from tqdm import tqdm as tq
from ImageGenerator import ImageGenerator
from dataLoader import TSVReader

#set a default path for the data
INPATH = 'data'

#set a default path for the images
OUTPATH = 'images'

#set a default number of files to count-in
count = -1

if len(sys.argv) > 2:
    INPATH = sys.argv[1]
    OUTPATH = sys.argv[2]

if len(sys.argv) > 3:
    INPATH = sys.argv[1]
    OUTPATH = sys.argv[2]
    try:
        count = int(sys.argv[3])
    except:
        print("Not a valid number of files. Will load all possible")

else:
    print("Requires at least 2 arguments: INPATH, OUTPATH; Optional arguments: Count")

print("*** Loading Files... ***")
if count > 0:
    reader = TSVReader(INPATH, count)
else:
    reader = TSVReader(INPATH)
    
gen = ImageGenerator(OUTPATH)

print("*** Loading Files... ***")
for filename, df in tq(reader.data.items()):
    gen.generate_image(df, filename)

gen.close()
