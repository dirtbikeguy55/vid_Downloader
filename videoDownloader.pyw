import os
import tkinter as tk
from tkinter import filedialog
import multiprocessing
import youtube_dl
import ffmpeg

#TODO: 
# Add the option to download playlists while also selecting certain ranges in the playlist
# Add check boxes for youtube and then other sites so that i can have things specific to youtube
# Add a progress bar for the download progress
# Change the enter button below the url input to be combined with the download button

#BUGS:
#The videos are still being downloaded to the current directory that the file is in

ydl_opts = {}

opts = [('Audio', '0'),
        ('Video', '1')]

wd = os.getcwd()

def getTxt():
    global URL
    global val
    val = var1.get()
    URL = urlin.get()
    return URL,val

#downloads the video that the user inputs
def download_vid(URL,val):
    print(val)
    if val == 1:
        #Download video and audio
        ydl_opts = {
        'format': 'bestvideo[ext=mkv]+bestaudio[ext=webm]/bestvideo+bestaudio',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            }]
        }
    #Downloads only the audio from the video
    if val == 0:
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
    f = multiprocessing.Process(target=download_vid,args=(URL,val,))
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
    os.chdir(folder_path)
    wd = os.getcwd()
    print(folder_path)
    print(wd)


if __name__ == "__main__":
    root = tk.Tk()

    root.title("Video Downloader")
    var1 = tk.IntVar()
    url = tk.StringVar(root)
    var1.set('0')
    #resizes the window
    root.geometry("400x200")
    root.configure(background = "gray")
    #specifies the canvas for the application
    label2 = tk.Label(root, text = "Enter URL", background = "gray")
    label2.pack(side = 'top')
    #user input
    urlin = tk.Entry(root,width = 45, background = "dark gray")
    urlin.pack(side = 'top')

    enter_url = tk.Button(root, text = "Enter",command = getTxt, background = "dark gray")
    enter_url.pack()

    for text,opt in opts:
        rb = tk.Radiobutton(root,text = text, variable = var1, value = opt, background = "gray", activebackground = "gray")
        rb.pack()

    des_button = tk.Button(root, text = "Destination", command = browse_button, background = "dark gray")
    des_button.pack(side = 'top')
    #creates a button that runs the function
    d_button = tk.Button(root, text = "Download Video", command = queue, background = "dark gray")
    d_button.pack(side = 'top')

    #creates a label for updating the user
    label = tk.Label(root, text = "Not Downloading", background = "gray")
    label.pack(side = 'top')
    root.mainloop()