# -*- coding: utf-8 -*-
import socket, netstream
connected = False
sock = None

serialID = 0            #server向客户端发回的序列ID号
isSet = False

def connect(gameScene):
    global connected, sock
    if connected:
        return connected
    #connect server
    host = "127.0.0.1"
    port = 9234
    sock = socket.socket()
    try: 
    	sock.connect((host, port))
    except:
    	connected = False
    	return connected
    
    connected = True

    #始终接收服务端消息
    def receiveServer(dt):
    	global connected, serialID
        if not connected:
            return
        data = netstream.read(sock)
        if data == netstream.TIMEOUT or data == netstream.CLOSED or data == netstream.EMPTY:
            return
        
        #客户端SID
        if 'sid' in data:
            serialID = data['sid']

        if 'notice_content' in data:
            import game_controller
            game_controller.showContent(data['notice_content']) #showContent is from game_controller
        if 'log_mess' in data:
            import game_controller
            if data['log_mess']=='succeed':
                game_controller.signMenu()
            else:
                game_controller.showContent(data['log_mess'])
    gameScene.schedule(receiveServer)
    return connected

def get_send_data():
    send_data = {}
    send_data['sid'] = serialID
    return send_data

def send_score_to_server(game_score):
    send_data = get_send_data()
    send_data['score'] = game_score
    netstream.send(sock, send_data)

def send_result_to_server(game_score,time):
    send_data = get_send_data()
    send_data['score'] = game_score
    send_data['liveTime'] = time
    netstream.send(sock, send_data)

def send_new_user_info(username,password):
    send_data = get_send_data()
    send_data['reg'] = 'register'
    send_data['username'] = username
    send_data['password'] = password
    netstream.send(sock, send_data)

def send_log_user_info(username,password):
    send_data = get_send_data()
    send_data['log'] = 'logIn'
    send_data['username'] = username
    send_data['password'] = password
    netstream.send(sock, send_data)
#向server请求公告
def request_notice():
    send_data = get_send_data()
    send_data['notice'] = 'request notice'
    netstream.send(sock, send_data)