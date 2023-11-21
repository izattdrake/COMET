"""
Created on Fri Oct 27 22:03:52 2023

@author: izattdrake
"""

import math
import os
from matplotlib import pyplot as plt
from Probe import Probe
from Plasma import Plasma
from IVTrace import IVTrace
from globals import *

def main():
    plot_figs = False
    probe = Probe(radius=0.5*10**(-3), length=0.01)
    pressure = 10
    power_vals = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    trace_vals = []
    for power in power_vals:
        file_path = f'.\\data\\{pressure}mTorr_{power}W.csv'
        plasma = Plasma(file_path, power, pressure, probe)
        trace = IVTrace(file_path, power, pressure, probe)
        trace_vals.append(trace)
    
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
        if show:
            plt.show()

        label = f'{self.pressure}mTorr_{self.power}W'
        path_output_IVTrace = f'output/IVTrace/{label}'
        os.makedirs(path_output_IVTrace, exist_ok=True)
        path_txt = f'{path_output_IVTrace}/{label}.txt'
        path = os.path.join(os.path.dirname(__file__), path_txt)

        if write_data:
            with open(path, 'w') as file:
                file.write('\n'.join(lines))

        if write_graphs:
            self.plot(self.v_bias, self.i, f'IV Trace {label}', show=False)
            plt.savefig(f'{path_output_IVTrace}/IVTrace_{label}.png')
            plt.clf()

            self.plot(self.v_bias, np.log(self.ie), f'ln(Electron Current) vs Bias Voltage {label}', show=False)
            plt.savefig(f'{path_output_IVTrace}/ln(ie)_{label}.png')
            plt.clf()
        """
    
if __name__ == '__main__':
    main()