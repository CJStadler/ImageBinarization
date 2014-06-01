"""
Chris Stadler
myimage.py
"""

import Image
# import sys

class MyImage:
    def __init__(self, filename):
        self.rawImage = Image.open(filename)
        self.grayscale = self.rawImage.convert("L")
        self.data = list(self.grayscale.getdata())
        self.width, self.height = self.rawImage.size

    def bin_global(self, e):
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
        binIm.show()
    
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

    def bin_local(self, ngbr):
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
##        binIm = Image.new("L", (self.width, self.height))
##        binIm.putdata(binData)
##        binIm.show()
        return binData
        #binIm.save("bin_local.png")
        
    def show(self):
        self.rawImage.show()

    def bin_better(self, ngbr):
        binData = self.bin_local(ngbr)
        left = min(self.data)
        right = max(self.data)
        globalT = self.find_global_threshold(125, 1)
        histogram = self.calculate_histogram()
        newLeft = histogram_mean(histogram, left, globalT) + left
        newRight = histogram_mean(histogram, globalT, right) + globalT
        
        for i in range(len(binData)):
            if self.data[i] > newRight:
                binData[i] = 255
            elif self.data[i] < newLeft:
                binData[i] = 0

        binIm = Image.new("L", (self.width, self.height))
        binIm.putdata(binData)
        binIm.show()
        

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

#Testing
lena = MyImage("lena.png")
#im = MyImage("C:\Users\Chris Stadler\Pictures\Art\Irises.jpg")
#lena.show()
#lena.bin_local(1)
#lena.bin_global(1)
#im.bin_global(1)
#im.bin_local(2)
lena.bin_better(2)


        
