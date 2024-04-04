from glob import glob
from tqdm import tqdm
import numpy as np
import os
import multiprocessing
from utils.database import Database
from utils.User import Profile
from models import taunet, fpnet

#define path used for evalutation folder
PATH = 'eval/evaluationImages'

#set number of threads available
NUM_OF_THREADS = 12

#initialize utilities
db = Database(256)

#define ranks
ranks = {1 : 0, 10 : 0, 100 : 0}

def process_firsts(item):
    img, txt = item

    #get the id for the file
    name = img[img.find('\\') + 1 : img.find('_')]
    
    # make 256 array
    fp = fpnet.generate(img).tolist()
    tn = taunet.generate(txt).tolist()
    arr = np.array(fp + tn)
    arr = (arr/np.linalg.norm(arr)).tolist()

    #create profile for the id
    pf = Profile(name)

    #add to the databse
    db.insert(arr, profile=pf)

def process_seconds(item):
    img, txt = item
    
    # make 256 array
    fp = fpnet.generate(img).tolist()
    tn = taunet.generate(txt).tolist()
    arr = np.array(fp + tn)
    arr = (arr/np.linalg.norm(arr)).tolist()

    #get name to id the vector
    name = img[img.find('\\') + 1 : img.find('_')]

    #find the indexes of the 
    idxs = db.find(arr, 100)[0]

    rank = 1
    for match in idxs:
        if db.db[match].profile.id == name:
            if rank == 1:
                ranks[1]+=1
                ranks[10]+=1
                ranks[100]+=1
                break
            elif rank > 1 and rank < 11:
                ranks[10]+=1
                ranks[100]+=1
                break
            else:
                ranks[100]+=1
                break
        else:
            rank+=1

def main():
    #create multiprocessing pool
    pool = multiprocessing.Pool(processes=NUM_OF_THREADS)

    # Step 1: Get all the .png or .txt files to extract unique numbers
    all_png_files = glob(os.path.join(PATH, '*_1.png'))  # Or use '*_2.png' if you prefer

    # Step 2: Extract unique numbers from these files
    unique_numbers = sorted(set([os.path.basename(file).split('_')[0] for file in all_png_files]))

    # Step 3: Limit to the first 100 unique numbers
    unique_numbers = unique_numbers[:100]

    # Step 4: Find corresponding files for each unique number
    img1, img2, txt1, txt2 = [], [], [], []
    for number in unique_numbers:
        img1.append(glob(os.path.join(PATH, f'{number}_keystrokes_1.png'))[0])
        img2.append(glob(os.path.join(PATH, f'{number}_keystrokes_2.png'))[0])
        txt1.append(glob(os.path.join(PATH, f'{number}_keystrokes_1.txt'))[0])
        txt2.append(glob(os.path.join(PATH, f'{number}_keystrokes_2.txt'))[0])

    print(img1)
    print(img2)

    #create dicts with images as keys and texts as pairs
    dict1 = dict(zip(img1, txt1))
    dict2 = dict(zip(img2, txt2))

    
    # one image at a time
    for item in tqdm(dict1.items()):
        process_firsts(item)

    for item in tqdm(dict2.items()):
        process_seconds(item)
    

    """
    # pooled processing
    with tqdm(total=len(dict1)) as pbar:
        for _ in pool.imap_unordered(process_firsts, dict1.items()):
            pbar.update(1)

    with tqdm(total=len(dict1)) as pbar:
        for _ in pool.imap_unordered(process_seconds, dict2.items()):
            pbar.update(1)
    
    pool.close()
    pool.join()
    """

    for rank in ranks:
        print("rank :", rank, ":", ranks[rank], "---", ranks[rank]/len(img1)) 

if __name__ == "__main__":
    main()
