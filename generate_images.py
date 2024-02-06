"""
Generates images for all desktop data files in the /data folder.
"""

from ImageGenerator import ImageGenerator
from dataLoader import TSVReader

gen = ImageGenerator('images')
reader = TSVReader('data')

data = reader.data

for df in data:
    gen.generate_image(data[df], df)
