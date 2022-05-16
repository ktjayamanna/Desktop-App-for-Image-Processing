# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 14:45:59 2021
@Description: This allows you to contrast stretch to different levels.
@Reference:https://realpython.com/pysimplegui-python/#integrating-opencv-with-pysimplegui
@author: kjayamanna
"""
import numpy as np
import matplotlib
matplotlib.rcParams.update({'font.size': 8})
#%%
# =============================================================================
# Functions
# =============================================================================
#%%
def histogram(f):
    #Define 8 bit gray levels.
    f_grey_levels = np.array(range(0,256))
    #Define a placeholder for the histogram.
    hist = np.zeros(f_grey_levels.shape)
    #Find the frequency count for each gray level.
    for i in np.nditer(f, order = 'C'):
        hist[i] = hist[i] + 1
    return hist
#%%
def customEq(f, hist, a, b, c, d):
    #Define 8-bit gray levels
    f_grey_levels = np.array(range(0,256))
    #Initialize the output graylevel map.
    qp = np.copy(f_grey_levels)
    #Check for invalid ranges
    if sum(hist[a:b+1]) == 0 or sum(hist[c:d+1]) == 0:
        return qp
    else:
        #Calcualte the total frequency of the input range.
        hist_total1 = sum(hist[a:b+1])
        #Calculate the cumilative total frequncy of the input range.
        hist_cum1 = np.zeros(hist.shape)
        hist_cum1[a] = hist[a]
        for i in range(a + 1,b + 1):
            hist_cum1[i] = hist[i] + hist_cum1[i-1]
        #Calculate qp for the given ranges.
        for i in range(a, b + 1):
            qp[i] = round((d - c) * hist_cum1[i]/hist_total1) + c
        return qp
#%%
def plot_hist(img,qp):
    #Define the 8 bit gray levels.
    f_grey_levels = np.array(range(0,256))
    img = np.array(img)
    #% Derive the Equalized Image
    img_eq = np.copy(img)
    #%% Reflect the changes in the output image.
    for ix,iy in np.ndindex(img.shape):
        img_eq[ix,iy] = qp[img[ix,iy]]
    #Generate the histogram for the original image.
    hist_org = histogram(img)
    #Generate the histogram for the equalized image.
    hist_eq = histogram(img_eq)
    #Generate a matplotlib figure.
    fig = matplotlib.figure.Figure(figsize=(10, 6), dpi=100)
    #Add display features to the figure.
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.title.set_text('Original Histogram')
    ax1.bar(f_grey_levels, hist_org)
    ax2.title.set_text('The Equalized Histogram')
    ax2.bar(f_grey_levels, hist_eq)
    return img_eq,fig
#%%
# =============================================================================
# #%% Application Example
# =============================================================================
#%%
#Input Range
# a = 97
# b = 214
#Output Range
# c = 20
# d = 25
#Input filename
# filename = r'C:\Users\keven\OneDrive - University of Nebraska at Omaha\Fall 2021\CSCI 8300\Pictures\insta.png'
#Open the file and convert to gray scale.
# img = Image.open(filename).convert('L')
#Generate the Histogram
# hist = histogram(img)

#%%
#Find qp
# qp = customEq(img, hist, a, b, c, d)
#Get the histogram plots and the equalized Image
# img_eq, fig= plot_hist(img, qp)






    

