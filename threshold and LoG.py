# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 09:28:20 2021
@Description: This runs the GUI for image binarization and LoG Edge detection.
@author: kjayamanna
@Reference:https://realpython.com/pysimplegui-python/#integrating-opencv-with-pysimplegui
"""
import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import  Image
import os
import io
#%%
def main():
    file_list_column = [

        [
            #Define Image Folder
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],

        [
            #Define Image File List
            sg.Listbox(
                values=[], enable_events=True, size=(60, 10), key="-FILE LIST-"
            )
        ],
    ]
    
    #Display a message to choose an image.
    image_viewer_column = [
        [sg.Text("Choose an image from list on left:")],
        [sg.Text(size=(1, 10), key="-TOUT-")],
    ]
    
    #Define the Color of the GUI
    sg.theme("DarkBrown")

    # Define the window layout
    layout = [
        
        #Define Image Loading Panel
        [sg.HorizontalSeparator()],
        [sg.Text("Image Loading Panel", size=(100, 1), justification="center", font=("Courier ", 15,('italic','bold')))],
        [sg.HorizontalSeparator()],
            [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ],
           
        #Define Image Display Panel
        [sg.HorizontalSeparator()],
        [sg.Text("Image Display Panel", size=(100, 1), justification="center", font=("Courier ", 15,('italic','bold')))],
        [sg.HorizontalSeparator()], 
        [sg.Image(filename="", key="-IMAGE-")],
        [sg.HorizontalSeparator()],
        [sg.Text("Input Panel", size=(100, 1), justification="center", font=("Courier ", 15,('italic','bold')))],
        [sg.HorizontalSeparator()],
        [sg.Radio("None", "Radio", True, size=(10, 1))],
        [
            #Define the slider for Binarization
            sg.Radio("Binarization", "Radio", size=(10, 1), key="-THRESH-"),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-THRESH SLIDER-",
            ),
        ],
        [
            #Define the Slider for LoG
            sg.Radio("LoG", "Radio", size=(10, 1), key="-LoG-"),
            sg.Slider(
                (0.1, 5.0),
                default_value = 4.0,
                resolution = 0.1,
                tick_interval= None,
                orientation="h",
                size=(20, 15),
                key="-Sigma Value-",
            ),

        ],
        #Define the Action Panel
        [sg.HorizontalSeparator()],
        [sg.Text("Action Panel", size=(100, 1), justification="center",font=("Courier ", 15,('italic','bold')))],
        [sg.HorizontalSeparator()],
        
        #Define the Exit Button
        [sg.Button("Exit", size=(10, 1))],
    ]

    # Create the window and show it without the plot
    window = sg.Window("CSCI 8300 Project Deliverable A Part I", layout, location=(800, 400))

    while True:
        #Poll every 20S 
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".gif", "jpg", "jpeg"))
            ]
            window["-FILE LIST-"].update(fnames)
        #Join the filepaths
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            #Open the selected image and convert it to a grayscale image.
            myImage = Image.open(filename).convert('L')
            #Resize the image
            myImage.thumbnail((400, 400))
            #Save the Image as PNG
            bio = io.BytesIO()
            myImage.save(bio, format="PNG")
            #Grab the image that was just saved.
            window["-IMAGE-"].update(data=bio.getvalue())
            #Make a copy of the input PNG Image
            frame = np.copy(myImage)
            
            #If the user has selected binarization, load the slider values to the openCV command.
            if values["-THRESH-"]:
                frame = cv2.threshold(
                    frame, values["-THRESH SLIDER-"], 255, cv2.THRESH_BINARY
                )[1]
            #If the user selected LoG, load the slider values to the variable sigma. 
            elif values["-LoG-"]:
                #find the kernel size
                sigma = values['-Sigma Value-']
                kernel_size = np.ceil((6 * sigma + 1)) // 2 * 2 + 1
                #Convert to integer
                kernel_size = int(kernel_size)
                #Limit the Kernel size to 31
                if (kernel_size > 31):
                    kernel_size = 31
                #Blurr the image with Gaussian low pass filtering.
                frame = cv2.GaussianBlur(frame,(kernel_size,kernel_size),cv2.BORDER_DEFAULT)
                #Find the laplacian output of the blurred image.
                frame = cv2.Laplacian(
                    frame,
                    cv2.CV_16S,
                    ksize = int(kernel_size)
                )
                #Use morphological operators to find the zero crossings.
                minLoG = cv2.morphologyEx(frame, cv2.MORPH_ERODE, np.ones((3,3)))
                maxLoG = cv2.morphologyEx(frame, cv2.MORPH_DILATE, np.ones((3,3)))
                zeroCross = np.logical_or(np.logical_and(minLoG < 0,  frame > 0), np.logical_and(maxLoG > 0, frame < 0))
                #convert the logical mask into 0 - 255 range.
                zeroCross = np.ones(zeroCross.shape) * zeroCross*255
                frame = zeroCross

            #Encode the image into a PNG
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            #Display the encoded image.
            window["-IMAGE-"].update(data=imgbytes)
        except:
            pass
    window.close()

main()