import uuid
import redis
from flask import Flask, jsonify, send_from_directory
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
app.config["CLIENT_VIDEO"] = '/download/'

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


@app.route("/api/v1/url-converter", methods=['POST'])
def url_converter():
    id = uuid.uuid4().hex
    message = request.get_json()
    tmpid = {"id": id}
    message.update(tmpid)

    if message is None:
        return json.dumps({'success': False,
                           'message': "url not found"}), 400, {'ContentType': 'application/json', }
    if "url" not in message:
        return json.dumps({'success': False,
                           'message': "url not found"}), 400, {'ContentType': 'application/json', }
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.12', port=5672,
                                                                   credentials=pika.credentials.PlainCredentials(
                                                                       'rabbitmq', 'rabbitmq'), ))
    channel = connection.channel()
    channel.queue_declare(queue='converter_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='converter_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
            message_id=id
        ))
    connection.close()
    return json.dumps({'success': True,
                       'id': id}), 200, {'ContentType': 'application/json'}


@app.route("/api/v1/file-converter", methods=['GET', 'POST'])
def file_converter():
    return json.dumps({'success': True,
                       'message': "Success"}), 202, {'ContentType': 'application/json'}


@app.route('/api/v1/<status_id>', methods=['GET', 'POST'])
def status(status_id):
    try:
        r = redis.StrictRedis(host='192.168.8.12', port=6379, db=1)
        status = r.get(status_id)
        r.close()
        if status is None:
            return json.dumps({'success': False,
                               'message': "Task not found"}), 404, {'ContentType': 'application/json'}
        else:
            r.delete(status_id)
            return status
    except Exception:
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


@app.route('/download/<file_name>', methods=['GET'])
def get_image(file_name):
    try:
        response = send_from_directory(app.config["CLIENT_VIDEO"], filename=file_name, conditional=False)
        response.headers["x-suggested-filename"] = file_name
        return response
    except FileNotFoundError:
        return json.dumps({'success': False,
                           'message': "File not found"}), 404, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, threaded=True)
    # app.run(host="0.0.0.0", port=8080, threaded=True)
    # app.run(debug=True)
