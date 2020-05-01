from PIL import Image

im = Image.open('testimg.jpg')
im1 = im.resize((100, 100))
im1.save('small.jpg')

