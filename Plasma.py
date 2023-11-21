"""
Created on Mon Nov 20 22:14:00 2023

@author: izattdrake
"""

from globals import *
from utilities import *
import csv
import numpy as np

class Plasma:
    def __init__(self, file_path, power, pressure, freq):
        self.file_path = file_path
        self.power = power
        self.pressure = pressure
        self.freq = freq

        self.i = []
        self.v_bias = []

        with open(self.file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.i.append(float(row[0]))
                self.v_bias.append(float(row[1]))

        v_float_pos = get_min_pos(self.i)
        self.v_float = self.v_bias[v_float_pos]

        slope, intercept = np.polyfit(self.v_bias[0:v_float_pos], self.i[0:v_float_pos])
        self.i_ion = slope * self.v_float + intercept
        self.ie = self.i - self.i_ion
        
        low_pos = get_nearest_pos()
