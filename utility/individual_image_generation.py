from PIL import Image

def generate_images(data, image_ID):
    image = Image.new('L', (600, 481))
    for hz in range(20,501):
        for i in range(len(data)):
            value = int(data[i])%(1000/hz)
            image.putpixel((i,hz-20), int((value/(1000/hz))*255))

    image.save(image_ID)