import json
import pika
import time


connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672, credentials=pika.credentials.PlainCredentials('rabbitmq', 'rabbitmq'),))
channel = connection.channel()
channel.queue_declare(queue='online_converter_queue', durable=True)

print('-----Wait-----')

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("url: {}".format(data['url']))
    print("email: {}".format(data['email']))
    print('Isfile: {}'.format(data['IsFile']))
    print('format: {}'.format(data['format']))
    print('quality: {}'.format(data['quality']))


    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='online_converter_queue', on_message_callback=callback)
channel.start_consuming()

