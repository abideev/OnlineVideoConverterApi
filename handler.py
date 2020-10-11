import json
import pika
import time
from videocheckformat import YoutubeParce


connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672, credentials=pika.credentials.PlainCredentials('rabbitmq', 'rabbitmq'),))
channel = connection.channel()
channel.queue_declare(queue='online_converter_queue', durable=True)

print('-----Wait-----')

def RabbitMQSent(videoinfo,queue_info):
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672, credentials=pika.credentials.PlainCredentials('rabbitmq', 'rabbitmq'),))
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


def ReturnVideoInfo(url):
  queue_info = "video_info_queue"
  videoinfo = YoutubeParce(url)
  RabbitMQSent(videoinfo, queue_info)



def callback(ch, method, properties, body):
  data = json.loads(body)
  ReturnVideoInfo(data['url'])
 
  ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='online_converter_queue', on_message_callback=callback)
channel.start_consuming()

