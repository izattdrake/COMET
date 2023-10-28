"""
Created on Fri Oct 27 23:45:07 2023

@author: izattdrake
"""

from globals import *

class Probe:

    def __init__(self, radius, length):
        self.radius = radius
        self.length = length
        self.area = 2 * PI * self.radius * self.length