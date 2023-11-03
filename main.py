"""
Created on Fri Oct 27 22:03:52 2023

@author: izattdrake
"""

import math
from Probe import Probe
from IVTrace import IVTrace
from globals import *

def main():
    pressure = 10
    power = 100
    file_path = f'.\\data\\{pressure}mTorr_{power}W.csv'
    probe = Probe(radius=0.0015, length=0.01)
    test = IVTrace(file_path, power, pressure, probe=probe)

if __name__ == '__main__':
    main()