""" index file for REST APIs using Flask """
from app import app
import logger
import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory
import threading
import rabbit


def start():
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    os.environ.update({'ROOT_PATH': ROOT_PATH})
    sys.path.append(os.path.join(ROOT_PATH, 'modules'))

    # Create a logger object to log the info and debug
    LOG = logger.get_root_logger(os.environ.get(
        'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

    # Port variable to run the server on.
    PORT = os.environ.get('PORT') or 4000

    @app.errorhandler(404)
    def not_found(error):
        """ error handler """
        LOG.error(error)
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.route('/')
    def index():
        """ static files serve """
        return send_from_directory('dist', 'index.html')

    @app.route('/<path:path>')
    def static_proxy(path):
        """ static folder serve """
        file_name = path.split('/')[-1]
        dir_name = os.path.join('dist', '/'.join(path.split('/')[:-1]))
        return send_from_directory(dir_name, file_name)

    if __name__ == '__main__':
        LOG.info('running environment: %s', os.environ.get('ENV'))
        app.run(host='0.0.0.0', port=int(PORT))  # Run the app


threading.Thread(target=start).start()
threading.Thread(target=rabbit.start).start()

print("Total number of threads", threading.activeCount())
print("List of threads: ", threading.enumerate())
