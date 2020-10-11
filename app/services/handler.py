import json
import pika
import time
from app.ytdl.videocheckformat import youtube_parser

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672, credentials=pika.credentials.PlainCredentials('rabbitmq', 'rabbitmq'),))
channel = connection.channel()
channel.queue_declare(queue='online_converter_queue', durable=True)

print('-----Wait-----')


def rabbit_mq_sent(videoinfo, queue_info):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672,
                                                                   credentials=pika.credentials.PlainCredentials(
                                                                       'rabbitmq', 'rabbitmq'), ))
    channel = connection.channel()
    channel.queue_declare(queue=queue_info, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_info,
        body=json.dumps(videoinfo),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()


def return_video_info(url):
    queue_info = "video_info_queue"
    videoinfo = youtube_parser(url)
    rabbit_mq_sent(videoinfo, queue_info)


def callback(ch, method, properties, body):
    data = json.loads(body)
    return_video_info(data['url'])

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='online_converter_queue', on_message_callback=callback)
channel.start_consuming()
