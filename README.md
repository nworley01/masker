# Masker

Masker is an application to help make mask annotations for image segmentation tasks using Python and Kivy

## To use:
1. Clone this repo
1. Place images you want to annotate into images/to_anotate directory
1. Open a terminal (or command line, anaconda prompt, etc) and navigate to the base masker directory
1. run $ python masker.py


## Commands:
Annotate the image by left clicking points around the object in the image you wish to annotate.
Currently this application only supports annotation of a single class. Once you have finished
outlining the object of interest, press M to close the shape, convert to a mask, and save to png.

* N - Navigate to the next image using
* B - Backspace (remove last point)
* C - Close shape
* M - Make mask (closes shape, black white, and saves)
* H - Help (toggles displaying this window)
