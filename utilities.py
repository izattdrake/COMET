def get_min_pos(vals):
    abs_vals = [abs(val) for val in vals]
    min_pos = abs_vals.index(min(abs_vals))
    return min_pos

def get_nearest_pos(vals, target):
    diff_vals = [abs(val - target) for val in vals]
    nearest_pos = diff_vals.index(min(diff_vals))

