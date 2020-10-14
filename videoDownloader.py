import os
import tkinter as tk
import multiprocessing

#TODO: Make the URL be user input and add a text field for the input
# Add check boxes that allow the user to select audio or video
# Add a field for the user to select to download destination
# 
# Add an advanced section that lets the user add args to the youtube-dl command

URL = "https://www.youtube.com/watch?v=sJ0MaudqcsY"
args = ""
#url = input(str("Enter the URL: "))

#downloads the video that the user inputs
def download_vid():
    os.system('cmd /c youtube-dl '+ URL)

#downloads the audio from the video that the user inputs
def download_audio():
    os.system('cmd /c youtube-dl --extract-audio --audio-format mp3 ' + URL)

def advanced():
    os.system('cmd /c youtube-dl ' + args + ' ' + URL)

#adds multiprocessing to the command so tkinter dosent freeze while its running
def queue():
    f = multiprocessing.Process(target=download_vid)
    #starts the function that the user selects
    f.start()
    #checks to see if the function is running
    check_status(f)
    return

def check_status(f):
    #changes the label to show that the function is running
    if f.is_alive():
        label.config(text = "Downloading")
        d_button.config(state = "disabled")
        root.after(200, lambda f=f: check_status(f))
    else:
    #changes the label to show when the function is not running
        label.config(text = "Not Downloading")
        d_button.config(state = "normal")
    return

if __name__ == "__main__":
    root = tk.Tk()
    #specifies the canvas for the application
    canvas1 = tk.Canvas(root, width = 300, height = 200, bg = 'gray90', relief = 'raised')
    canvas1.pack()
    #creates a button that runs the function
    d_button = tk.Button(master = root, text = "Download Video", command = queue)
    d_button.pack()
    #creates a label for updating the user
    label = tk.Label(master = root, text = "Not Downloading")
    label.pack()
    root.mainloop()