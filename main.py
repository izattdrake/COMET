"""
Created on Fri Oct 27 22:03:52 2023

@author: izattdrake
"""

from Probe import Probe
from IVTrace import IVTrace
from globals import *

def main():
    file_path = '.\\data\\10mTorr_50W.csv'
    probe = Probe(radius=0.00615, length=0.012)
    test = IVTrace(file_path, power=50, pressure=10, probe=probe)

if __name__ == '__main__':
    main()