"""
Created on Fri Oct 27 22:04:16 2023

@author: izattdrake
"""

import math
import csv
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from globals import *

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

        #ion current < 0 
        self.i_ion = self.get_i_ion(self.i, self.v_bias, self.v_float, v_float_pos)
        self.ie = self.i - self.i_ion
        self.temp_e = self.get_temp_e(self.ie, self.v_bias, v_float_pos)
        self.vel_bohm = self.get_vel_bohm(self.temp_e)
        self.plasma_density = self.get_plasma_density(self.i_ion, self.probe, self.temp_e, self.type)
        self.v_plasma = self.get_v_plasma(self.v_float, self.temp_e)

        self.write_plasma()
    
    def plot(self, x_vals, y_vals, title, show=True):
        plt.plot(x_vals, y_vals, 'o--')
        plt.title(title)
        plt.grid()
        
        if show:
            plt.show()

    def write_plasma(self):
        lines = [
            f'Plasma Type: {self.type}',
            f'Probe Length: {self.probe.length} m',
            f'Probe Radius: {self.probe.radius} m',
            f'Pressure: {self.pressure }mTorr',
            f'Power: {self.power} W',
            f'Floating Potential: {self.v_float} V',
            f'Ion Current: {-self.i_ion} A',
            f'Electron Temperature: {self.temp_e} eV',
            f'Bohm Velocity: {self.vel_bohm} m/s',
            f'Plasma Density: {"{:e}".format(self.plasma_density)} m^-3',
            f'Plasma Potential: {self.v_plasma} V'
        ]

        label = f'{self.pressure}mTorr_{self.power}W'
        path_output_IVTrace = f'output/IVTrace/{label}'
        os.makedirs(path_output_IVTrace, exist_ok=True)
        path_txt = f'{path_output_IVTrace}/{label}.txt'
        path = os.path.join(os.path.dirname(__file__), path_txt)

        with open(path, 'w') as file:
            file.write('\n'.join(lines))

        self.plot(self.v_bias, self.i, f'IV Trace {label}', show=False)
        plt.savefig(f'{path_output_IVTrace}/IVTrace_{label}.png')
        plt.clf()

        self.plot(self.v_bias, np.log(self.ie), f'ln(Electron Current) vs Bias Voltage {label}', show=False)
        plt.savefig(f'{path_output_IVTrace}/ln(ie)_{label}.png')
        plt.clf()

    def get_i_ion(self, i, v_bias, v_float, v_float_pos):
        slope, intercept = np.polyfit(v_bias[0:v_float_pos], i[0:v_float_pos], 1)
        i_ion = slope * v_float + intercept
        return i_ion
            
    def get_v_float(self, v_bias, v_float_pos):
        v_float = v_bias[v_float_pos]
        return v_float
    
    def get_temp_e(self, ie, v_bias, v_float_pos):
        # TODO: FIND ZERO CROSSING NOT NECESSARILY V_FLOAT SINCE IF CLOSEST TO ZERO IS NEGATIVE LN WILL THROW NULL VAL
        ln_ie = np.log(ie)

        low_pos = self.get_nearest_pos(v_bias, 15)
        high_pos = self.get_nearest_pos(v_bias, 20)
        slope, intercept = np.polyfit(v_bias[low_pos:high_pos], ln_ie[low_pos:high_pos], 1)
        temp_e = 1/slope
        return temp_e

    def get_vel_bohm(self, temp_e, type=AR):
        if type == AR:
            amu = MASS_AR_AMU
        elif type == N:
            amu = MASS_N_AMU

        vel_bohm = math.sqrt(temp_e / (amu * MASS_P_EV))
        return vel_bohm
        
    def get_plasma_density(self, i_ion, probe, temp_e, type=AR):
        vel_bohm = self.get_vel_bohm(temp_e, type)
        plasma_density = -i_ion/(0.61 * CHARGE_E_SI * probe.area * vel_bohm)
        return plasma_density
        
    def get_v_plasma(self, v_float, temp_e, type=AR):
        if type == AR:
            amu = MASS_AR_AMU
        elif type == N:
            amu = MASS_N_AMU
        v_plasma = v_float + temp_e * (3.34 + 0.5 * math.log(amu))
        return v_plasma
    
    def smooth_poly(self, x_vals, y_vals, degree):
        poly_coeff = np.polyfit(x_vals, y_vals, degree)
        poly = np.poly1d(poly_coeff)
        return poly 
    
    def dn_poly(self, poly, x_vals, n):
        dn = poly.deriv(n)
        y_vals = dn(x_vals)
        return y_vals
    
    def get_min_pos(self, y_vals):
        y_vals_positive = np.array([abs(y_val) for y_val in y_vals])
        min_pos = np.where(y_vals_positive == y_vals_positive.min())[0][0]
        return min_pos
    
    def get_nearest_pos(self, vals, target):
        distance_vals = np.array([abs(val - target) for val in vals])
        nearest_pos = np.where(distance_vals == distance_vals.min())[0][0]
        return nearest_pos