"""
Created on Fri Oct 27 22:04:16 2023

@author: izattdrake
"""

import math
import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from globals import *

# Plasma potential at maximum of first derivative of I_e V trace
class IVTrace:

    def __init__(self, file_path, power, pressure, probe, type=AR):
        self.file_path = file_path
        self.power = power
        self.pressure = pressure
        self.probe = probe
        self.type = type

        df_iv = pd.read_csv(self.file_path, names=['Current', 'Voltage'])

        self.i = df_iv['Current']
        self.v_bias = df_iv['Voltage']

        plt.plot(self.v_bias, self.i, 'o--')
        plt.title('IV Trace')
        plt.grid()
        plt.show()

        i_positive = np.array([abs(i) for i in self.i])
        v_float_pos = np.where(i_positive == i_positive.min())[0][0]
        self.v_float = self.v_bias[v_float_pos]

        i_e = self.i[v_float_pos:]
        v_bias_e = self.v_bias[v_float_pos:]
        poly = self.smooth_poly(v_bias_e, i_e, 5)
        di_edv_bias = self.d1_poly(poly, v_bias_e)
        print(di_edv_bias)
        v_plasma_pos = np.where(di_edv_bias == di_edv_bias.max())[0][0]
        print(v_plasma_pos)
        v_plasma = v_bias_e[v_plasma_pos]

    def smooth_poly(self, x, y, degree):
        poly_coeff = np.polyfit(x, y, degree)
        poly = np.poly1d(poly_coeff)
        return poly
    
    def d1_poly(self, poly, x_vals):
        poly_d_1 = poly.deriv(1)
        y_vals = poly_d_1(x_vals)
        return y_vals
