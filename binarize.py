"""
Chris Stadler
binarize.py

for Python 2.7
"""

try:
    import Image
except ImportError:
    print "requires Python Image Library"
    exit(1)
#import sys

class MyImage:
    def __init__(self, filename):
        self.rawImage = Image.open(filename)
        self.grayscale = self.rawImage.convert("L")
        self.data = list(self.grayscale.getdata())
        self.width, self.height = self.rawImage.size

    def bin_global(self, e, out_file):
        binData = []
        # Guess T by calculating global mean
        globalSum = 0
        for p in self.data:
            globalSum += p
        guessT = globalSum/len(self.data)
        T = self.find_global_threshold(guessT, e)
        for p in self.data:
            # Binarize the pixel
            if p >= T:
                newp = 255
            else:
                newp = 0
            # Add the binarized pixel to the binarized data
            binData.append(newp)
        binIm = Image.new("L", (self.width, self.height))
        binIm.putdata(binData)
        #binIm.show()
        binIm.save(out_file)
    
    def find_global_threshold(self, T, e):
        histogram = self.calculate_histogram()
        # Find the means on either side of T
        meanLeft = histogram_mean(histogram, 0, T)
        meanRight = histogram_mean(histogram, T, 255)
        newT = (meanLeft + meanRight)/2
        if abs(T - newT) < e:
            return newT
        else:
            return self.find_global_threshold(newT, e)     
    
    def calculate_histogram(self):
        histogram = [0]*256 # Initialize histogram array
        for pixel in self.data:
            histogram[pixel] += 1 # Increase the frequency for that intensity by 1
        return histogram

    def bin_local(self, ngbr, out_file):
        binData = [] # Initialize a new data array
        # Keep track of the row and column indices
        row = 0
        col = 0
        for p in self.data: # Find the local threshold
            locSize = 0 # number of pixels in neighborhood
            locSum = 0 # Sum of neighborhood
            # Sum every pixel in the neighborhood
            for locRow in range(row-ngbr, row+ngbr+1):
                for locCol in range(col-ngbr, col+ngbr+1):
                    if 0 <= locRow < self.height and 0 <= locCol < self.width:
                        intensity = self.data[locRow*self.width + locCol]
                        locSum += intensity
                        locSize += 1

            # Threshold = mean of neighborhood
            T = locSum/locSize
            
            # Binarize the pixel
            if p >= T:
                newp = 255
            else:
                newp = 0

            # Add the binarized pixel to the binarized data
            binData.append(newp)
            # Update row and col
            if col == self.width-1:
                row += 1
                col = 0
            else:
                col += 1
                
        # Create new image with binarized data
        binIm = Image.new("L", (self.width, self.height))
        binIm.putdata(binData)
        #binIm.show()
        binIm.save(out_file)
        
    def show(self):
        self.rawImage.show()   

# Calculates the mean intensity between left and right (inclusive) of a histogram
def histogram_mean(histogram, left, right):
    i = left
    histsum = 0
    n = 0
    while i <= right:
        freq = histogram[i]
        histsum += freq*i
        n += freq
        i += 1
    return histsum/n


# Command line interface
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Binarize an image")
    parser.add_argument('input', help='filename of image to binarize')
    parser.add_argument('--bin_local', '-l', help='output filename for local binarization')
    parser.add_argument('--bin_global', '-g', help='output filename for global binarization')
    args = parser.parse_args()
    if args.input and (args.bin_local or args.bin_global):
        im = MyImage(args.input)
        if args.bin_local:
            im.bin_local(2, args.bin_local)
        if args.bin_global:
            im.bin_global(1, args.bin_global)
    else:
        print "usage: <input file name> <'-l' for local binarization AND/OR '-g' for global> <output file name>"
        exit(1)
"""

#Testing
lena = MyImage("lena.png")
#lena.show()
#lena.bin_local(1)
#lena.bin_global(1)
#im.bin_global(1)
#im.bin_local(2)
lena.bin_better(2)
"""

        
