# A Discrete Fracture Network Generation and Analysis Library for Use in CAD Software Environments

# Author: 

Name: Falola Yusuf

Email address: fyf17@ic.ac.uk

CID: 01481781


# Introduction

This work introduces an easy to use, open sourced library, Y-Frac, for DFN modelling and analysis. Y-Frac is built upon the python APIs available on Rhinoceros 6. Hence, Y-Frac is fit for use on Rhinoceros software package. Y-Frac can model fracture networks containing circular, elliptical and regular polygonal fractures. This library is computationally cheap for DFN modelling and analysis. Some of the functionalities of this library for DFN analysis include fracture intersection analysis, cut-plane analysis, and percolation analysis. Algorithms for constructing an intersection matrix and determining percolation state of a fracture network are also included in this work. The output text file from this library containing modelled fracture networks’ parameters can serve as input for appropriate software packages to simulate flow and perform mechanical analysis in fracture networks. The practical applicability of Y-Frac was demonstrated by performing percolation threshold analysis of 3D fracture networks and comparing the results to published data. 

![DFN](./images/Rendered.png)

# Requirements
This software expands on Rhiniceros 6 python API. Hence, users need to install the software before using this library.

- Rhinoceros 6, can be donloaded [here](https://www.rhino3d.com/download)
- Rhinoceros 6 hardware requirements can be found [here](https://www.rhino3d.com/6/system_requirements)
- matplotlib >= 3.0.2 for postprocessing

# Installation
- Clone this repository to your computer using the following

`git clone http://github.com/msc-acse/acse-9-independent-research-project-Falfat.git`

- The contents in the file should be copied to the Rhinoceros 6 script folder for use as described below

`~\AppData\Roaming\McNeel\Rhinoceros\6.0\scripts`

