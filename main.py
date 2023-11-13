"""
Created on Fri Oct 27 22:03:52 2023

@author: izattdrake
"""

from Probe import Probe
from IVTrace import IVTrace
from globals import *

def main():
    probe = Probe(radius=0.0015, length=0.01)
    pressure = 10
    power_vals = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    
    for power in power_vals:
        file_path = f'.\\data\\{pressure}mTorr_{power}W.csv'
        IVTrace(file_path, power, pressure, probe=probe)

if __name__ == '__main__':
    main()