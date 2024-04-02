from glob import glob
from lookup.database import Database
from lookup.Profile import Profile
from models import taunet, fpnet

#define path used for evalutation folder
PATH = 'eval/evaluationImages'

#initialize utilities
db = Database(256)
#reader = TSVReader('evaluationImages')

# for each -1 image - generate and load into the db
# for each -2 image - see if the rank-1,10,50,100 is there
# calculate statistics based on if it worked or not

def main():
    #get all the filenames
    img1 = glob(PATH + '/*_1.png')
    img2 = glob(PATH + '/*_2.png')
    txt1 = glob(PATH + '/*_1.txt')
    txt2 = glob(PATH + '/*_2.txt')

    #define ranks
    ranks = {1 : 0, 10 : 0, 100 : 0}

    for img, txt in zip(img1, txt1):
        #get the id for the file
        name = img[img.find('\\') + 1 : img.find('_')]
        
        # make 256 array
        arr = fpnet.generate(img).extend(taunet.generate(txt))

        #create profile for the id
        pf = Profile(name)

        #add to the databse
        db.insert(arr, profile=pf)

    for img, txt in zip(img2, txt2):
        #make the array
        arr = fpnet.generate(img).extend(taunet.generate(txt))

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
                elif rank > 1 and rank < 11:
                    ranks[10]+=1
                    ranks[100]+=1
                else:
                    ranks[100]+=1
                continue
            else:
                rank+=1

    print(ranks)   

if __name__ == "__main__":
    main()
