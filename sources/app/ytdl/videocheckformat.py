import youtube_dl
import json


def youtube_parser(url):
    video_format={
        # youtube video
        '394': {'resolution': '256x144', 'format': '144p', 'extension': 'mp4', 'fps': '30'},
        '395': {'resolution': '426x240', 'format': '240p', 'extension': 'mp4', 'fps': '30'},
        '396': {'resolution': '640x360', 'format': '360p', 'extension': 'mp4', 'fps': '30'},
        '397': {'resolution': '854x480', 'format': '480p', 'extension': 'mp4', 'fps': '30'},
        '398': {'resolution': '1280x720', 'format': '720p', 'extension': 'mp4', 'fps': '30'},
        '136': {'resolution': '1280x720', 'format': '720p', 'extension': 'mp4', 'fps': '30'},
        '137': {'resolution': '1920x1080', 'format': '1080p', 'extension': 'mp4', 'fps': '30'},
        '400': {'resolution': '2560x1440', 'format': '1440p', 'extension': 'mp4', 'fps': '60'},
        '401': {'resolution': '3840x2160', 'format': '2160p', 'extension': 'mp4', 'fps': '60'},
        '278': {'resolution': '256x144', 'format': '144p', 'extension': 'webm', 'fps': '30'},
        '160': {'resolution': '256x144', 'format': '144p', 'extension': 'mp4', 'fps': '30'},
        '242': {'resolution': '426x240', 'format': '240p', 'extension': 'webm', 'fps': '30'},
        '133': {'resolution': '426x240', 'format': '240p', 'extension': 'mp4', 'fps': '30'},
        '134': {'resolution': '640x360', 'format': '360p', 'extension': 'mp4', 'fps': '30'},
        '243': {'resolution': '640x360', 'format': '360p', 'extension': 'webm', 'fps': '30'},
        '244': {'resolution': '854x480', 'format': '480p', 'extension': 'webm', 'fps': '30'},
        '135': {'resolution': '854x480', 'format': '480p', 'extension': 'mp4', 'fps': '30'},
        '247': {'resolution': '1280x720', 'format': '720p', 'extension': 'webm', 'fps': '30'},
        '18': {'resolution': '640x360', 'format': '360p', 'extension': 'mp4', 'fps': '30'},
        '22': {'resolution': '1280x720', 'format': '720p', 'extension': 'mp4', 'fps': '30'},
        ##youtube music TODO
        #####
        ###pornohub
        '240p': {'resolution': '426x240', 'format': '240p', 'extension': 'mp4', 'fps': '30'},
        '480p': {'resolution': '854x480', 'format': '480p', 'extension': 'mp4', 'fps': '30'},
        '720p': {'resolution': '1280x720', 'format': '720p', 'extension': 'mp4', 'fps': '30'},
        '1080p': {'resolution': '1920x1080', 'format': '1080p', 'extension': 'mp4', 'fps': '30'},
        ###xhamster
        'mp4-144p': {'resolution': '256x144', 'format': '144p', 'extension': 'mp4', 'fps': '30'},
        'mp4-240p': {'resolution': '426x240', 'format': '240p', 'extension': 'mp4', 'fps': '30'},
        'mp4-480p': {'resolution': '854x480', 'format': '480p', 'extension': 'mp4', 'fps': '30'},
        'mp4-720p': {'resolution': '1280x720', 'format': '720p', 'extension': 'mp4', 'fps': '30'},
        'mp4-1080p': {'resolution': '1920x1080', 'format': '1080p', 'extension': 'mp4', 'fps': '30'},
        ##facebook TODO
        '1994421467348134v': {'resolution': '256x144', 'format': '144p', 'extension': 'mp4', 'fps': '30'},
        '641315383188552v': {'resolution': '426x240', 'format': '240p', 'extension': 'mp4', 'fps': '30'},
        '1192007917865798v': {'resolution': '640x362', 'format': '360p', 'extension': 'mp4', 'fps': '30'},
        '204109750952096v': {'resolution': '854x480', 'format': '480p', 'extension': 'mp4', 'fps': '30'}
    }
    formats_array=[]
    ydl_opts={}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta=ydl.extract_info(
                url, download=False)
            formats=meta.get('formats', [meta])
            thumbnails=meta.get('thumbnails', [meta])
        for format in formats:
            for video_tag, data in video_format.items():
                if video_tag == format['format_id']:  # and data["extension"] == "mp4":
                    if data not in formats_array:
                        formats_array.append(data)
        formats_array.append(thumbnails[-1])
        return formats_array
    except Exception:
        return json.dumps({'success': False,
                           'message': "Not support"}), 404, {'ContentType': 'application/json'}
