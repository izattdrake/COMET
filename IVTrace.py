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
        v_float_pos = self.get_min_pos(self.i)
        self.v_float = self.v_bias[v_float_pos]

        #ion current assumed negative at the moment
        self.i_ion = self.get_i_ion(self.i, self.v_bias, self.v_float, v_float_pos)
        #i_e = i_probe - i_ion
        self.ie = self.i - self.i_ion
        self.temp_e = self.get_temp_e(self.ie, self.v_bias, v_float_pos)
        self.plasma_density = self.get_plasma_density(self.i_ion, self.probe, self.temp_e, self.type)

        """
        poly = self.smooth_poly(self.v_bias, self.i, 10)
        di_edv_bias = self.d1_poly(poly, self.v_bias)
        v_plasma_pos = np.where(di_edv_bias == di_edv_bias.max())[0][0]
        v_plasma = v_bias_e[v_plasma_pos]
        """
        """
        plt.plot(self.v_bias, self.i, 'o--')
        plt.title('IV Trace')
        plt.grid()
        plt.show()
        """
    
    def get_temp_e(self, ie, v_bias, v_float_pos):
        # TODO: FIND ZERO CROSSING NOT NECESSARILY V_FLOAT SINCE IF CLOSEST TO ZERO IS NEGATIVE LN WILL THROW NULL VAL
        ln_ie = np.log(ie)

        # TODO: THINK ABOUT BOUNDS FOR LINEAR FIT TO LN(IE)
        low = 5
        high = 10

        slope , intercept = np.polyfit(v_bias[v_float_pos+low:v_float_pos+high], ln_ie[v_float_pos+low:v_float_pos+high], 1)
        temp_e = 1/slope
        return temp_e
        
        """
        plt.plot(v_bias[v_float_pos+low:v_float_pos+high], ln_ie[v_float_pos+low:v_float_pos+high])
        plt.title(f'ln(Electron Current) {self.power}W {self.pressure}mTorr')
        plt.grid()
        plt.show()
        """

    def get_plasma_density(self, i_ion, probe, temp_e, type):
        if type == AR:
            v_bohm = math.sqrt(temp_e / (MASS_AR_AMU * MASS_P_EV))
        if type == N:
            v_bohm = math.sqrt(temp_e / (MASS_N_AMU * MASS_P_EV))

        plasma_density = i_ion/(0.61 * probe.area * v_bohm)
        print(f'Plasma Density: {plasma_density}')

    def get_i_ion(self, i, v_bias, v_float, v_float_pos):
        slope, intercept = np.polyfit(v_bias[0:v_float_pos], i[0:v_float_pos], 1)
        i_ion = slope * v_float + intercept
        return i_ion

    def smooth_poly(self, x_vals, y_vals, degree):
        poly_coeff = np.polyfit(x_vals, y_vals, degree)
        poly = np.poly1d(poly_coeff)
        return poly 
    
    def d1_poly(self, poly, x_vals):
        poly_d_1 = poly.deriv(1)
        y_vals = poly_d_1(x_vals)
        return y_vals
    
    def get_min_pos(self, y_vals):
        y_vals_positive = np.array([abs(y_val) for y_val in y_vals])
        min_pos = np.where(y_vals_positive == y_vals_positive.min())[0][0]
        return min_pos
            
    def get_v_float(self, v_bias, v_float_pos):
        v_float = v_bias[v_float_pos]
        return v_float
    