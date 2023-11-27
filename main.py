"""
Created on Fri Oct 27 22:03:52 2023

@author: izattdrake
"""

import math
import os
from matplotlib import pyplot as plt
from Probe import Probe
from Plasma import Plasma
from Data import Data
from globals import *
from utilities import *

def main():
    plot_figs = False
    probe = Probe(radius=0.5*10**(-3), length=0.01)
    pressure = 10
    freq = 13.6
    powers = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    file_paths = []

    for power in powers:
        file_path = f'.\\input\\{pressure}mTorr_{power}W_{freq}KHz.csv'
        file_paths.append(file_path)

    data = Data(file_paths, probe)
    
    """
    if plot_figs:
        path_figs = f'output/IVTrace/VsPower'
        os.makedirs(path_figs, exist_ok=True)
        v_float_vals = [trace.v_float for trace in trace_vals]
        i_ion_vals = [trace.i_ion for trace in trace_vals]
        temp_e_low_vals = [trace.temp_e_low for trace in trace_vals]
        temp_e_high_vals = [trace.temp_e_high for trace in trace_vals]
        plasma_density_vals = [trace.plasma_density for trace in trace_vals]
        v_plasma_vals = [trace.v_plasma for trace in trace_vals]

        plt.plot(power_vals, v_float_vals, 'o--')
        plt.xlabel('Power (W)')
        plt.ylabel('Floating Potential (V)')
        plt.title('Floating Potential vs Power')
        plt.grid()
        plt.savefig(f'{path_figs}/floating_potential.png')
        plt.clf()

        plt.plot(power_vals, i_ion_vals, 'o--')
        plt.xlabel('Power (W)')
        plt.ylabel('Ion Current (A)')
        plt.title('Ion Current vs Power')
        plt.grid()
        plt.savefig(f'{path_figs}/ion_current.png')
        plt.clf()

        plt.plot(power_vals, temp_e_low_vals, 'o--', label='Low Electron Temp')
        plt.plot(power_vals, temp_e_high_vals, 'o--', label='High Electron Temp')
        plt.xlabel('Power (W)')
        plt.ylabel('Electron Temperature (eV)')
        plt.title('Electron Temperature vs Power')
        plt.grid()
        plt.savefig(f'{path_figs}/electron_temperature.png')
        plt.clf()
        
        plt.plot(power_vals, plasma_density_vals, 'o--')
        plt.xlabel('Power (W)')
        plt.ylabel('Plasma Density (m^-3)')
        plt.title('Plasma Density vs Power')
        plt.grid()
        plt.savefig(f'{path_figs}/plasma_density.png')
        plt.clf()
        
        plt.plot(power_vals, v_plasma_vals, 'o--')
        plt.xlabel('Power(W)')
        plt.ylabel('Plasma Potential (V)')
        plt.title('Plasma Potential vs Power')
        plt.grid()
        plt.savefig(f'{path_figs}/plasma_potential.png')
        plt.clf()
    """
        
if __name__ == '__main__':
    main()