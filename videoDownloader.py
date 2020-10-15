import os
import tkinter as tk
from tkinter import filedialog
import multiprocessing
import youtube_dl
import ffmpeg

#TODO: 
# Make the URL be user input and add a text field for the input
# Add check boxes that allow the user to select audio or video
# Add a field for the user to select to download destination
# Show the command line output in a text box
# Make it so that the user input is actually taken into the URL string
# Add the option to download playlists while also selecting certain ranges in the playlist
#
# Add an advanced section that lets the user add args to the youtube-dl command

URL = ''
ydl_opts = {}

opts = [('Audio', '0'),
        ('Video', '1')]

wd = os.getcwd()



#downloads the video that the user inputs
def download_vid():
    getTxt()
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
        rb.config(state = "disabled")
        des_button.config(state = "disabled")
        root.after(200, lambda f=f: check_status(f))
    else:
    #changes the label to show when the function is not running
        label.config(text = "Not Downloading")
        d_button.config(state = "normal")
        rb.config(state = "normal")
        des_button.config(state = "normal")
    return

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path = filename
    os.chdir(filename)
    wd = os.getcwd()
    print(filename)
    print(wd)

#Left off here trying to fix the url get fnc so that it grabs the user input and saves it to the URL variable
def getTxt():
    URL = urlin.get()
    print(URL)
    return URL

if __name__ == "__main__":
    root = tk.Tk()

    root.title("Video Downloader")
    var1 = tk.StringVar()
    url = tk.StringVar()
    var1.set('0')
    #resizes the window
    root.geometry("400x200")
    #specifies the canvas for the application
    label2 = tk.Label(root, text = "Enter URL")
    label2.pack(side = 'top')
    #user input
    urlin = tk.Entry(root,textvariable = url,width = 45)
    urlin.pack(side = 'top')

    for text,opt in opts:
        rb = tk.Radiobutton(root,text=text, variable = var1, value = opt)
        rb.pack()

    des_button = tk.Button(root, text = "Destination", command = browse_button)
    des_button.pack(side = 'top')
    #creates a button that runs the function
    d_button = tk.Button(root, text = "Download Video", command = queue)
    d_button.pack(side = 'top')

    folder_path = ''
    lbl1 = tk.Label(master=root,textvariable=folder_path)
    lbl1.pack()

    #creates a label for updating the user
    label = tk.Label(root, text = "Not Downloading")
    label.pack(side = 'top')
    root.mainloop()