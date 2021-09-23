import threading
import time
from Cryptodome.Random import get_random_bytes
import pyaudio
from threading import Thread
import global_values as g
import custom_components as ccp
from PyQt5 import QtWidgets
import pyaudio


def generate_key(path='32byteskey.pem'):
	key = get_random_bytes(32)
	with open(path, mode='wb') as f:
		f.write(key)	

def dialog_show(title,content,choice=False): 
	dlg = QtWidgets.QMessageBox()
	dlg.setWindowTitle(title)
	dlg.setText(content)
	if choice:
		dlg.setStandardButtons(True | False)
	#dlg.setIcon(QtWidgets.QMessageBox.Question)
	button = dlg.exec()
	#if button == QtWidgets.QMessageBox.Yes:
	return button

def login_click():
	def callback():
		if g.client.connected:
			g.window.show()
			g.login_window.close()
			print(f'connected \n{g.client.s}')
			g.ui.label_connect_status.setText('在线')
			g.ui.label_connect_status.setStyleSheet('background-color: rgb(40,255,40);color: rgb(255, 255, 255);')
			g.ui.textBrowser.append('...加载完B!')
			#add name if it is not empty
			name = g.login_ui.input_account.text()
			g.client.name = name if name else g.client.name
		else:
			g.login_ui.btn_login.setEnabled(True)
			g.login_ui.btn_login.setText('重连')
	def msg_callback(ecdata):
		g.ui.textBrowser.signal.emit(ecdata)
	#---------------
	g.login_ui.btn_login.setEnabled(False)
	g.login_ui.btn_login.setText('连接中...')
	g.client.connect(g.aes,callback,msg_callback)

def msg_callback_func(ecdata):
	print(f'encrypted data:\n{ecdata}')
	g.ui.textBrowser.append(ecdata)
	g.ui.input_box.clear()

def draw_chatlog():
	'''
	All this FUCKING JUNK code just to update the GUI in a thread
	'''
	import custom_components as ccp
	x,y=20,20
	w,h=g.ui.widget_chatlog.width(),g.ui.widget_chatlog.height()
	g.ui.textBrowser = ccp.CustomTextEdit(g.ui.widget_chatlog)
	g.ui.textBrowser.setGeometry(x,y,w-int(2*x),h-int(2*y))
	g.ui.textBrowser.signal.connect(msg_callback_func)

def send_click():
	def callback():
		#g.ui.input_box.clear()
		pass
	#---------------
	print('clicked')
	if g.client.connected:
		g.client.send_msg(g.aes,g.ui.input_box.toPlainText(),callback)

def voip_click():
	def callback():
		g.ui.btn_voip.setStyleSheet('background-color: rgb(255, 120, 120);color: rgb(255, 255, 255);')
	def reset():
		g.ui.btn_voip.setStyleSheet('background-color: rgb(124, 255, 150);color: rgb(255, 255, 255);')
		g.client.voip_on = False
	#---------------
	if g.client.connected and g.client.voip_on==False:
		g.client.voip(g.aes,callback,reset)

	else:
		reset()

	import numpy as np
	import pyaudio	 #sudo apt-get install python-pyaudio


import pysine
import pyaudio  
import wave  

def input_space():
	global timer
	global n_bit
	def handle():
		while g.pressed:
			pysine.sine(frequency=2000.0, duration=(0.005)) 
	
	timer=time.time()
	g.pressed = True
	Thread(target=handle).start()

def input_space_released():



	global n_bit
	global char
	global timer


	
	g.pressed=False
	print('released')
	timer = time.time() - timer
	print(f'time: {timer}s')
	code = '1' if timer >= 0.2 else '0'
	char = char + code
	print(char)
	if n_bit >= 6:
		g.ui.input_space.setEnabled(False)
		n_bit = 0
		print(f'binary code:{char}')
		print(int(char, 2))
		input_char=chr(int(char, 2))
		play_sound('change_line.wav')
		g.ui.input_space.setEnabled(True)
		g.ui.input_box.setText(g.ui.input_box.toPlainText()+input_char)
		char='0'
		return

	n_bit += 1
	

def play_sound(path):
	chunk = 1024  
	f = wave.open(path,"rb")  
	#instantiate PyAudio  
	p = pyaudio.PyAudio()  
	#open stream  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
					channels = f.getnchannels(),  
					rate = f.getframerate(),  
					output = True)  
	#read data  
	data = f.readframes(chunk)  
	#play stream  
	while data:  
		stream.write(data)  
		data = f.readframes(chunk)  
	#stop stream  
	stream.stop_stream()  
	stream.close()  
	#close PyAudio  
	p.terminate()  


char='0'
n_bit=0
timer=0