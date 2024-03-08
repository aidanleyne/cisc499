"""
Generates images for all desktop data files in the /data folder.
"""
import sys
import multiprocessing
from tqdm import tqdm as tq
from ImageGenerator import ImageGenerator
from DataLoader import TSVReader


def run(item, savefile):
    filename, df = item
    gen.generate_image(df, filename, savefile)

#set number of threads on system
NUM_OF_CORES = 16

#set a default path for the data
INPATH = 'data'

#set a default path for the images
OUTPATH = 'images'

#set a default number of files to count-in
count = -1

if len(sys.argv) > 5:
    INPATH = sys.argv[1]
    OUTPATH = sys.argv[2]
    try:
        count = int(sys.argv[3])
    except:
        print("Not a valid number of files. Will load all possible")

    if sys.argv[4] == 'reverse=True':
        reverse = True
        print('Reding files bottom up...')
    else:
        reverse = False

    if sys.argv[5] == 'save=True':
        savefile=1
    else:
        savefile=0

elif len(sys.argv) > 5:
    INPATH = sys.argv[1]
    OUTPATH = sys.argv[2]
    try:
        count = int(sys.argv[3])
    except:
        print("Not a valid number of files. Will load all possible")

    if sys.argv[4] == 'reverse=True':
        reverse = True
        print('Reding files bottom up...')
    else:
        reverse = False

elif len(sys.argv) > 3:
    INPATH = sys.argv[1]
    OUTPATH = sys.argv[2]
    try:
        count = int(sys.argv[3])
    except:
        print("Not a valid number of files. Will load all possible")

elif len(sys.argv) > 2:
    INPATH = sys.argv[1]
    OUTPATH = sys.argv[2]

else:
    print("Requires at least 2 arguments: INPATH, OUTPATH; Optional arguments: Count")
    exit()

print("*** Loading Files... ***")
if count > 0:
    reader = TSVReader(INPATH, count, reverse)
else:
    reader = TSVReader(INPATH)
    
gen = ImageGenerator(OUTPATH)

print("\n*** Creating Images... ***")
pool = multiprocessing.Pool(processes=NUM_OF_CORES)
pool.map(run, reader.data.items(), savefile) 

gen.close()
