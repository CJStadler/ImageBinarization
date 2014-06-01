ImageBinarization
=================
Chris Stadler

Script for local and global image binarization

Written for cs106 at Haverford College with Marco Alvarez.


Local binarization has a fixed neighborhood radius, currently set to 2.

binarize.py Command line interface:

	positional arguments:
		input          		filename of image to binarize

	optional arguments:
		-h, --help
		-l, --bin_local		filename for local binarization
		-g, --bin_global	filename for global binarization


	example usage:
		binarize.py lena.png -l lena_local.png -g lena_global.png