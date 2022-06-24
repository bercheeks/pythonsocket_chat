import socket
import threading

from cairo import FORMAT_A1 # so clients dont have to wait for other clients to send/recieve messages

# gets local ip address of NIC. e.g. eth0, wlp2s0
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

HEADER = 64
PORT = 5600 # port for the server running
SERVER = get_ip_address() #ip of the server
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


#make a socket that will allow to open up this device to other connections
# 1. pick the port and server
# 2. pick the socket. then bind the socket to the server 

server =socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_NET specifies the type of network addresses
server.bind(ADDR)

# handles individual connections between client and server
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            #conn.send("MSG Recieved".encode(format))

    conn.close()




# handles new connections
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")

print("[STARTING] server is starting... ")
start()