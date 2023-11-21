"""
Created on Fri Oct 27 22:04:16 2023

@author: izattdrake
"""

import math
import sys
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
        self.temp_e_low, self.temp_e_high = self.get_temp_e(self.ie, self.v_bias, v_float_pos)
        self.vel_bohm = self.get_vel_bohm(self.temp_e_low)
        self.plasma_density = self.get_plasma_density(self.i_ion, self.probe, self.temp_e_low, self.type)
        self.v_plasma = self.get_v_plasma(self.v_float, self.temp_e_low)
        self.delta_v = self.get_delta_v(self.v_bias, self.v_plasma)
        self.eedf = self.get_eedf(self.ie, self.v_bias, self.v_float, self.v_plasma, self.delta_v, self.probe)
        # self.write_plasma()
    
    def get_delta_v(self, v_bias, v_plasma):
        delta_v = [val for val in (v_plasma - v_bias) if (val >= 0 and val <= v_bias.max())]
        delta_v.reverse()
        return delta_v

    def get_eedf(self, ie, v_bias, v_float, v_plasma, delta_v, probe):
        v_float_pos = self.get_nearest_pos(v_bias, v_float)
        v_plasma_pos = self.get_nearest_pos(v_bias, v_plasma)

        sqrt_delta_v = np.sqrt(delta_v)

        delta_v_full = [val for val in (v_plasma - v_bias)]
        delta_v_full.reverse()
        poly = self.smooth_poly(v_bias, ie, 9)
        d2_ie = self.dn_poly(poly, delta_v, 2)
        
        list = []
        for i in range(d2_ie.size):
            const = 2 * math.sqrt(2 * MASS_E_SI / CHARGE_E_SI**3) / probe.area
            # print('{:e}'.format(val))
            val = const * sqrt_delta_v[i] * d2_ie[i]
            list.append(val)

        eedf = np.array(list)
        self.plot(delta_v, list, "EEDF")
        sys.exit()
        return eedf
    
    def get_i_ion(self, i, v_bias, v_float, v_float_pos):
        slope, intercept = np.polyfit(v_bias[0:v_float_pos], i[0:v_float_pos], 1)
        i_ion = slope * v_float + intercept
        return i_ion
            
    def get_v_float(self, v_bias, v_float_pos):
        v_float = v_bias[v_float_pos]
        return v_float
    
    def get_temp_e(self, ie, v_bias, v_float_pos):
        ln_ie = np.log(ie)

        low_pos_low = self.get_first_pos(ln_ie)
        high_pos_low = low_pos_low + 2
        slope, intercept = np.polyfit(v_bias[low_pos_low:high_pos_low], ln_ie[low_pos_low:high_pos_low], 1)
        temp_e_low = 1/slope

        low_pos_high = self.get_nearest_pos(v_bias, 20)
        high_pos_high = self.get_nearest_pos(v_bias, 25)
        slope, intercept = np.polyfit(v_bias[low_pos_high:high_pos_high], ln_ie[low_pos_high:high_pos_high], 1)
        temp_e_high = 1/slope

        return temp_e_low, temp_e_high

    def get_vel_bohm(self, temp_e, type=AR):
        if type == AR:
            amu = MASS_AR_AMU
        elif type == N:
            amu = MASS_N_AMU
        vel_bohm = math.sqrt(temp_e / (amu * MASS_P_EV))
        return vel_bohm
        
    def get_plasma_density(self, i_ion, probe, temp_e_low, type=AR):
        vel_bohm = self.get_vel_bohm(temp_e_low, type)
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
    
    def get_first_pos(self, vals):
        for val in vals:
            if not np.isnan(val):
                first_pos = np.where(vals == val)[0][0]
                return first_pos
        
    def plot(self, x_vals, y_vals, title, show=True):
        plt.plot(x_vals, y_vals, 'o--')
        plt.title(title)
        plt.grid()
        
        if show:
            plt.show()

    def write_plasma(self, write_data=True, write_figs=True):
        lines = [
            f'Plasma Type: {self.type}',
            f'Probe Length: {self.probe.length} m',
            f'Probe Radius: {self.probe.radius} m',
            f'Pressure: {self.pressure} mTorr',
            f'Power: {self.power} W',
            f'Floating Potential: {self.v_float} V',
            f'Ion Current: {-self.i_ion} A',
            f'Electron Temperature Low: {self.temp_e_low} eV',
            f'Electron Temperature High: {self.temp_e_high} eV',
            f'Bohm Velocity: {self.vel_bohm} m/s',
            f'Plasma Density: {"{:e}".format(self.plasma_density)} m^-3',
            f'Plasma Potential: {self.v_plasma} V'
        ]

        label = f'{self.pressure}mTorr_{self.power}W'
        path_output_IVTrace = f'output/IVTrace/{label}'
        os.makedirs(path_output_IVTrace, exist_ok=True)
        path_txt = f'{path_output_IVTrace}/{label}.txt'
        path = os.path.join(os.path.dirname(__file__), path_txt)

        if write_data:
            with open(path, 'w') as file:
                file.write('\n'.join(lines))

        if write_figs:
            self.plot(self.v_bias, self.i, f'IV Trace {label}', show=False)
            plt.savefig(f'{path_output_IVTrace}/IVTrace_{label}.png')
            plt.clf()

            self.plot(self.v_bias, np.log(self.ie), f'ln(Electron Current) vs Bias Voltage {label}', show=False)
            plt.savefig(f'{path_output_IVTrace}/ln(ie)_{label}.png')
            plt.clf()

            self.plot(self.delta_v, np.flip(self.eedf), f'EEDF {label}', show=False)
            plt.savefig(f'{path_output_IVTrace}/eedf.png')
            plt.clf()

        