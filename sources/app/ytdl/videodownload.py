import youtube_dl
import os
from sources.app.services.uploader import uploader_file


def youtube_download(url):
    ydl_opts = {'outtmpl': rf'C:\Users\ph03n1x\Documents\Downloads\%(id)s.%(ext)s', }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            url, download=True)
        filename = ydl.prepare_filename(meta)
    if os.path.exists(filename):
        extfilename = (meta['id'] + "." + meta['ext'])
        return uploader_file(extfilename)
    elif os.path.exists(os.path.splitext(filename)[0] + '.mkv'):
        extfilename = (meta['id'] + '.mkv')
        return uploader_file(extfilename)
    else:
        print("Error: file doesn't exist")
