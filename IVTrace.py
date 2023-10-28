"""
Created on Fri Oct 27 22:04:16 2023

@author: izattdrake
"""

import math
import csv
import numpy as np
import pandas as pd
from globals import *

class IVTrace:

    def __init__(self, file_path, power, pressure, probe, type=AR):
        self.file_path = file_path
        self.power = power
        self.pressure = pressure
        self.probe = probe
        self.type = type
        self.probe_area = 2 * PI * probe.radius * probe.length

        df_iv = pd.read_csv(self.file_path, names=['Current', 'Voltage'])

        self.current = df_iv['Current']
        self.v_bias = df_iv['Voltage']

        current_positive = [abs(i) for i in self.current]
        v_float_pos = current_positive.index(min(current_positive))

        self.v_float = self.v_bias[v_float_pos]
