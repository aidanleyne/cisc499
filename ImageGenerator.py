import logging
import time
import sys
from PIL import Image

###LOGGING SETUP###
logging.basicConfig(filename="ImageGenerator.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.DEBUG)
logger = logging.getLogger()

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
        self.data = dataframe.loc[:,["PRESS_TIME", "RELEASE_TIME"]]
        
        #@TODO: what did this line do originally?
        #we should have 600 events that are a combo of a start-end pair
        #confirm this with danel/ethan
        #ed = events[:600]

        #compute the pixels for the image
        self.compute()

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
        #ef = self.data[-600:]
        for hz in range(20,501):
            #for i in range(len(ef)):
            for i in range(600):
                #value = int(ef[i]) % (1000/hz)
                value = (int(self.data['RELEASE_TIME'][i]) - int(self.data['PRESS_TIME'][i])) % (1000/hz)
                self.image.putpixel(i, hz-20, int(value/(1000/hz)*255))


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