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
    Contains an arbitrary amount of plasmas and holds data analysis methods for them
    """
    def __init__(self, file_paths: list[str], probe: Probe = None):
        """
        @file_paths: Data path locations
        """
        self.file_paths = file_paths
        self.plasmas = []
    
        for file_path in self.file_paths:
            i, v_bias = __class__.read_file(file_path)
            params = re.findall( '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', file_path)

            pressure = params[0]
            power = params[1]
            freq = params[2]

            plasma = Plasma(i, v_bias, pressure, power, freq, probe)   
             
            self.plasmas.append(plasma)          

    def write_plasmas(self, write_txt: bool = True, write_figs: bool = True):
        if write_txt:
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

                path_output = f'output/{self.label}'
                os.makedirs(path_output, exist_ok=True)
                path_txt = f'{path_output}/{label}.txt'
                path = os.path.join(os.path.dirname(__file__), path_txt)

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
    def plot(x_vals: list[float], y_vals: list[float], title: str, show: bool = True) -> None:
        """
        Streamlines matplotlib functionality in a single method
        @x_vals: Values on the horizontal axis
        @y_vals: Values on the vertical axis
        @title: Title of figure
        @show: Show the figure or not
        """
        plt.plot(x_vals, y_vals, 'o--')
        plt.title(title)
        plt.grid()
        
        if show:
            plt.show()

        plt.clf()
        