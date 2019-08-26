# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 11:57:58 2019

@author: falol
"""
# POST PROCESSING MODULE

import numpy as np
from matplotlib import pyplot as plt


def IntersectionMatrixColorMap(matrix_data):
    """
    Function to plot and save a colormap for visualisation of intersection
    matrix

    Parameter
    --------
    matrix_data: list of lists, a square matrix of interstions

    Returns: None
    """
    # set figure size
    fig = plt.figure(figsize=(12, 12))
    # add a 1x1 grid subplot
    ax = fig.add_subplot(1, 1, 1)
    # set title
    ax.set_title("Intersection Matrix ColorMap", fontsize=16)
    # plot the color map
    plt.imshow(matrix_data)
    # set the aspect of axes scaling
    ax.set_aspect("equal")
    # plot color bar
    plt.colorbar()
    # save figure
    plt.savefig('colormap')
    return None


def IntersectionHistogram(lengths_list):
    """
    A function to plot and save the histogram of lengths of intersections of 3D
    fractures in a domain after some simulations.

    Parameter
    --------
    lengths_list: list of lengths of intersection
    Returns: None
    """
    # set x and y axes limits
    plt.xlim([min(lengths_list), max(lengths_list)])
    # plot histogram
    plt.hist(lengths_list, color='blue', edgecolor='black', alpha=0.6)
    # set title
    plt.title('Histogram of Lengths of Intersection', fontsize=16)
    # set x_label
    plt.xlabel('Length', fontsize=16)
    # set y_label
    plt.ylabel('Frequency', fontsize=16)
    # save histogram
    plt.savefig('intersection_histogram')
    # display histogram
    plt.show()
    return None


def IntersectionsPerFracturePlot(intersection_list):
    """
    A function to plot and save the total intersections per fracture

    Parameter
    --------
    intersection_list: list, list containing the intersections
                per fracture
    Returns: None
    """
    # get number of fractures. NB: Number of fractures will be
    # equal length of intersections
    num_frac = len(intersection_list)
    print(num_frac)
    # create a list of numbers to represent each fracture
    frac = np.linspace(1, num_frac, num_frac)
    # Now plot total intersections vs fracture
    # set x axis to be wholw number
    fig = plt.figure(figsize=(14, 12))
    ax1 = fig.add_subplot(111)
    # set x axis markers as integers
    plt.xticks(frac)
    # make plot
    ax1.plot(frac, intersection_list, 'ro')
    # set title
    plt.title('Plot of number of intersections per fracture', fontsize=16)
    # set axes labels
    plt.xlabel('fracture number', fontsize=16)
    plt.ylabel('number of intersections', fontsize=16)
    # save plot
    plt.savefig('intersection_per_fracture')
    # display plot
    plt.show()
    return None

# Intersections_per_Fracture_Plot("C:/Users/falol/AppData/Roaming/McNeel/Rhinoceros/6.0/scripts/myf.txt")
