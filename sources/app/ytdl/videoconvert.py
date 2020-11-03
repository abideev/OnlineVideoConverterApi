import subprocess
import re
import redis

presets = {}
presets['same'] = {'s': 'same', 'b': {'high': '6000k', 'normal': '4000k', 'low': '2000k'}, 'ab': '128k'}
presets['1080p'] = {'s': '1920x1080', 'b': {'high': '8000k', 'normal': '6000k', 'low': '4000k'}, 'ab': '128k'}
presets['720p'] = {'s': '1280x720', 'b': {'high': '6000k', 'normal': '4000k', 'low': '2000k'}, 'ab': '128k'}
presets['480p'] = {'s': '854x480', 'b': {'high': '3000k', 'normal': '2000k', 'low': '1000k'}, 'ab': '128k'}
presets['360p'] = {'s': '640x360', 'b': {'high': '2000k', 'normal': '1000k', 'low': '500k'}, 'ab': '64k'}
presets['240p'] = {'s': '427x240', 'b': {'high': '1000k', 'normal': '500k', 'low': '300k'}, 'ab': '64k'}

formats = {}
formats['mp4'] = {'vcodec': 'libx264', 'acodec': 'aac', 'more_options': ''}
formats['avi'] = {'vcodec': 'libx264', 'acodec': 'aac', 'more_options': ''}
formats['mkv'] = {'vcodec': 'libx264', 'acodec': 'aac', 'more_options': ''}
formats['webm'] = {'vcodec': 'libvpx', 'acodec': 'libvorbis', 'more_options': ''}


def get_seconds(time):
    h = int(time[0:2])
    m = int(time[3:5])
    s = int(time[6:8])
    ms = int(time[9:12])
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts


"1.mkv", "8888.mkv", "mkv", "720p", "normal", "87546537"


def ffmpeg_transcode(srcfile, dstfile, format, frame, bitrate, id):
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
    r = redis.StrictRedis(host='192.168.8.12', port=6379, db=1)
    r.mset({id: str(strToJson)})
    r.expire(id, 43200)
    r.close()
