from glob import glob
from tqdm import tqdm
import numpy as np
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
    print(idxs)

    rank = 1
    for match in idxs:
        if db.db[match].profile.id == name:
            if rank == 1:
                ranks[1]+=1
                ranks[10]+=1
                ranks[100]+=1
            elif rank > 1 and rank < 11:
                ranks[10]+=1
                ranks[100]+=1
            else:
                ranks[100]+=1
            continue
        else:
            rank+=1

def main():
    #create multiprocessing pool
    pool = multiprocessing.Pool(processes=NUM_OF_THREADS)

    #get all the filenames
    img1 = glob(PATH + '/*_1.png')[:100]
    img2 = glob(PATH + '/*_2.png')[:100]
    txt1 = glob(PATH + '/*_1.txt')[:100]
    txt2 = glob(PATH + '/*_2.txt')[:100]

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
