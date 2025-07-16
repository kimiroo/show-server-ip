import os
from flask import Flask, render_template, jsonify, send_from_directory
from utils.query_public_ip import QueryPublicIp

app = Flask(__name__)

# Default cache timeout for static files (in seconds).
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/v1/server-ip', methods=['GET'])
def get_server_ip():
    """
    Returns the public IPv4 and/or IPv6 address of the server.
    """
    ip_querier = QueryPublicIp()
    ip_info = ip_querier.query_public_ip()
    return jsonify(ip_info)

@app.route('/api/v1/health', methods=['GET'])
def health():
    return 'alive'

@app.route('/favicon.ico')
def favicon():
    """Serves favicon.ico"""
    return send_from_directory('static', 'img/favicon.ico')

if __name__ == '__main__':
    from waitress import serve

    debug_str = os.getenv('DEBUG', 'false')
    debug = True if debug_str.lower() == 'true' else False
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))

    if debug:
        print(f'[INFO] Debug mode enabled')

    print(f'Listening on {host}:{port}')
    serve(app, host=host, port=port)