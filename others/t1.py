import numpy as np
import streamlit as st

def bending_moment(support_moments, point_loads, distributed_loads, external_moments, beam_length, resolution):
    """
    Calculates bending moment along the length of the beam.

    Parameters:
        support_moments (list of tuples): [(position, moment)], support moments at fixed positions.
        point_loads (list of tuples): [(position, magnitude)], point loads along the beam.
        distributed_loads (list of tuples): [(start_pos, end_pos, start_mag, end_mag)], linearly varying loads.
        external_moments (list of tuples): [(position, magnitude)], moments applied at specific positions.
        beam_length (float): Length of the beam.
        resolution (float): Step size for calculating moments.

    Returns:
        x_coords (numpy array): Positions along the beam.
        moment (numpy array): Bending moment values at each position.
    """
    # Generate positions along the beam
    x_coords = np.arange(0, beam_length + resolution, resolution)
    moment = np.zeros_like(x_coords)

    # Add support moments to the bending moment
    if support_moments:
        for position, magnitude in support_moments:
            for i, x in enumerate(x_coords):
                if x >= position:
                    moment[i] += magnitude

    # Add point loads to the bending moment
    for position, magnitude in point_loads:
        for i, x in enumerate(x_coords):
            if x >= position:
                moment[i] += magnitude * (x - position)

    # Add distributed loads to the bending moment
    for start_pos, end_pos, start_mag, end_mag in distributed_loads:
        for i, x in enumerate(x_coords):
            if start_pos <= x <= end_pos:
                # Calculate the load at position x
                load = start_mag + (end_mag - start_mag) * ((x - start_pos) / (end_pos - start_pos))
                for j, y in enumerate(x_coords):
                    if y >= x:
                        moment[j] += load * (y - x) * (x_coords[1] - x_coords[0])

    # Add external moments
    for position, magnitude in external_moments:
        for i, x in enumerate(x_coords):
            if x >= position:
                moment[i] += magnitude

    return x_coords, moment
