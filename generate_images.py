"""
Generates images for all desktop data files in the /data folder.
"""
import sys
import multiprocessing
from tqdm import tqdm as tq
from ImageGenerator import ImageGenerator
from DataLoader import TSVReader


def img_gen(item):
    filename, df = item
    gen.generate_image(df, filename, 1)

def file_read(filename):
    data[filename] = reader.read(filename)

#set number of threads on system
NUM_OF_CORES = 16

#set a default path for the data
INPATH = 'data'

#set a default path for the images
OUTPATH = 'images'

#set a default number of files to count-in
count = -1

#start dictionary for everything to be appended
data = {}

#create multiprocessing pool
pool = multiprocessing.Pool(processes=NUM_OF_CORES)


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

elif len(sys.argv) > 4:
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

reader = TSVReader(INPATH, count, reverse)
gen = ImageGenerator(OUTPATH)

#get files in directory
files = reader.get_files()

print("*** Loading Files... ***")
for _ in tq(pool.imap_unordered(file_read, files), total=len(len(files))):
    pass

print("\n*** Creating Images... ***")
for _ in tq(pool.imap_unordered(img_gen, data.items()), total=len(reader.data.items())):
    pass

gen.close()
reader.close()