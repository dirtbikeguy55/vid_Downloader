import os
import tkinter as tk
import multiprocessing
import youtube_dl

#TODO: Make the URL be user input and add a text field for the input
# Add check boxes that allow the user to select audio or video
# Add a field for the user to select to download destination
# Show the command line output in a text box
# Make it so that the user input is actually taken into the URL string
# Make a button to choose the download destination
#
# Add an advanced section that lets the user add args to the youtube-dl command

URL = ""

ydl_opts = {}

var1 = int
var2 = int

#downloads the video that the user inputs
def download_vid():
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp4',
        'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])

#downloads the audio from the video that the user inputs
def download_audio():

    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])

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
        audiocb.config(state = "disabled")
        videocb.config(state = "disabled")
        root.after(200, lambda f=f: check_status(f))
    else:
    #changes the label to show when the function is not running
        label.config(text = "Not Downloading")
        d_button.config(state = "normal")
    return

if __name__ == "__main__":
    root = tk.Tk()
    #resizes the window
    root.geometry("400x200")
    #specifies the canvas for the application
    label2 = tk.Label(root, text = "Enter URL")
    label2.pack(side = 'top')
    #user input
    urlin = tk.Entry(root,width = 45)
    urlin.pack(side = 'top')
    audiocb = tk.Checkbutton(root,text = 'Audio', variable=var1)
    audiocb.pack(side = 'top')
    videocb = tk.Checkbutton(root,text = 'Video', variable=var2)
    videocb.pack(side = 'top')
    #creates a button that runs the function
    d_button = tk.Button(root, text = "Download Video", command = queue)
    d_button.pack(side = 'top')
    #creates a label for updating the user
    label = tk.Label(root, text = "Not Downloading")
    label.pack(side = 'top')
    root.mainloop()