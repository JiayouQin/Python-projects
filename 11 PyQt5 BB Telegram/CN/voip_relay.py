'''
This relay serves only for text based chat
'''


import threading,socket,select

def relay(conn):
    try:
        while True:
            data = conn.recv(HEADER)
            if not data: #receives empty header
                break
            for x in clientsockets: # Do the same stuff for every socket
                #if x is not conn:
                x.send(data)
    except:
        conn.close()

    finally:
        with clientsockets_lock:
            clientsockets.remove(conn)

        conn.close()

HEADER=1024
FORMAT = "UTF-8"
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object outside of the instance
host = "Admin" # local machine name
serverip = "" #just leaving it blank will do
port = 6668             # Reserve a port for your service.
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
    print(f"{addr} has connected to the Server")
    thread = threading.Thread(target=relay,args=(conn,))
    thread.start()