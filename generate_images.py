"""
Generates images for all desktop data files in the /data folder.
"""
import argparse
import multiprocessing
from tqdm import tqdm as tq
from utils.ImageGenerator import ImageGenerator
from utils.DataLoader import TSVReader

#set number of threads on system
NUM_OF_CORES = 16

#start dictionary for everything to be appended
data = {}

#argparse for cli arguments
parser = argparse.ArgumentParser(description='Generates Phase Images')
parser.add_argument("--INPATH", type=str, default='data/Keystrokes/files', 
                    help="Input path")
parser.add_argument("--OUTPATH", type=str, default="images", 
                    help="Output path")
parser.add_argument("--count", type=int, default=0, 
                    help="Number of files to read")
parser.add_argument("--reverse", action="store_true", 
                    help="Read files bottom-up")
parser.add_argument("--saveFile", action="store_true", 
                    help="Save text files along with images")
parser.add_argument("--cSize", type=int, default=25000,
                    help="Specify processing chunk-size")

args = parser.parse_args()

reader = TSVReader(args.INPATH)
gen = ImageGenerator(args.OUTPATH)

def img_gen(item):
    filename, df = item
    gen.generate_image(df, filename, args.saveFile)

def main():
    #create multiprocessing pool
    pool = multiprocessing.Pool(processes=NUM_OF_CORES)
    
    #load in files
    files = reader.get_files()

    #reverse list if specified
    if args.reverse:
        files = files[::-1]

    #limit size of files used
    if args.count > 0:
        files = files[:args.count]

    #calculate chunks required
    chunks = len(files) // args.cSize

    for c in tq(range(chunks+1)):
        print("*** Loading Chunk" + str(c) + " of " + str(chunks) + "... ***")
        data.clear()
        
        #get subset of files to process
        if c == chunks:
            remainder = len(files) % args.cSize
            sub_files = files[:remainder] 
        else:
            sub_files = files[c*args.cSize : (c+1)*args.cSize]

        #read files
        print("*** Loading Files... ***")
        for filename in tq(sub_files):
            fdata = reader.read(filename)
            if not fdata.empty:
                data[filename] = fdata

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