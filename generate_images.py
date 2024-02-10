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

if len(sys.argv) > 1:
    INPATH = sys.argv[1]

elif len(sys.argv) > 2:
    INPATH = sys.argv[1]
    OUTPATH = sys.argv[2]

print("*** Loading Files... ***")
reader = TSVReader(INPATH)
gen = ImageGenerator(OUTPATH)

print("*** Loading Files... ***")
for filename, df in tq(reader.data.items()):
    gen.generate_image(filename, df)

gen.close()
