import logging
import time
import sys
from PIL import Image
from decimal import Decimal, getcontext

###LOGGING SETUP###
logging.basicConfig(filename="ImageGenerator.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.DEBUG)
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
        valid = self.validate_file(filename)

        #return and skip for invalid file
        if valid == -1:
            logger.info(str(filename) + " invalid for image generation --- skipping...")
            return
        
        #small array for the indexes used in image generation
        indexes = [0, valid]
        logger.debug("indexes for " + filename + " : " + str(indexes))
       
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
            savename = str(self._PATH + '/' + str(filename[:-4]) + '_' + str(i+1) + '.png')
            self.image.save(savename)
            logger.debug("Image generated for data. Stored under : " + savename)

    """
    Performs necessay computations to color-in image
    Requires: img - 0,1 for first or second image
    Returns: N/A
    """
    def compute(self, start):
        #set start and end indicies
        sidx = 0 + start
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
                    
                self.image.putpixel((x*2, hz-20), int(press_pixel))
                self.image.putpixel(((x*2)+1, hz-20), int(release_pixel))

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
        if rows < 601:
            logger.debug(filename + " not enough rows : " + str(rows))
            return -1
        
        s = self.data['SENTENCE'][300]
        i = 301

        while i < (rows - 300):
            if self.data['SENTENCE'][i] != s:
                if (rows - i) >= 300:
                    return i+2
                else:
                    logger.debug(filename + " not enough rows remaining after sentence change " + str(rows - i - 300) + "...")
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