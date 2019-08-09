# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 11:57:58 2019

@author: falol
"""
# POST PROCESSING MODULE

import numpy as np
from matplotlib import pyplot as plt


def Intersection_Matrix_ColorMap(file_path):
    """
    Function to plot a colormap for visualisation of intersection matrix
    file_path: str, path of file containing intersection matrix
    Returns: None
    """
    # read the file and convert to array
    # data to plot
    # data ==
    # set figure size
    fig = plt.figure(figsize=(12, 12))
    # add a 1x1 grid subplot
    ax = fig.add_subplot(1, 1, 1)
    # set title
    ax.set_title("Intersection Matrix ColorMap", fontsize=16)
    # plot the color map
    plt.imshow(data)
    # set the aspect of axes scaling
    ax.set_aspect("equal")
    # plot color bar
    plt.colorbar()
    # display image
    plt.imshow()
    return None


def Intersection_Hist_3D_Plot(file_path):
    """
    A function to plot the histogram of lengths of intersections of 3D
    fractures in a domain after some simulations.
    file_path: path of file containing lengths of intersection
    Returns: None
    """
    # change the directory to where file is contined
    # read data from file
    # set x and y axes limits
    plt.xlim([min(data), max(data)])
    # plot histogram
    plt.hist(data, color='blue', edgecolor='black', alpha=0.6)
    # set title
    plt.title('3D Histogram of Lengths of Intersection', fontsize=16)
    # set x_label
    plt.xlabel('Length', fontsize=16)
    # set y_label
    plt.ylabel('Frequency', fontsize=16)
    # display histogram
    plt.show()
    return None


def Intersections_per_Fracture_Plot(file_path):
    """
    A function to plot the total intersections per fracture
    file_path: str, the path of the text file containing the intersections
                per fracture
    Returns: None
    """
    # change directory to where the text file is contained
    # os.chdir("/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/text_files")
    # load the file
    intersections = np.loadtxt(file_path)
    # get number of fractures. NB: Number of fractures will be
    # equal length of intersections
    num_frac = len(intersections)
    # create a list of numbers to represent each fracture
    frac = np.linspace(1, num_frac, num_frac)
    # Now plot total intersections vs fracture
    # set x axis to be wholw number
    plt.xticks(frac)
    # make plot
    plt.plot(frac, intersections)
    # set title
    plt.title('Plot of number of intersections per fracture', fontsize=16)
    # set axes labels
    plt.xlabel('fracture number', fontsize=16)
    plt.ylabel('number of intersections', fontsize=16)
    # display plot
    plt.show()
    return None

# Intersections_per_Fracture_Plot("C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/myf.txt")
