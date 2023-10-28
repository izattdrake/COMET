"""
Created on Fri Oct 27 22:04:16 2023

@author: izattdrake
"""

import math
from globals import *

class IVTrace:

    def __init__(self, file_path, power, pressure, radius, length, type = AR):
        self.file_path = file_path
        self.power = power
        self.pressure = pressure
        self.radius = radius
        self.length = length
        self.type = type

        self.probe_area = 2 * PI * radius * length