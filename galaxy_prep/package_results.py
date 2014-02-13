__author__ = 'Ian Fenech Conti'

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------
# defining the results file paramaters
WSC_X = 0
WSC_Y = 1
E1 = 2
E2 = 3
WEIGHT = 4
FIT_CLASS = 5
SCALE_LENGTH = 6
BULGE_FRACTION = 7
MODEL_FLUX = 8
PIXEL_SN_RATIO = 9
MODEL_SN_RATIO = 10
PSF_E1 = 11
PSF_E2 = 12
PSF_STREHL = 13
STAR_GALAXY_F_PROBABILITY = 14
FIT_PROBABILITY = 15
MEASUREMENT_VARIANCE = 16
MEAN_LIKELIHOOD_E = 17
MEAN_LIKELIHOOD_E1 = 18
MEAN_LIKELIHOOD_E2 = 19
CAT_MAG = 20
N_EXPOSURES = 21
CAT_ID = 22


def package_results(output_standard, output_celestial):
    lensfit_standard = load_datatable(output_standard, True)
    lensfit_celestial = load_datatable(output_celestial, True)

    lensfit_standard_e1 = extract_parameter(E2, lensfit_standard)
    lensfit_celestial_e1 = extract_parameter(E2, lensfit_celestial)

    plot_results([val[0] for val in lensfit_standard_e1],
                 [val[0] for val in lensfit_celestial_e1],
                 'Correct Distortion : 1 (e2)',
                 'Correct Distortion : 0 (e2)')

def load_datatable(output_path, exclude_failed):
    data_table = np.genfromtxt(output_path, dtype=None)
    filtered_results = []

    for data_entry in data_table:
        if data_entry[FIT_CLASS] != exclude_failed:
            filtered_results.append(data_entry)

    return filtered_results

def extract_parameter(paramater, data_table):
    filtered_results = []
    for data_entry in data_table:
        filtered_results.append([data_entry[paramater],
                                 data_entry[CAT_ID]])

    return filtered_results

def plot_results(x_value, y_value, x_title, y_title):
    plt.figure()
    plt.plot(x_value, y_value, 'ro', markersize=1.5)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title('Lensfit Analysis')
    plt.show()


