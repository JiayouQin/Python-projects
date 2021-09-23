import sys

from PyQt5 import QtWidgets,QtCore

from login_window import Ui_login_window
from main_window import Ui_MainWindow

import functions as f

from client_comm import Client
from Cryptodome.Cipher import AES


def connect_functions():
	#--------------login menu
	login_ui.btn_login.clicked.connect(f.login_click)

	#--------------chat window
	ui.btn_send.clicked.connect(f.send_click)
	ui.btn_voip.clicked.connect(f.voip_click)
	ui.input_space.pressed.connect(f.input_space)
	ui.input_space.released.connect(f.input_space_released)

#------------initial parameter
run=True
pressed=False
#------------setting up UI/UI functions
app = QtWidgets.QApplication(sys.argv)
login_window = QtWidgets.QMainWindow()
login_ui = Ui_login_window()
login_ui.setupUi(login_window)

window = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

f.draw_chatlog()
connect_functions()


#------------instantiate
client=Client()

with open('32byteskey.pem', mode='rb') as f:
    key = f.read()   
aes=AES.new(key, AES.MODE_ECB)