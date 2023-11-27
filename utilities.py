import numpy as np

def get_min_pos(vals):
    abs_vals = [abs(val) for val in vals]
    min_pos = abs_vals.index(min(abs_vals))
    return min_pos

def get_nearest_pos(vals, target):
    diff_vals = [abs(val - target) for val in vals]
    nearest_pos = diff_vals.index(min(diff_vals))

def get_first_pos(vals):
    for val in vals:
        if not np.isnan(val):
            first_pos = np.where(vals == vals)[0][0]
            return first_pos
        
def smooth_poly(x_vals, y_vals, degree):
    poly_coeff = np.polyfit(x_vals, y_vals, degree)
    poly = np.poly1d(poly_coeff)
    return poly

def dn_poly(poly, vals, n):
    dn = poly.deriv(n)
    dn_vals = dn(vals)
    return dn_vals