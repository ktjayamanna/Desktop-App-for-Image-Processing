"""
Created on Sun Oct  3 09:28:20 2021
@author: kjayamanna
@Reference:https://realpython.com/pysimplegui-python/#integrating-opencv-with-pysimplegui
@Reference: Dr.Zhu's Slides'
"""

import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image
import os
import io
import custom_hist_final as hq
import matplot_lib_helper as mathelp
#%%
def main():    
    file_list_column = [
        
        [
            #define the folder browser.
            sg.Text("Image Folder"),
            sg.In(size=(100, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        
        [
            #Define the listbox that views the available image files.
            sg.Listbox(
                values=[], enable_events=True, size=(119, 5), key="-FILE LIST-"
            )
        ],
    ]
    #Define the GUI color
    sg.theme("DarkBrown")

    # Define the window layout
    layout = [
        #Define the Image Loading Panel.
        [sg.HorizontalSeparator()],
        [sg.Text("Image Loading Panel", size=(100, 1), justification="center", font=("Courier ", 15,('italic','bold')))],
        [sg.HorizontalSeparator()],
            [
        sg.Column(file_list_column),
    ],
        #Define the Image Display Panel.
        [sg.HorizontalSeparator()],
        [sg.Text("Image Display Panel", size=(100, 1), justification="center", font=("Courier ", 15,('italic','bold')))],
        [sg.HorizontalSeparator()],
        #Define a placeholder for the original Image.
        [sg.Text("Original Image" ,size=(25, 1)),sg.VSeperator(), sg.Image(filename="", key="-IMAGE-")],
        [sg.Text("Histogram Equalized Image" ,size=(25, 1)),sg.VSeperator(),sg.Image(filename="", key="-IMAGE2-")],
        [sg.HorizontalSeparator()],
        #Define Equalizer Panel
        [sg.Text("Equalizer Panel", size=(100, 1), justification="center", font=("Courier ", 15,('italic','bold')))],
        [sg.HorizontalSeparator()],
        [sg.Radio("None", "Radio", True, size=(10, 1))],

        [
            #Define a radio for user inputs.
            sg.Radio("Histogram \n Equalization", "Radio", size=(10, 1), key="-Histeq-"),
            #Get histogram input value a.
            sg.Slider(
                (0, 255),
                default_value = 0,
                resolution = 1,
                tick_interval= None,
                orientation="v",
                size=(5, 15),
                key="-Histeqa-",
            ),
            #Get histogram input value b.
            sg.Text('\n\n\n\n\n\n\n\nValue a'),
            sg.Slider(
                (0, 255),
                default_value = 0,
                resolution = 1,
                tick_interval= None,
                orientation="v",
                size=(5, 15),
                key="-Histeqb-",
            ),
            #Get histogram output value c.
            sg.Text('\n\n\n\n\n\n\n\nValue b'),
            sg.Slider(
                (0, 255),
                default_value = 0,
                resolution = 1,
                tick_interval= None,
                orientation="v",
                size=(5, 15),
                key="-Histeqc-",
            ),
            #Get histogram output value d.
            sg.Text('\n\n\n\n\n\n\n\nValue c'),
            sg.Slider(
                (0, 255),
                default_value = 0,
                resolution = 1,
                tick_interval= None,
                orientation="v",
                size=(5, 15),
                key="-Histeqd-",
            ),
            sg.Text('\n\n\n\n\n\n\n\nValue d')  
        ],
        #Define the Action Panel.
        [sg.HorizontalSeparator()],
        [sg.Text("Action Panel", size=(100, 1), justification="center",font=("Courier ", 15,('italic','bold')))],
        [sg.HorizontalSeparator()],
        #Define Action Buttons.
        [sg.Button("Enter", size=(10, 1))],
        [sg.Button("Exit", size=(10, 1))],
        
    ]
    # Create the window and show it without the plot
    window = sg.Window("CSCI 8300 Project Deliverable A Part II", layout, location=(400, 400))
    #Define the polling loop that checks user inputs every 20 sec.
    while True:
        event, values = window.read(timeout=20)
        #Close the window if the user hit exit or hit the close button.
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
            #Use list comprehension to list the file names.
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".gif", "jpg"))
            ]
            #Update the filename list on the file list.
            window["-FILE LIST-"].update(fnames)
            #Create paths for the files detected.
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            #Open the image.
            myImage = Image.open(filename).convert('L')
            #Resize the Image
            myImage.thumbnail((2000, 150))
            #Save as a PNG Image.
            bio = io.BytesIO()
            myImage.save(bio, format="PNG")
            #Update the display.
            window["-IMAGE-"].update(data=bio.getvalue())
            #Make a copy of the PNG Image.
            frame = np.copy(myImage)
            #Initialize the user inputs with zero if the user... 
            #...has not selected histeq on the radio.
            if values["-Histeq-"] == False:
                a_previous = 0
                b_previous = 0
                c_previous = 0
                d_previous = 0
            # If the user has updated a,b,c,d and the hit enter,
            if values["-Histeq-"] and event == "Enter":
                #Load the input values to the variables.
                a = int(values['-Histeqa-'])
                b = int(values['-Histeqb-'])
                c = int(values['-Histeqc-'])
                d = int(values['-Histeqd-'])
                #If the user inputs have been updated,
                if (
                        a != a_previous or 
                        b != b_previous or 
                        c != c_previous or 
                        d != d_previous
                        ):
                    #find the histogram of the input images.
                    hist = hq.histogram(frame)
                    #find the qp of the image.
                    qp = hq.customEq(frame, hist, a, b, c, d)
                    #Plot the histograms and get the equalized image.
                    frame_eq, fig = hq.plot_hist(frame, qp)
                    #Update the previous value trackers.
                    a_previous = a
                    b_previous = b
                    c_previous = c
                    d_previous = d
                    #Update the display.
                    imgbytes2 = cv2.imencode(".png", frame_eq)[1].tobytes()
                    window["-IMAGE2-"].update(data=imgbytes2)
                    #Define a layout for a new window to display plots.
                    layout2 = [
                    [sg.Text("Histogram Plots")],
                    #Place holder for Matplotlib Plot
                    [sg.Canvas(key="-CANVAS2-")],
                    #Define a button to kill the window.
                    [sg.Button("Ok",size=(10, 1))],
                    ]
                    #Define a seperate window to display histograms.
                    window2 = sg.Window(
                    "Hist_window",
                    layout2,
                    location=(0, 0),
                    finalize=True,
                    element_justification="center",
                    font="Helvetica 18",
                    size = (2000,800)
                    )
                    #Create a matplotlib figure and display it.
                    mathelp.draw_figure(window2["-CANVAS2-"].TKCanvas, fig)
                    event2, values2 = window2.read()
                    window2.close()
        except:
            pass 
    window.close()
main()

