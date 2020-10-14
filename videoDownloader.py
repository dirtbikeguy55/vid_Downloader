import os
import tkinter as tk
import multiprocessing

URL = "https://www.youtube.com/watch?v=sJ0MaudqcsY"
#url = input(str("Enter the URL: "))


def download_vid():
    os.system('cmd /c youtube-dl '+ URL)

def download_audio():
    os.system('cmd /c youtube-dl --extract-audio --audio-format mp3 ' + URL)

def queue():
    f = multiprocessing.Process(target=download_vid)
    f.start()
    check_status(f)
    return

def check_status(f):
    if f.is_alive():
        label.config(text = "Downloading")
        d_button.config(state = "disabled")
        root.after(200, lambda f=f: check_status(f))
    else:
        label.config(text = "Not Downloading")
        d_button.config(state = "normal")
    return

if __name__ == "__main__":
    root = tk.Tk()
    canvas1 = tk.Canvas(root, width = 300, height = 200, bg = 'gray90', relief = 'raised')
    canvas1.pack()
    d_button = tk.Button(master = root, text = "Download Video", command = queue)
    d_button.pack()
    label = tk.Label(master = root, text = "Not Downloading")
    label.pack()
    root.mainloop()