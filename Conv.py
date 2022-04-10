# Convert the Geodetic coordinates to Cartesian coordinates 

import numpy
from tkinter import filedialog
from tkinter import *
from tkinter import filedialog

class Conv:
    def __init__(self, latitude=0, longitude=0):
        self.latitude = latitude
        self.longitude = longitude
		
    def converter(self):
        r = 6371008800  # earth radius in millimeters
        east = r * (numpy.sin(numpy.radians(self.latitude))) * (numpy.cos(numpy.radians(self.longitude)))
        north = r * (numpy.cos(numpy.radians(self.latitude)))
        return (east, north)