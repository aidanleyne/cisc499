"""
Generates images for all desktop data files in the /data folder.
"""
import sys
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

reader = TSVReader(INPATH)
gen = ImageGenerator(OUTPATH)

data = reader.data

for df in data:
    gen.generate_image(data[df], df)

gen.close()
