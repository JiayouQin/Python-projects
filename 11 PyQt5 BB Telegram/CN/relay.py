'''
This relay serves only for text based chat
'''


import threading,socket,select

def relay(conn):
    try:
        while True:
            relay_length = conn.recv(HEADER)
            if not relay_length: #receives empty header
                break
            print(f"header type{type(relay_length)}")
            print(f"receiving message from{conn}/n message length:{int(relay_length)}")
            msg = conn.recv(int(relay_length))
            print(f"message{msg}")
            if msg:
                for x in clientsockets: # Do the same stuff for every socket
                    print(f"relay length: {relay_length}")
                    x.send(relay_length)
                    x.send(msg)
                    print("encrypted message sent")

    except:
        conn.close()

    finally:
        with clientsockets_lock:
            clientsockets.remove(conn)

        conn.close()

HEADER=32
FORMAT = "UTF-8"
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object outside of the instance
host = "Admin" # local machine name
serverip = "" #just leaving it blank will do
port = 6667                # Reserve a port for your service.
print("Binding IP to socket")
serversocket.bind((serverip, port))        # Bind to the port
serversocket.listen(5)                 # Now wait for client connection.
print(f"Server has been established")
clientsockets = set()
clientsockets_lock = threading.Lock()
threadlist = []
conn = []
addr = []
strlist = []

while True:
    conn, addr = serversocket.accept()
    with clientsockets_lock:
        clientsockets.add(conn)
    print(f'clientsockets:\n')
    print(f"{addr} has connected to the Server")
    thread = threading.Thread(target=relay,args=(conn,))
    thread.start()