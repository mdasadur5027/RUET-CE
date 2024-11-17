import numpy as np
beam_length = 2
resolution = 2
shear = [0.0] * (int(beam_length * resolution) + 1)
print(len(shear))
x_coords = np.linspace(0, beam_length, len(shear))
print(len(x_coords))
print(x_coords)