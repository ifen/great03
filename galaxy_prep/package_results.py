__author__ = 'Ian Fenech Conti'

"""
GREAT3 - Results Packaging.

This code is responsible for handling the lensift results interpretation,
which will be used for statistical analysis on the outputs.
"""

import numpy as np
import matplotlib.pyplot as plt
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# defining the results file paramaters
PARAMS = {'WSC_X': 0,
          'WSC_Y': 1,
          'E1': 2,
          'E2': 3,
          'WEIGHT': 4,
          'FIT_CLASS': 5,
          'SCALE_LENGTH': 6,
          'BULGE_FRACTION': 7,
          'MODEL_FLUX': 8,
          'PIXEL_SN_RATIO': 9,
          'MODEL_SN_RATIO': 10,
          'PSF_E1': 11,
          'PSF_E2': 12,
          'PSF_STREHL': 13,
          'STAR_GALAXY_F_PROBABILITY': 14,
          'FIT_PROBABILITY': 15,
          'MEASUREMENT_VARIANCE': 16,
          'MEAN_LIKELIHOOD_E': 17,
          'MEAN_LIKELIHOOD_E1': 18,
          'MEAN_LIKELIHOOD_E2': 19,
          'CAT_MAG': 20,
          'N_EXPOSURES': 21,
          'CAT_ID': 22}


def plot_attribute(output_path, attribute_1, attribute_2, save_path):

    """
    @param output_path: The path to the output file where results are
    stored.
    @param attribute_1: The attribute to be plot on the X-axis.
    @param attribute_2: The attribute to be plot on the Y-axis.
    @param save_path: The dir. path to the folder where the plots will
    be svaed
    @return: returns the path of the plot that was saved.
    """

    data_table = load_datatable(output_path, True)
    attribute_1_data = extract_parameter(PARAMS[attribute_1], data_table)
    attribute_2_data = extract_parameter(PARAMS[attribute_2], data_table)

    path = plot_results([val[0] for val in attribute_1_data],
        [val[0] for val in attribute_2_data],
        attribute_1,
        attribute_2,
        save_path)

    return path


def compare_outputs(output_1, output_2):

    """
    @param output_1: The X-value to be compared.
    @param output_2: The Y-value to be compared.
    """

    lensfit_standard = load_datatable(output_1, True)
    lensfit_celestial = load_datatable(output_2, True)

    lensfit_standard_e1 = extract_parameter(PARAMS['E1'], lensfit_standard)
    lensfit_celestial_e1 = extract_parameter(PARAMS['E2'], lensfit_celestial)

    plot_results([val[0] for val in lensfit_standard_e1],
                 [val[0] for val in lensfit_celestial_e1],
                 'Correct Distortion : 1 (e2)',
                 'Correct Distortion : 0 (e2)',
                 '')


def load_datatable(output_path, exclude_failed):

    """
    @param output_path: Path to output file.
    @param exclude_failed: Include the galaxies that failed the lensfit
    fit test.
    @return: A list of filtered values, read from the lensfit .out file.
    """

    data_table = np.genfromtxt(output_path, dtype=None)
    filtered_results = []

    for data_entry in data_table:
        if data_entry[PARAMS['FIT_CLASS']] > -1:
            filtered_results.append(data_entry)

    return filtered_results


def processed_galaxies(output_path):

    """
    @param output_path: Path to lensfit out file.
    @return: The number of galaxies that passed the lensfit fit test.
    """

    data_table = np.genfromtxt(output_path, dtype=None)

    count = 0
    for data_entry in data_table:
        if data_entry[PARAMS['FIT_CLASS']] > -1:
            count += 1

    return count


def extract_parameter(paramater, data_table):

    """
    @param paramater: Extract this paramater from the data_table.
    @param data_table: A loaded list with lensfit output values.
    @return: A list of the requested paramater.
    """

    filtered_results = []
    for data_entry in data_table:
        filtered_results.append([data_entry[paramater],
                                 data_entry[PARAMS['CAT_ID']]])

    return filtered_results


def plot_results(x_value, y_value, x_title, y_title, save_path):

    """
    @param x_value: A List of values to be plot on the X-axis.
    @param y_value: A list of values to be plot on the Y-axis.
    @param x_title: A string rep. the X title name.
    @param y_title: A string rep. the Y title name.
    @param save_path: Path where the plot is to be saved.
    @return: A path to where the plot was saved.
    """

    plt.figure()
    plt.plot(x_value, y_value, 'bo', markersize=0.8)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title('Lensfit Analysis')
    if save_path:
        fig_path = save_path + ' ' + x_title + '_v_' + y_title + '.png'
        print 'saving plot ' + fig_path
        plt.savefig(fig_path)
        return fig_path
    else:
        plt.draw()


def email_results(subject, add_to, add_from, content, image_paths):

    """
    @param subject: Subject of email.
    @param add_to: To address of email.
    @param add_from: From address of email.
    @param content: Email HTML content.
    @param image_paths: Paths to image plots to be attached.
    """

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = add_to
    msg['To'] = add_from

    text = MIMEText(content, 'html')
    msg.attach(text)

    for image_path in image_paths:
        image = get_image_data(image_path)
        image_attachment = MIMEImage(image, name=os.path.basename(image_path))
        msg.attach(image_attachment)

    config_file = open('/home/ian/Documents/GREAT03/utils/email_settings.config', 'r')
    config_contents = config_file.readline()

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('ianfc89@gmail.com', config_contents)
    s.sendmail(add_from, add_to, msg.as_string())
    s.quit()


def get_image_data(img_path):

    """
    @param img_path: Path to plot.
    @return: A binary image of the plot.
    """

    return open(img_path, 'rb').read()

