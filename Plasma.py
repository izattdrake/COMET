"""
Created on Mon Nov 20 22:14:00 2023

@author: izattdrake
"""

import csv
import numpy as np
import math
from Probe import Probe
from globals import *
from utilities import *

class Plasma:
    """
    Object that contains and computes plasma parameters 
    """
    def __init__(self, i: list[float], v_bias: list[float], pressure: float, power: float, freq: float, probe: Probe, type: str = AR):
        """
        @i: The langmuir probe's induced current
        @v_bias: The voltage applied to langmuir probe from SMU
        @pressure: The COMET chamber's pressure
        @power: The power applied by COMET power supplies
        @freq: The frequency of applied RF signal. Usually 13.56 or 60KHz
        @probe: The langmuir probe's properties
        @type: The plasma matter
        """
        
        self.pressure = pressure
        self.power = power
        self.freq = freq
        self.probe = probe
        self.type = type
        self.i = i
        self.v_bias = v_bias
        
        if self.type == AR:
            self.amu = MASS_AR_AMU
        elif self.type == N:
            self.amu = MASS_N_AMU

        v_float_pos = get_min_pos(self.i)
        self.v_float = self.v_bias[v_float_pos]

        slope, intercept = np.polyfit(self.v_bias[0:v_float_pos], self.i[0:v_float_pos], 1)
        self.i_ion = slope*self.v_float + intercept
        self.ie = self.i - self.i_ion
        ln_ie = np.log(self.ie)
        low_pos = get_first_pos(ln_ie)
        high_pos = low_pos + 2

        slope, intercept = np.polyfit(self.v_bias[low_pos:high_pos], ln_ie[low_pos:high_pos], 1)
        self.temp_e = 1/slope

        bohm_vel = math.sqrt(self.temp_e/(self.amu*MASS_P_EV))
        self.density = -self.i_ion/(0.61*CHARGE_E_SI*self.probe.area *bohm_vel)
        self.v_plasma = self.v_float + self.temp_e*(3.34 + 0.5*math.log(self.amu))
        v_plasma_pos = get_nearest_pos(self.v_bias, self.v_plasma)
        delta_v = [val for val in (self.v_plasma - self.v_bias) if (val >= 0 and val <= max(self.v_bias))]
        delta_v.reverse()
        sqrt_delta_v = np.sqrt(delta_v)
        ie_poly = smooth_poly(self.v_bias, self.ie, 9)
        d2_ie = dn_poly(ie_poly, delta_v, 2)

        eedf = []
        for i in range(len(d2_ie)):
            k = 2*math.sqrt(2*MASS_E_SI/CHARGE_E_SI**3)/self.probe.area
            eedf_val = k*sqrt_delta_v[i]*d2_ie[i]
            eedf.append(eedf_val)
        