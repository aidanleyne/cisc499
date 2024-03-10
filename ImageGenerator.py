import logging
import time
import sys
from threading import Thread
from PIL import Image
from decimal import Decimal, getcontext

###LOGGING SETUP###
logging.basicConfig(filename="ImageGenerator.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.INFO)
logger = logging.getLogger()

###FIXED POINT ARITHMETIC###
getcontext().prec = 13

###DEFAULT PATH###
PATH = "images"

"""
Phase image generator class
Allows for specification of an export folder
"""
class ImageGenerator:
    def __init__(self, path=PATH):
        logging.info("====START LOG====")
        self._PATH=path

    """
    Generates and saves image based on pandas dataframe
    Requires: dataframe - pandas dataframe; filename - string for saving
    Returns: N/A
    If a filename is not provided, the time since epoch is used
    """
    def generate_image(self, dataframe, filename=int(time.time_ns()), saveFile=0):
        #get columns from passed dataframe
        try:
            self.data = dataframe.loc[:,["SENTENCE", "PRESS_TIME", "RELEASE_TIME"]]
        except:
            logger.exception("Could not caputre columns for file : " + str(filename) + " --- skipping...")
            return
        
        #validate file
        try:
            valid = self.validate_file(filename)
        except:
            logger.exception("Could not validate " + str(filename) + " --- skipping...")
            return

        #return and skip for invalid file
        if valid == -1:
            logger.info(str(filename) + " invalid for image generation --- skipping...")
            return
        
        #small array for the indexes used in image generation
        self.indexes = [0, valid]
        logger.debug("indexes for " + filename + " : " + str(self.indexes))

        #create dict to make sure both images are generated
        self.images = {}
       
        #generate the pair of images and save to dict
        try:
            t1 = Thread(self.compute(self.indexes[0], filename, 1))
            t2 = Thread(self.compute(self.indexes[1], filename, 2))

            t1.start()
            t2.start()

            t1.join()
            t2.join()
        except:
            logger.exception("Could not compute image for file : " + str(filename) + " --- skipping...")
            return
        
        #if both images are generated, save them
        if len(self.images) == 2:
            self.save(saveFile)
            
            del self.images
            del self.data
            return

        logger.info("Only one image saved for : " + filename + " --- skipping...")
        return

    """
    Performs necessay computations to color-in image
    Requires: img - 0,1 for first or second image
    Returns: N/A
    """
    def compute(self, start, filename, filenum):
        #create an image
        image = Image.new('L', (600, 481))

        #set start and end indicies
        sidx = start
        eidx = 300 + start

        #make lists based on dataframe and indicies
        press = self.data['PRESS_TIME'][sidx : eidx].tolist()
        release = self.data['RELEASE_TIME'][sidx : eidx].tolist()
        
        #loop through hz range
        for hz in range(20,501):
            period_ms = Decimal(1000) / Decimal(hz)
            
            #loop through data for each pixel
            for x in range(300):
                press_phase = int(press[x]) % period_ms 
                release_phase = int(release[x]) % period_ms
                
                press_pixel = (press_phase * 255) // period_ms
                release_pixel = (release_phase * 255) // period_ms
                    
                image.putpixel((x*2, hz-20), int(press_pixel))
                image.putpixel(((x*2)+1, hz-20), int(release_pixel))

        #save image to dict
            savename = str(self._PATH + '/' + str(filename[:-4]) + '_' + str(filenum) + '.png')
            self.images[savename] = image

        #memory management
        del press
        del release

    """
    Validates that the file can be used for a phase image computation
    Requires: None
    Returns: Index of where data changes or -1 for a file failure
    """
    def validate_file(self, filename):
        rows = len(self.data['SENTENCE'])
        #check that the file has enough rows to start
        if rows < 601:
            logger.debug(filename + " not enough rows : " + str(rows))
            return -1
        
        s = self.data['SENTENCE'][300]
        i = 301

        while i < (rows - 300):
            if self.data['SENTENCE'][i] != s:
                #check if enough rows remaining with 10 buffer rows
                if (rows - i) >= 310:
                    return i+2
                else:
                    logger.debug(filename + " not enough rows remaining after sentence change " + str(rows - i - 300) + "...")
                    return -1
            i += 1
        
        return -1

    """
    Saves the phase image pair and potentially the used data
    Requires: saveFile (num) - if the file-data is to be saved
    Returns: N/A
    """
    def save(self, saveFile):
        for savename, img in self.images.items():
                img.save(savename)
                logger.debug("Image generated for data. Stored under : " + savename)

                if saveFile == 1:
                    data_name = str(savename[:-4] + '.txt')
                    self.save_data(data_name)

    """
    Saves the data used to generate a phase image
    Requires: savename - name the file will be saved under
    Returns: N/A
    """
    def save_data(self, savename):
        #identify start-point in the data based on file being written
        sidx = self.indexes[int(savename[-5:-4]) - 1]
        eidx = 300 + sidx

        #make lists based on dataframe and indicies
        press = self.data['PRESS_TIME'][sidx : eidx].tolist()
        release = self.data['RELEASE_TIME'][sidx : eidx].tolist()

        with open(savename, 'w') as file:
            file.write("TIME_DELTA\n")

            for i in range(299):
                file.write(str(int(release[i] - press[i])) + '\n')
                file.write(str(int(press[i+1] - release[i])) + '\n')
            file.write(str(int(release[299] - press[299])))

        file.close()

        del press
        del release
            
    """
    This function terminates the ImageGenerator object.
    Also closes the logger.
    """
    def close(self):
        logger.info("====END LOG====\n")

def main():
    if len(sys.argv) < 2:
        gen = ImageGenerator()
    else:
        gen = ImageGenerator(sys.argv[1])

    return

if __name__ == "__main__":
    main()