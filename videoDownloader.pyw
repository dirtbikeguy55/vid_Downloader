import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Label
import multiprocessing
import youtube_dl
import time

#TODO: 
# Save the files already downloaded to a file so that they dont get downloaded twice
# This works while using --download-archive, but I cant get it to work without using the command line.
#
# Fix the downloading/not downloading label so that it still says that it is downloading while the temp files are being converted/deleted

#BUGS:

ydl_opts = {}

opts = [('Audio', '0'),
        ('Video', '1')]

wd = os.getcwd()
svlwd = os.getcwd()

def getTxt():
    global URL
    global val

    val = var1.get()
    URL = urlin.get()
    return URL,val

#Not currently used
def svLink():
    wd = os.getcwd()
    os.chdir(svlwd)
    svl = urlin.get()
    
    #eventually add option that compares user input text with links in file
    with open('links.txt', 'a') as f:
        f.write(svl+"\n")
        f.close()
    
    os.chdir(wd)

#downloads the video that the user inputs
def download_vid(URL,val):
        
    if val == 0:
        #Downloads only the audio from the video
        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':  '%(title)s.%(ext)s',
        'forcethumbnail': True,
        'noplaylist' : True,
        '--download-archive' : 'Archive.txt',
        'progress_hooks': [my_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
            }]
        }

    if val == 1:
        #Download video with audio
        ydl_opts = {
        'format': 'bestvideo[ext=mkv]+bestaudio[ext=webm]/bestvideo+bestaudio',
        'outtmpl':  '%(title)s.%(ext)s',
        'forcethumbnail': True,
        'noplaylist' : True,
        'progress_hooks': [my_hook],
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            }]
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])

def download_playlist(URL,val):
    if val == 1:
        #Download video with audio
        ydl_opts = {
        'format': 'bestvideo[ext=mkv]+bestaudio[ext=webm]/bestvideo+bestaudio',
        'outtmpl':  '%(title)s.%(ext)s',
        'forcethumbnail': True,
        'noplaylist' : False,
        'progress_hooks': [my_hook],
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            }]
        }
    
    #Downloads only the audio from the video
    if val == 0:
        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':  '%(title)s.%(ext)s',
        'forcethumbnail': True,
        'noplaylist' : False,
        'progress_hooks': [my_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
            }]
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
    

#adds multiprocessing to the command so the program dosent freeze while its running
def queue():
    global playli
    playli = pl.get()
    getTxt()
    svLink()
    if playli == 0:
        f = multiprocessing.Process(target=download_vid,args=(URL,val,))
    if playli == 1:
        f = multiprocessing.Process(target=download_playlist,args=(URL,val,))
    #starts the function that the user selects
    f.start()
    #checks to see if the function is running
    check_status(f)
    return

def check_status(f):
    #changes the label to show that the function is running
    if f.is_alive():
        label.config(text = "Downloading")
        urlin.config(state = "disabled")
        d_button.config(state = "disabled")
        rb.config(state = "disabled")
        des_button.config(state = "disabled")
        root.after(200, lambda f=f: check_status(f))
    else:
    #changes the label to show when the function is not running
        label.config(text = "Not Downloading")
        urlin.config(state = "normal")
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
    downloc.config(text = wd)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
#Supposed to change the value of the download label when the video is converting, dosent currently work
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
        #label.config(text = "Converting Video...")
    return

if __name__ == "__main__":
    root = tk.Tk()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title("Video Downloader")
    var1 = tk.IntVar()
    pl = tk.IntVar()
    plint = tk.IntVar()
    url = tk.StringVar(root)
    pic = tk.PhotoImage(file = 'icon.png')
    root.iconphoto(False,pic)
    var1.set('0')

    #resizes the window
    root.geometry("400x225")
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

    play = tk.Checkbutton(root,text = "Playlist",variable = pl,background="gray",activebackground="gray")
    play.grid(row=2,column=2)

    des_button = tk.Button(root, text = "Destination", command = browse_button, background = "dark gray")
    des_button.grid(row=5,column=2)

    #Label that shows the download location
    downloc = tk.Label(root, text = "Download Location...", background = "dark gray")
    downloc.grid(row=6,column=2)
    #creates a button that runs the function
    d_button = tk.Button(root, text = "Download Video", command = queue, background = "dark gray")
    d_button.grid(row=7,column=2)

    #creates a label for updating the user
    label = tk.Label(root, text = "Not Downloading", background = "gray")
    label.grid(row=8,column=2)

    root.mainloop()