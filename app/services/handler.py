import json
import pika
import os
import time
import redis
from app.ytdl.videoconvert import ffmpeg_transcode
from app.services.sender import sender_email
from app.ytdl.videocheckformat import youtube_parser
from app.ytdl.videodownload import youtube_download

connection=pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672,
                                                             credentials=pika.credentials.PlainCredentials('rabbitmq',
                                                                                                           'rabbitmq'), ))
channel=connection.channel()

print('-----Wait-----')


def redis_sent(status, id):
    r=redis.StrictRedis(host='192.168.8.12', port=6379, db=1)
    r.mset({id: str(status)})
    r.expire(id, 86400)
    r.close()


def return_video_info(url, id):
    videoinfo=youtube_parser(url)
    redis_sent(videoinfo, id)


def return_video_file(url, id):
    video_download_file=youtube_download(url)
    strToJson=({"URL": "http://127.0.0.1:8080/download/" + video_download_file})
    redis_sent(strToJson, id)


def return_video_convert(email, url, id, dstformat, size, bitrate):
    video_download_file=youtube_download(url)
    video_convert_file=ffmpeg_transcode(
        rf'C:\Users\ph03n1x\Documents\123\{video_download_file}',
        rf'C:\Users\ph03n1x\Documents\123\{id}.{dstformat}',
        dstformat,
        size,
        bitrate,
        id)
    time.sleep(1)
    os.remove(rf'C:\Users\ph03n1x\Documents\123\{video_download_file}')
    strToJson=({"URL": "http://127.0.0.1:8080/download/" + id + "." + dstformat})
    if email != "None":
        sender_email(email, str("http://127.0.0.1:8080/download/" + id + "." + dstformat))
    redis_sent(strToJson, id)


def callback_converter(ch, method, properties, body):
    data_dict=json.loads(body)
    if data_dict['convert'] == "false" and data_dict['download'] == "false":
        return_video_info(data_dict['url'], properties.message_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif data_dict['convert'] == "false" and data_dict['download'] == "true":
        return_video_file(data_dict['url'], properties.message_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif data_dict['convert'] == "true" and data_dict['email'] == "":
        return_video_convert("None", data_dict['url'],  properties.message_id, data_dict['format'], data_dict['size'], data_dict['bitrate'])
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif data_dict['convert'] == "true" and data_dict['email'] != "":
        return_video_convert(data_dict['email'], data_dict['url'],  properties.message_id, data_dict['format'], data_dict['size'], data_dict['bitrate'])
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='converter_queue', on_message_callback=callback_converter)
channel.start_consuming()
