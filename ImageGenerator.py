import logging
import time
import sys
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
    def generate_image(self, dataframe, filename=int(time.time_ns())):
        #get columns from passed dataframe
        try:
            self.data = dataframe.loc[:,["SENTENCE", "PRESS_TIME", "RELEASE_TIME"]]
        except:
            logger.exception("Could not caputre columns for file : " + str(filename) + " --- skipping...")
            return
        
        #validate file
        valid = self.validate_file()

        #return and skip for invalid file
        if valid == -1:
            logger.info(str(filename) + " invalid for image generation --- skipping...")
            return
        
        #small array for the indexes used in image generation
        indexes = [0, valid]
       
        for i in range(2):
            #create blank image
            self.image = Image.new('L', (600, 481))

            #compute the pixels for the image
            try:
                self.compute(indexes[i])
            except:
                logger.exception("Could not compute image for file : " + str(filename) + " --- skipping...")
                return

            #save image to destination
            savename = str(self._PATH + '/' + str(filename[:-4]) + '_' + str(i) + '.png')
            self.image.save(savename)
            logger.debug("Image generated for data. Stored under : " + savename)
            return

    """
    Performs necessay computations to color-in image
    Requires: img - 0,1 for first or second image
    Returns: N/A
    """
    def compute(self, start):
        sidx, eidx = 0 + start, 300 + start
        press = self.data['PRESS_TIME'][sidx : eidx].tolist()
        release = self.data['RELEASE_TIME'][sidx : eidx].tolist()
        #loop through hz range
        for hz in range(20,501):
            #loop through last 300 entries
            for i in range(300):
                period_ms = Decimal(1000) / Decimal(hz)
                press_value = (int(press[int(i)]) % period_ms * 255) // period_ms
                release_value = (int(release[int(i/2)]) % period_ms * 255) // period_ms
                    
                self.image.putpixel((i, hz-20), press_value)
                self.image.putpixel((i+1, hz-20), release_value)

                #memory management
                del press
                del release

    """
    Validates that the file can be used for a phase image computation
    Requires: None
    Returns: Index of where data changes or -1 for a file failure
    """
    def validate_file(self):
        rows = len(self.data['SENTENCE'])
        if rows < 700:
            return -1
        
        s = self.data['SENTENCE'][300]
        i = 301

        while i < rows:
            if self.data['SENTENCE'][i] != s:
                if (rows - i) >= 300:
                    return i
                else:
                    return -1
            i += 1
        return -1

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