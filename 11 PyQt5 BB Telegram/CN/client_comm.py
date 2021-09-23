'''
Please change the host adress in the 32th line to your own server which has the relay setup,
the relay is under the same folder named as relay.
'''


import socket
import os
import threading
import sys

from configparser import ConfigParser
import pyaudio


def checkini(config):
	'''
	check if config file is present if not then create the follwing file
	'''
	file = "config/server.ini"
	try:
		with open(file) as f: #check if ini exists
			config.read(file)
	except:
		print('error occured when loading config file, creating new config file...')
		with open(file,"w+") as configfile:
			config.read(file)
			config.add_section("General")
			config.set("General","HEADER","32")
			config.set("General","port_misc","6666")
			config.set("General","port","6667")
			config.set("General","v_port","6668")
			config.set("General","HOST","111.111.111.111")
			config.set('General','timeout','5')
			config.set('General','FORMAT','UTF-8')
			config.write(configfile)

class Client:
	def __init__(self):
		config=ConfigParser()
		checkini(config)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.settimeout(int(config["General"]["timeout"]))
		self.s_misc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s_voip = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s_voip.settimeout(int(config["General"]["timeout"]))
		self.HEADER = int(config["General"]["HEADER"])
		self.port_misc = int(config["General"]["port_misc"])
		self.port = int(config["General"]["port"])
		self.port_voip = int(config["General"]["v_port"])
		self.HOST = config["General"]["HOST"]
		self.FORMAT = config["General"]["FORMAT"]
		self.cmd_show = True #show logs on command console
		self.connected = False
		self.name='???'
		self.voip_on = False
		#self.vid = cv2.VideoCapture(0)
	def voip(self,aes,callback=None,disconnect_callback=None):
		def recv_handle():
			while self.connected and self.voip_on:
				try:
					ecdata = self.s_voip.recv(CHUNK*4)
					data = aes.decrypt(ecdata)
					stream.write(data, CHUNK)
				except Exception as err:
					print(err)
			self.voip_on = False
		def send_handle():
			print("* recording")
			while self.connected and self.voip_on:
				try:
					data = stream.read(CHUNK)
					ecdata = aes.encrypt(data)
					self.s_voip.send(ecdata)
					#ret, frame = self.vid.read()# for video streaming
					#result, encimg = cv2.imencode('.jpg', frame)
					#cv2.imshow('frame',frame)
					#print(len(encimg))
				except:
					break
			self.voip_on = False
			stream.stop_stream()
			stream.close()
			p.terminate()
			
			#self.vid.release()
			disconnect_callback()
		#------------------------------
		try:
			self.s_voip=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s_voip.connect((self.HOST, self.port_voip))
			self.voip_on=True
			print('connected') if self.cmd_show else None
			callback() if callback else None
		except Exception as err:
			print(f'{err}')
			#self.vid.release()
			disconnect_callback()
			return

		self.voip_on = True
		CHUNK = 256
		WIDTH = 2
		CHANNELS = 2
		RATE = 44100
		

		p = pyaudio.PyAudio()
		stream = p.open(format=p.get_format_from_width(WIDTH),channels=CHANNELS,rate=RATE,
						input=True,output=True,frames_per_buffer=CHUNK)
		threading.Thread(target=send_handle).start()
		threading.Thread(target=recv_handle).start()


	def connect(self,aes,callback=None,msg_callback=None):
		def room_handle():
			pass
		def handle():
			while self.connected:
				try:
					print('waiting for new message') if self.cmd_show else None
					msg_len=int(self.s.recv(self.HEADER).decode(self.FORMAT))
					ecdata=self.s.recv(msg_len)
					decdata=aes.decrypt(ecdata).decode(self.FORMAT)
					print(f'incoming ecdata:{decdata}') if self.cmd_show else None
					msg_callback(decdata) if msg_callback else None
				except Exception as err:
					print(err)
					self.connected=False
					self.s.close()
		print(f'callback:{callback,msg_callback}')
		try:
			self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((self.HOST, self.port))
			self.connected=True if self.cmd_show else None
			print('connected') if self.cmd_show else None
			threading.Thread(target=handle).start()
		except Exception as err:
			print(f'{err}')
			self.connected=False
			
		callback() if callback else None #execute callback if there is any
		



	def send_msg(self,aes,msg,callback=None):
		if not msg:
			return

		msg=f'{self.name}:\n{msg}'.encode()
		ecdata=b''
		while msg:
			temp = msg[:32]
			msg = msg[32:]
			if len(temp) < 32:
				temp += (32-len(temp))* b" "
			ecdata += aes.encrypt(temp) #does not add encryption yet
		print(f"ec data length {len(ecdata)}") if self.cmd_show else None
		msg_len = str(len(ecdata)).encode(self.FORMAT)
		msg_len += b' ' * (self.HEADER - len(msg_len))
		self.s.send(msg_len) if self.cmd_show else None
		print(f'header sent,length:{msg_len}')
		self.s.send(ecdata) if self.cmd_show else None
		print(f'ecdata sent:\n{ecdata}')
		callback() if callback else None


