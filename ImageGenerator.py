import logging
import time
import sys
from PIL import Image

###LOGGING SETUP###
logging.basicConfig(filename="dataLoader.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.DEBUG)
logger = logging.getLogger()

#default path
PATH = "images"

"""
Phase image generator class
Allows for specification of an export folder
"""
class ImageGenerator:
    def __init__(self, path=PATH):
        logging.info("====START LOG====\n")
        PATH=path

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

        #save image to destination
        savename = str(PATH + '/' + str(filename) + '.jpg')
        self.image.save(savename)
        logger.debug("Image generated for data. Stored under : ", savename)

    """
    Performs necessay computations to color-in image
    Requires: N/A
    Returns: N/A
    """
    def compute(self):
        for hz in range(20,501):
            for i in range(len(ef)):
                value = int(ef[i]) % (100/hz)
                self.image.putpixel((i,hz-20), int(value/(100/hz)*255))
   
#@TODO: what did this line do originally?
#ef = events[:600]

def main():
    if len(sys.argv) == 0:
        gen = ImageGenerator()
    else:
        gen = ImageGenerator(sys.argv[1])

    return

if __name__ == "__main__":
    main()