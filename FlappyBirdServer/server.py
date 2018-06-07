# -*- coding: utf-8 -*-
import socket, select, netstream, random, pickle, os, traceback

HOST = "127.0.0.1"
disconnected_list = []#断开连接的客户端列表
onlineUser = {}
sid = 0

if __name__ == "__main__":
	s = socket.socket()

	host = HOST
	port = 9234

	s.bind((host, port))
	s.listen(4)

	inputs = []
	inputs.append(s)
	print 'server start! listening host:', host, ' port:', port

while inputs:
	try:
		rs, ws, es = select.select(inputs, [], [])
		for r in rs:
			if r is s:
				print 'sid:', sid
				# accept
				connection, addr = s.accept()
				print 'Got connection from' + str(addr)
				inputs.append(connection)
				sendData = {}
				sendData['sid'] = sid
				netstream.send(connection, sendData)

				cInfo = {}
				cInfo['connection'] = connection
				cInfo['addr'] = str(addr)
				cInfo['ready'] = False
				onlineUser[sid] = cInfo
				print(str(onlineUser))
				sid += 1
			else:
				# receive data
				recvData = netstream.read(r)
				# print 'Read data from ' + str(r.getpeername()) + '\tdata is: ' + str(recvData)
				# socket关闭
				if recvData == netstream.CLOSED or recvData == netstream.TIMEOUT:
					if r.getpeername() not in disconnected_list:
						print str(r.getpeername()) + 'disconnected'
						disconnected_list.append(r.getpeername())
				else:  # 根据收到的request发送response
					#公告
					if 'notice'in recvData:
						number = recvData['sid']
						print 'receive notice request from user id:', number
						sendData = {"notice_content": "This is a notice from server. Good luck!"}
						netstream.send(onlineUser[number]['connection'], sendData)
					if 'score' in recvData:
						print 'score: ',recvData['score']
					if 'reg' in recvData:
						print 'user ',recvData['username']
						print 'Psw ',recvData['password']
						output = open('user.txt', 'a+')
						output.writelines([recvData['username'],'\n',recvData['password'],'\n'])
						#output.write(recvData['password'])
						output.close()
					if 'log' in recvData:
						print 'log'
						sendData = {"log_mess": "wrong username"}
						number = recvData['sid']
						print 'user ',recvData['username']
						print 'Psw ',recvData['password']
						userFile = open('user.txt', 'r')
						userLine=userFile.read().splitlines()
						for index in range(len(userLine)):
							if index%2==0 and userLine[index]==recvData['username']:
								print 'f-user ',userLine[index]
								print 'f-Psw ',userLine[index+1]
								if userLine[index+1]==recvData['password']:
									sendData = {"log_mess": "succeed"}
									onlineUser[number]['username']=recvData['username']
									onlineUser[number]['password']=recvData['password']
									break
								else:
									sendData = {"log_mess": "wrong password"}
									break
						netstream.send(onlineUser[number]['connection'], sendData)
						userFile.close()
					if 'liveTime' in recvData:
						user=onlineUser[number]['username']
						output = open('./score/'+user+'.txt', 'a+')
						output.writelines([str(recvData['score']),'\n',str(recvData['liveTime']),'\n'])
						output.close()
	except Exception:
		traceback.print_exc()
		print 'Error: socket 链接异常'