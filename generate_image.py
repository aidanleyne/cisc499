from PIL import Image

keystroke_file = open('data/36_keystrokes.txt', 'r')
events = []

for line in keystroke_file.readlines()[2:]:
    arr = line.split('\t')
    events.append(arr[5])
    events.append(arr[6])
    
ef = events[:600]

image = Image.new('L', (600, 481))

for hz in range(20,501):
    for i in range(len(ef)):
        value = int(ef[i]) % (100/hz)
        image.putpixel((i,hz-20), int(value/(100/hz)*255))

image.save("images/36_keystrokes.jpg")