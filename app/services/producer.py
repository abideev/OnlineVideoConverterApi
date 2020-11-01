from flask import Flask, jsonify
from flask import request
from flask import abort
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, flash, request, redirect, url_for
import json
import pika
from werkzeug.utils import secure_filename
import os


abs_path_to_producer = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = 'D:\\'
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

# Config application
app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
API_URL = "/static/swagger.json"
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Online video converter"
    },
)
# Register blueprint at URL
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return jsonify(message="not supported"), 404


@app.route("/api/v1/url-converter",  methods=['POST'])
def url_converter():
    message = request.get_json()
    if message is None:
        abort(400)
    if "url" not in message:
        return json.dumps({'success': False,
                           'message': "url not found"}), 400, {'ContentType': 'application/json',}
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12',
                                                                   port=5672,
                                                                   credentials=pika.credentials.PlainCredentials('rabbitmq', 'rabbitmq'),))
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
    return json.dumps({'success': True,
                       'id': None}), 200, {'ContentType': 'application/json'}


@app.route("/api/v1/file-converter",  methods=['GET', 'POST'])
def file_converter():
    message = request.get_json()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12',
                                                                   port=5672,
                                                                   credentials=pika.credentials.PlainCredentials('rabbitmq', 'rabbitmq'),))
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
    return 'success'


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, threaded=True)
    # app.run(host="0.0.0.0", port=8080, threaded=True)
    # app.run(debug=True)
