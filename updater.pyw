import wget,os

def update():
    url = "https://github.com/dirtbikeguy55/vid_Downloader/raw/master/videoDownloader.pyw"
    os.remove('videoDownloader.pyw')
    filename = wget.download(url)
update()