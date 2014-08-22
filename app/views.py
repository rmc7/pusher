# -*- coding: utf-8 -*-
from flask import request, render_template, jsonify, session
from app import app
import pusher
from datetime import datetime
from time import time


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET'])
def send():
    name = request.args.get("name_data")
    msg = request.args.get("msg_data")
    p = pusher.Pusher(
      app_id='86076',
      key='775a6c9c734291f6ccab',
      secret='a3fbc79fac9e20d744fb'
    )
    p['test_channel_room'].trigger('my_event', {
        'name': name,
        'msg': msg
    })
    return ""

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/mainsend', methods=['GET'])
def mainsend():
    name = request.args.get("name_data")
    msg = request.args.get("msg_data")
    p = pusher.Pusher(
      app_id='86076',
      key='775a6c9c734291f6ccab',
      secret='a3fbc79fac9e20d744fb'
    )
    p['main_room'].trigger('main_event', {
        'name': name,
        'msg': msg
    })
    return ""

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chat-login', methods=['POST'])
def chatlogin():
    if 'id' in request.form:
        id = request.form.get('id')
        session['username'] = id
        result = {'success':True, 'msg':'Login Successfully'}
        return jsonify(result)
    else:
        return jsonify(success=False)
    
@app.route('/pusher/auth', methods=['POST'])
def push_auth():
    p = pusher.Pusher(app_id='86076', key='775a6c9c734291f6ccab', secret='a3fbc79fac9e20d744fb')
    socket_id = request.form.get('socket_id')
    channel_name = request.form.get('channel_name')
# 위 2줄의 ()안은 따로 설정안해도 pusher에서 알아서 보냄(socket과 channel은 고유이름)
# socket은 사용자 1명이 서버와 통신하는 것.
    username = session['username']

    channel_data = {'user_info':{'username':username}}
    channel_data['user_id'] = username
# 위 2줄의 dic에서 key값 2개(info, id)는 바꾸면 인식을 못함. pusher에서 정해둔 것.
# 윗 줄의 username이 중요하고, 아랫줄 = username은 덜중요-user마다 다르기만 하면됨
# = username은 여기선 쉽게하려고 저렇게 씀(바꿔도됨). 개별 식별자로 사용되어야.
# = username에 primary key를 쓰면 user끼리 중복안되고 사용가능
    response = p[channel_name].authenticate(socket_id, channel_data)

    return jsonify(response)

@app.route('/send_msg', methods=['POST'])
def send_msg():
    p = pusher.Pusher(app_id='86076', key='775a6c9c734291f6ccab', secret='a3fbc79fac9e20d744fb')
    username = session['username']
# 서버에 저장된 정보(session)를 아래 new_msg에서 사용함. 매번 id도 같이 보낼필요없음
    msg = request.form.get('msg')
    ti = time()
    st = datetime.fromtimestamp(ti).strftime('%Y-%m-%d %H:%M:%S')
    # st = datetime.fromtimestamp(ti).strftime('%Y년-%m월-%d일 %H:%M:%S')
# 입력받은 시간을 strftime을 통해 string form으로 바꿔줌
    p['presence-jrm-room'].trigger('new_msg',{'msg':msg, 'username':username, 'time':st})
    return jsonify(success=True)

