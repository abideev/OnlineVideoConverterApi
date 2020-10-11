from flask import Flask
from flask import request
from flask import abort
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, flash, request, redirect, url_for
import json
import pika
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'D:\\'
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

# Config application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
API_URL = "/swagger.json"  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Online video converter"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

# Register blueprint at URL
# (URL must match the one given to factory function above)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

'''
Next the functions that check if an extension is valid and 
that uploads the file and redirects the user to the URL for the uploaded file
'''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'not supported'


@app.route("/api/v1/url-converter",  methods=['POST'])
def url_converter():
    message = request.get_json()
    if message is None:
        abort(400)
    if "url" not in message:
        return json.dumps({'success': False,
                           'message': "url not found"}), 400, {'ContentType': 'application/json',}
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
    return json.dumps({'success': True,
                       'id': None}), 200, {'ContentType': 'application/json'}


@app.route("/api/v1/file-converter",  methods=['GET', 'POST'])
def file_converter():
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
    return 'success'


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, threaded=True)
    # app.run(debug=True)
