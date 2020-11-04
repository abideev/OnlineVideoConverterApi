import youtube_dl
import os
import json
from sources.app.services.uploader import uploader_file


def youtube_download(url):
    abs_path_ytdl = os.path.dirname(os.path.abspath(__file__))
    path_download = os.path.join(abs_path_ytdl, "..", "data")
    ydl_opts = {'outtmpl': rf'{path_download}/%(id)s.%(ext)s', }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              meta = ydl.extract_info(
                  url, download=True)
              filename = ydl.prepare_filename(meta)
              title = (meta["title"])
        if os.path.exists(filename):
            extfilename = (meta['id'] + "." + meta['ext'])
            return uploader_file(extfilename,title)
        elif os.path.exists(os.path.splitext(filename)[0] + '.mkv'):
            extfilename = (meta['id'] + '.mkv')
            return uploader_file(extfilename,title)
        else:
            print("Error: file doesn't exist")
    except Exception:
        return json.dumps({'success': False,
                           'message': "Not support"}), 404, {'ContentType': 'application/json'}
