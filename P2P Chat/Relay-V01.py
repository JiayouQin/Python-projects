#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import filedialog, Text
import threading,socket


class mainfunc(threading.Thread):
    def __init__(self,windowsize,s):
        threading.Thread.__init__(self)
        self.start()
        self.windowsize = windowsize
        self.connected = False
        self.s = s
        self.conn = []
        self.addr = []
    def run(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,width = self.windowsize[0],height = self.windowsize[1], bg="#fad92f")
        self.canvas.pack()
        self.sending = ""
        print(self.sending)
        #---------------chat page-----------------
        self.chatlogbg = tk.Canvas(self.root, bg="#fad92f")
        self.chatlogbg.place(relwidth=0.85,relheight=0.80,relx=0.15,rely=0)
        self.textBox1=Text(self.chatlogbg,height=4)
        self.textBox1.place(relwidth=0.9,relheight=0.9,relx=0.02,rely=0.05)

        
        #---------------input --------------------
        self.inputblank = tk.Frame(self.root, bg="#b5b5b5")
        self.inputblank.place(relwidth=0.85,relheight=0.2,relx=0.15,rely=0.8)
        self.textBox2=Text(self.inputblank,height=4)
        self.textBox2.place(relwidth=0.95,relheight=0.9,relx=0.02,rely=0.05)
        self.submit = tk.Button(self.inputblank)
        self.root.bind('<Return>', self.uicallback)
        self.root.bind('<space>', self.updatechats)
        
        #---------------sidebar-------------------
        self.sidebar = tk.Frame(self.root, bg="#000000")
        self.sidebar.place(relwidth=0.15,relheight=1)
        self.redraw()
        
    def redraw(self):
        self.root.mainloop()
        print("session ended")
    def uicallback(self,event):
        print(f"debug-isserverL:{isserver}")
        if self.connected == True:
            self.sending = name +": "+ self.textBox2.get("1.0", "end-1c")
            self.textBox1.insert(tk.END, self.sending)
            sending(self.sending)
            self.textBox2.delete("1.0", "end-1c")
            
    def updatechats(self,event):
        
        self.chatlogbg.select_clear()
        print(self.sending)

def sending(inputmessage):
    if inputmessage != "/disconnect":
        message = inputmessage.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        if isserver == True:
            print("server sent a message")
            uiinstance.conn.send(send_length)# Gets me everytime, this should only be an adress on server's end
            uiinstance.conn.send(message)
        if isserver == False:
            uiinstance.s.send(send_length)
            uiinstance.s.send(message)
        print(message)
    
def handle_client(conn, addr):
    
    print(f"{addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length) #how many bytes will be receiving
            msg = conn.recv(msg_length).decode(FORMAT)
            uiinstance.textBox1.insert(tk.END, msg)
            if msg == "/disconnect":
                connected = False
    conn.close()
    print ("connection to client is closed")
    
def server_listen_start():
    s.listen()
    print (f"server is listening on {serverip}")
    while True:
        uiinstance.conn, uiinstance.addr = s.accept()
        thread = threading.Thread(target=handle_client,args=(uiinstance.conn, uiinstance.addr))
        thread.start()
        print(f"active connections:{ threading.activeCount()-1}")
        
def client_listen_start():
    connected = True
    print (f"server is listening on {serverip}")
    while connected:
        msg_length = s.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length) #how many bytes will be receiving
            msg = s.recv(msg_length).decode(FORMAT)
            uiinstance.textBox1.insert(tk.END, msg)
            if msg == "/disconnect":
                connected = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
windowsize = (1440,720)
uiinstance = mainfunc(windowsize,s)

print("Threading Ok")
name = "WTF01"
HEADER = 64
FORMAT = "UTF-8"
port = 6666
serverip = ""
clientip = socket.gethostbyname(socket.gethostname()) # get host ip

#--------------Ask if is server
print("is this a server?")
inputcheck = input()

while (inputcheck != "n" and inputcheck != "y"):
    inputcheck = str(input())

#--------------is a client
if inputcheck == "n":
    isserver = False
    print("Binding IP to socket")
    print(f"connecting to peer{serverip}.")
    uiinstance.s.connect((serverip,port))
    print(f"peer{serverip} connected.")
    uiinstance.connected = True
    client_listen_start()
else:
    isserver = True
    uiinstance.s.bind((serverip,port))
    print("Binding IP to socket")
    print(f"Server has been established")
    uiinstance.connected = True
    uiinstance.textBox1.insert(tk.END, f"Server Loaded/n")
    server_listen_start()
    
        


# In[ ]:





# In[ ]:




