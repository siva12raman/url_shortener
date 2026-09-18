import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200


@app.route('/api/v1/urls', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True) or {}
    long_url = data.get('long_url')
    alias = data.get('alias')

    # Placeholder status responses for future reference:
    # 400: invalid URL
    # 429: rate limit
    # 409: shortURL already taken
    # 201: {"short_url": "", "expires_at": "", "created_at": ""}

    if not long_url:
        return jsonify({'error': 'invalid URL'}), 400

    now = datetime.now(timezone.utc).isoformat()
    short_code = alias if alias else 'sample123'
    return jsonify({
        'short_url': f"http://localhost:{os.environ.get('PORT', 5001)}/{short_code}",
        'expires_at': None,
        'created_at': now
    }), 201


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
