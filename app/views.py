from app import app
from flask import render_template, request, make_response, jsonify
import server
import json

server_instance = None
urls = json.load(open('urls', 'r'))

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Кот' } # выдуманный пользователь

    urls = json.load(open('urls', 'r'))

    return render_template("index.html",
        title = 'Home',
        user = user,
        urls = urls)

@app.route('/play', methods=['POST'])
def play():
    for k, v in request.form.items():
        cmd = k
    if cmd !='stop':

        try:
            global server_instance
            if server_instance is None:
                server_instance = server.Server(urls[cmd])
                server_instance.start
            else:
                server_instance.stop
                server_instance = server.Server(urls[cmd])
                server_instance.start
        except:
            make_response(jsonify({'status': 'fail'}))
        else:

            return make_response(jsonify({'status' : 'OK' }))
    elif cmd == 'stop':
        try:
            server_instance.stop
        except:
            make_response(jsonify({'status': 'fail'}))
        else:
            return make_response(jsonify({'status': 'OK'}))