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
        #create blank image
        self.image = Image.new('L', (600, 481))

        #get columns from passed dataframe
        try:
            self.data = dataframe.loc[:,["PRESS_TIME", "RELEASE_TIME"]]
        except:
            logger.exception("Could not caputre columns for file : " + str(filename) + " --- skipping...")
            return

        #compute the pixels for the image
        try:
            self.compute()
        except:
            logger.exception("Could not compute image for file : " + str(filename) + " --- skipping...")
            return

        #save image to destination
        savename = str(self._PATH + '/' + str(filename) + '.png')
        self.image.save(savename)
        logger.debug("Image generated for data. Stored under : " + savename)

    """
    Performs necessay computations to color-in image
    Requires: N/A
    Returns: N/A
    """
    def compute(self):
        press = self.data['PRESS_TIME'][-300:].tolist()
        release = self.data['RELEASE_TIME'][-300:].tolist()
        #loop through hz range
        for hz in range(20,501):
            #loop through last 300 entries
            for i in range(600):
                if i/2 % 2 == 0:
                    period_ms = Decimal(1000) / Decimal(hz)
                    phase_ms = int(press[int(i/2)]) % period_ms
                    pixel_value = (phase_ms * 255) // period_ms
                else:
                    #get value and graph release time
                    period_ms = Decimal(1000) / Decimal(hz)
                    phase_ms = int(release[int(i/2)]) % period_ms
                    pixel_value = (phase_ms * 255) // period_ms
                    
                self.image.putpixel((i, hz-20), pixel_value)

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