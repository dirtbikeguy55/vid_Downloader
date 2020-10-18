import os
import tkinter as tk
from tkinter import filedialog
import multiprocessing
import youtube_dl
import time

#TODO: 
# Add the option to download playlists while also selecting certain ranges in the playlist
# Add check boxes for youtube and then other sites so that i can have things specific to youtube
# Switch from grid to pack

#BUGS:
# When the window closes, end the youtube-dl download

#Changes:
# Changed app icon
# Added playlist checkbox
# Fixed some bugs

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
    getTxt()
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

if __name__ == "__main__":
    root = tk.Tk()

    root.title("Video Downloader")
    var1 = tk.IntVar()
    pl = tk.IntVar()
    plint = tk.IntVar()
    url = tk.StringVar(root)
    pic = tk.PhotoImage(file = 'icon.png')
    root.iconphoto(False,pic)
    var1.set('0')
    #resizes the window
    root.geometry("400x200")
    root.configure(background = "gray")
    #specifies the canvas for the application
    label2 = tk.Label(root, text = "Enter URL", background = "gray",)
    label2.grid(row=0,column=2)
    #user input
    urlin = tk.Entry(root,width = 45, background = "dark gray",justify='center')
    urlin.grid(row=1,column=2)

    r = 3
    c = 2
    for text,opt in opts:
        rb = tk.Radiobutton(root,text = text, variable = var1, value = opt, background = "gray", activebackground = "gray")
        rb.grid(row=r,column=c)
        r+=1

    play = tk.Checkbutton(root,text = "Playlist", variable = pl,background="gray",activebackground="gray")
    play.grid(row=3,column=3)

    playint = tk.Entry(root,background="dark gray")
    playint.grid(row=4,column=3)

    des_button = tk.Button(root, text = "Destination", command = browse_button, background = "dark gray")
    des_button.grid(row=5,column=2)
    #creates a button that runs the function
    d_button = tk.Button(root, text = "Download Video", command = queue, background = "dark gray")
    d_button.grid(row=6,column=2)

    #creates a label for updating the user
    label = tk.Label(root, text = "Not Downloading", background = "gray")
    label.grid(row=7,column=2)

    root.mainloop()