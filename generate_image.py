from PIL import Image

keystroke_file = open("36_keystrokes.txt", 'r')
events = []

for line in keystroke_file.readlines()[2:]:
    arr = line.split('\t')
    events.append(arr[5])
    events.append(arr[6])
    
ef = events[0:600]

image = Image.new('L', (600, 481))

for hz in range(20,501):
    for i in range(len(ef)):
        value = int(ef[i])%(1000/hz)
        image.putpixel((i,hz-20), int((value/(1000/hz))*255))

image.save("pi.png")