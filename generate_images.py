"""
Generates images for all desktop data files in the /data folder.
"""
import sys
import multiprocessing
from tqdm import tqdm as tq
from ImageGenerator import ImageGenerator
from DataLoader import TSVReader

#set number of threads on system
NUM_OF_CORES = 16

#set a default path for the data
INPATH = 'data'

#set a default path for the images
OUTPATH = 'images'

#start dictionary for everything to be appended
data = {}

"""if len(sys.argv) > 5:
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
    exit()"""

reader = TSVReader('data/Keystrokes')
gen = ImageGenerator(OUTPATH)

def file_read(filename):
    data[filename] = reader.read(filename)

def img_gen(item):
    filename, df = item
    gen.generate_image(df, filename, 1)

def main():
    #create multiprocessing pool
    pool = multiprocessing.Pool(processes=NUM_OF_CORES)
    
    #load in files
    print("*** Loading Files... ***")
    files = reader.get_files()[:10000]
    with tq(total=len(files)) as pbar:
        #for _ in pool.imap_unordered(file_read, files):
            #pbar.update(1)
        for file in files:
            file_read(file)
            pbar.update(1)

    print(len(data))

    #make the phase images
    print("\n*** Creating Images... ***")
    with tq(total=len(data)) as pbar:
        for _ in pool.imap_unordered(img_gen, data.items()):
            pbar.update(1)

    pool.close()
    pool.join()
    
    gen.close()
    reader.close()

if __name__ == '__main__':
    main()