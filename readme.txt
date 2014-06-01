Chris Stadler
readme.txt

class MyImage has 5 methods:
bin_global: O(n)
    loop over self.data to calculate global mean: O(n)
    calls find_global_threshold: O(n)
    loop over self.data to binarize pixels and append to binData: O(n)
    Create new image from binData: O(n)
bin_local: O(n^2)
    loops over self.data: O(n)
        loops over the neighborhood: O(n) (In the worst case this will be the whole image
    Create a new image from binData: O(n)
find_global_threshold: O(c*(n+n)) = O(n)
    calls calculate_histogram: O(n)
    calls histogram_mean: O(n)
    recurses: O(c)
        We are recursing over a histogram of constant size and so the number of
        recursions does not depend on the size of the image.
calculate_histogram: O(n)
    loops over self.data: O(n)           
show: O(n)
