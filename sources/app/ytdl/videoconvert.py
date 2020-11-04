import subprocess
import re
import redis
import os


presets={'same': {'s': 'same', 'b': {'high': '6000k', 'normal': '4000k', 'low': '2000k'}, 'ab': '128k'},
         '1080p': {'s': '1920x1080', 'b': {'high': '8000k', 'normal': '6000k', 'low': '4000k'}, 'ab': '128k'},
         '720p': {'s': '1280x720', 'b': {'high': '6000k', 'normal': '4000k', 'low': '2000k'}, 'ab': '128k'},
         '480p': {'s': '854x480', 'b': {'high': '3000k', 'normal': '2000k', 'low': '1000k'}, 'ab': '128k'},
         '360p': {'s': '640x360', 'b': {'high': '2000k', 'normal': '1000k', 'low': '500k'}, 'ab': '64k'},
         '240p': {'s': '427x240', 'b': {'high': '1000k', 'normal': '500k', 'low': '300k'}, 'ab': '64k'}
         }


formats={
    'mp4': {'vcodec': 'libx264', 'acodec': 'aac', 'more_options': ''},
    'avi': {'vcodec': 'libx264', 'acodec': 'aac', 'more_options': ''},
    'mkv': {'vcodec': 'libx264', 'acodec': 'aac', 'more_options': ''},
    'webm': {'vcodec': 'libvpx', 'acodec': 'libvorbis', 'more_options': ''}
}

def get_seconds(time):
    h = int(time[0:2])
    m = int(time[3:5])
    s = int(time[6:8])
    ms = int(time[9:12])
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts

#ffmpeg -y -hwaccel cuvid -c:v h264_cuvid -i input.mp4 -c:v h264_nvenc -vframes 2500 -threads 1 output.mkv
#ffmpeg -y -hwaccel cuvid -c:v h264_cuvid -resize 640x480 -i input.mp4 -c:v h264_nvenc -cq 21 -c:a copy output.mp4

def ffmpeg_transcode(srcfile, dstfile, format, frame, bitrate, id, gpu,transmux):
    try:
        if gpu == "false" and transmux == "false":
            ffmpegcmd = "ffmpeg -i " + srcfile + " "
            ffmpegcmd += "-vcodec " + formats[format]['vcodec'] + " "
            if frame != "same":
                ffmpegcmd += "-s " + presets[frame]['s'] + " "
            if bitrate in ("high", "normal", "low"):
                ffmpegcmd += "-b " + presets[frame]['b'][bitrate] + " "
            else:
                ffmpegcmd += "-b " + bitrate + " "
            ffmpegcmd += "-acodec " + formats[format]['acodec'] + " "
            ffmpegcmd += "-ab " + presets[frame]['ab'] + " "
            ffmpegcmd += "-ar 48000 -ac 2 "
            ffmpegcmd += formats[format]['more_options'] + " "
            ffmpegcmd += dstfile + " -y"
        elif gpu == "true" and transmux == "false":
            ffmpegcmd = "ffmpeg -y -hwaccel cuvid -c:v h264_cuvid "
            if frame != "same":
                ffmpegcmd += "-resize " + presets[frame]['s'] + " "
            ffmpegcmd += srcfile + " "
            ffmpegcmd += "-c:v h264_nvenc -cq 21  -c:a copy "
            ffmpegcmd += dstfile
        elif gpu == "false" and transmux == "true":
            ffmpegcmd = "ffmpeg -i " + srcfile + " "
            ffmpegcmd += "-c:v copy -ab 128k -b 1024 "
            ffmpegcmd += dstfile + " -y"
    except Exception:
        return sent_message(str("error ffmpeg"), id)

    cmd = ffmpegcmd.split()
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)

    while True:
        line = p.stderr.readline().rstrip('\r\n')

        if line != '':
            duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)

            result = re.search(r'time=(?P<time>\S+)', line)
            if result is not None and duration is not None:
                elapsed_time = result.groupdict()['time']

                currentTime = get_seconds(elapsed_time)
                allTime = get_seconds(duration)

                progress = round(currentTime / allTime * 100)
                sent_message(progress, id)
        else:
            break


def sent_message(progress, id):
    strToJson = ({"progress": + progress})
    r = redis.StrictRedis(host=os.getenv("redis_host"), port=6379, db=1)
    r.mset({id: str(strToJson)})
    r.expire(id, 43200)
    r.close()
