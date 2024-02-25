#!/usr/bin/python3
""" Initialize the blueprint app_views """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.route('/api/v1/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(self):
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
