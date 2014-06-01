import Image
import sys

# read file name
#file_name = sys.argv[1]
file_name = "lena.png"

# open image
im = Image.open(file_name)
print 'Image read from', file_name, 'with size', im.size

# convert image to grayscale
im = im.convert("L")
im.show()

# get data from image
data = list(im.getdata())

# modify the data (you should remove these lines and use your code)
for i in range(0, 50000):
	data[i] = 0

# create a new image with the new data
im2 = Image.new("L", im.size)
im2.putdata(data)
im2.show()
