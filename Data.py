"""
Created on Fri Oct 27 22:04:16 2023

@author: izattdrake
"""

import csv
import os
import re
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from Probe import Probe
from Plasma import Plasma
from globals import *

class Data:
    """
    Contains an arbitrary amount of plasmas and data analysis methods for them
    """
    def __init__(self, file_paths: list[str], probe: Probe = None):
        """
        @file_paths: Data path locations
        """
        self.file_paths = file_paths
        self.plasmas: list[Plasma] = []
    
        for file_path in self.file_paths:
            i, v_bias = __class__.read_file(file_path)
            params = re.findall( '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', file_path)

            pressure = params[0]
            power = params[1]
            freq = params[2]

            plasma = Plasma(i, v_bias, pressure, power, freq, probe)   
             
            self.plasmas.append(plasma)          

    def write_plasmas(self) -> None:
        """
        Saves plasma data to an output folder. Currently, calculated plasma parameters are saved to a text file
        while plots of the IVTrace, the log of electron current (used to calculate electron temperature),
        electron energy distribution function, and a comparison of plasma parameters varying with
        power are saved
        """
        for plasma in self.plasmas:
            lines = [
                f'Plasma Type: {plasma.type}',
                f'Probe Length: {plasma.probe.length} m',
                f'Probe Radius: {plasma.probe.radius} m',
                f'Pressure: {plasma.pressure} mTorr',
                f'Power: {plasma.power} W',
                f'Floating Potential: {plasma.v_float} V',
                f'Ion Current: {-plasma.i_ion} A',
                f'Electron Temperature: {plasma.temp_e} eV',
                f'Plasma Density: {"{:e}".format(plasma.density)} m^-3',
                f'Plasma Potential: {plasma.v_plasma} V'
            ]

            plasma_label = f'{plasma.pressure}mTorr_{plasma.power}W_{plasma.freq}KHz'
            folder_path = os.path.join(os.path.dirname(__file__), f'output/{plasma_label}')
            os.makedirs(folder_path, exist_ok=True)

            with open(f'{folder_path}/parameters.txt', 'w') as txt:
                txt.write('n'.join(lines))

            self.plot(plasma.v_bias, plasma.i, x_label='Bias Voltage (V)', 
                      y_label='Current (A)', title=f'IV Trace', show=False, write_path=f'{folder_path}/IVTrace.png')

            self.plot(plasma.v_bias, np.log(plasma.ie), x_label='Bias Voltage (V)',
                      y_label='Log(Ie)', title=f'log(Electron Current) vs Bias Voltage', 
                      show=False, write_path=f'{folder_path}/log.png')

            self.plot(self.delta_v, np.flip(self.eedf), x_label='Plasma Potential - Bias',
                      y_label='EEDF', title='Electron Energy Distribution Function', show=False,
                      write_path=f'{folder_path}/EEDF.png')

    @staticmethod
    def read_file(file_path: str) -> tuple[list[float], list[float]]:
        """
        Returns an array for each data column in a CSV file
        @file_path: CSV file location
        """
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            col1 = []
            col2 = []
            for row in csv_reader:
                col1.append(float(row[0]))
                col2.append(float(row[1]))

        return col1, col2

    @staticmethod 
    def plot(x_vals: list[float], y_vals: list[float], x_label: str = None, y_label: str = None, 
             title: str = None, show: bool = True, write_path: str = None) -> None:
        """
        Streamlines matplotlib functionality in a single method
        @x_vals: Values on the horizontal axis
        @y_vals: Values on the vertical axis
        @x_label: Label on the horizontal axis
        @y_label: Label on the vertical axis
        @title: Title of plot
        @show: Show the plot or not
        @write_path: Path to save plot if desired
        """
        plt.plot(x_vals, y_vals, 'o--')
        plt.title(title)
        if x_label: plt.xlabel(x_label)
        if y_label: plt.ylabel(y_label)
        if title: plt.title(title)
        plt.grid()
        if show: plt.show()
        if write_path: plt.savefig(write_path)

        plt.clf()
        