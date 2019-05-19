import hashlib
from typing import Any

from flask import jsonify, redirect, request, url_for

from app import app, db, rate_limiter
from app.schema import URLMapping


@app.route('/<hash>', methods=['GET', 'DELETE'])
def get_url(hash: str) -> Any:
    # get total app hits and per ip hits
    max_hits, max_per_ip, total_hits, hits_per_ip = rate_limiter.check_if_valid_request(str(request.remote_addr))
    if total_hits > max_hits:
        return jsonify({'message': 'Unable to serve request temporarily', 'status': 429}), 429
    if hits_per_ip > max_per_ip:
        return jsonify({'max_request_limit': max_per_ip, 'hits': hits_per_ip, 'status': 429}), 429

    if request.method == 'GET':
        result = URLMapping.query.filter_by(hash=hash).first()  # type: URLMapping
        if not result:
            return redirect(url_for('static', filename='page_not_found.html'))
        return redirect(result.url)
    elif request.method == 'DELETE':
        result = URLMapping.query.filter_by(hash=hash).first()  # type: URLMapping
        db.session.delete(result)
        db.session.commit()
        return jsonify({"status": 200}), 200


@app.route('/put/', methods=['POST'])
def get_hash() -> Any:
    max_hits, max_per_ip, total_hits, hits_per_ip = rate_limiter.check_if_valid_request(str(request.remote_addr))

    if total_hits > max_hits:
        return jsonify({'message': 'Unable to serve request temporarily', 'status': 429}), 429
    if hits_per_ip > max_per_ip:
        return jsonify({'max_request_limit': max_per_ip, 'hits': hits_per_ip, 'status': 429}), 429

    url = request.form['url']
    md5_hash = hashlib.md5(url.encode())
    hash_string = md5_hash.hexdigest()[:6]
    db.session.add(URLMapping(hash=hash_string, url=url))
    db.session.commit()
    return jsonify({'short_url': hash_string, 'max_request_limit': max_per_ip,
                    'hits': hits_per_ip, 'status': 200}), 200


@app.route('/getall/', methods=['GET'])
def get_all() -> Any:
    max_hits, max_per_ip, total_hits, hits_per_ip = rate_limiter.check_if_valid_request(str(request.remote_addr))

    if total_hits > max_hits:
        return jsonify({'message': 'Unable to serve request temporarily', 'status': 429}), 429
    if hits_per_ip > max_per_ip:
        return jsonify({'max_request_limit': max_per_ip, 'hits': hits_per_ip, 'status': 429}), 429

    result = URLMapping.query.all()  # type: List[URLMapping]
    return jsonify({'result': [item.serialize() for item in result], 'status': '200'}), 200
