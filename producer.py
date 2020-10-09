from flask import Flask
from flask import request
import json
import pika

app = Flask(__name__)

@app.route('/')
def index():
    return 'not supported'


@app.route("/api/v1/onlineconverter",  methods = ['POST'])
def OnlineVideoConverter():
    message = request.get_json()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672, credentials=pika.credentials.PlainCredentials('rabbitmq', 'rabbitmq'),))
    channel = connection.channel()
    channel.queue_declare(queue='online_converter_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='online_converter_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()
    return " Success"

#    print(request.get_json())
#    return request.get_json(), 200, {'ContentType':'application/json'} 


@app.route("/api/v1/offlineconverter",  methods = ['POST'])
def OfflineVideoConverter():
    message = request.get_json()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672, credentials=pika.credentials.PlainCredentials('rabbitmq', 'rabbitmq'),))
    channel = connection.channel()
    channel.queue_declare(queue='offline_converter_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='offline_converter_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()
    return " Success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)


