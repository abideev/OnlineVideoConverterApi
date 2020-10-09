from __future__ import unicode_literals
import youtube_dl

def status(d):
    if d['status'] == 'finished':
        print('Dwonload compleate, convert')

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',        
    'outtmpl': '%(id)s',        
    'noplaylist' : True,        
    'progress_hooks': [status],  
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=NbIQSXlCMT0&ab_channel=NTDRussian'])

