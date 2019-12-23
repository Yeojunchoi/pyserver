import socket
from _thread import *

def threaded(client_socket, addr):
    print('Connected by:', addr[0], ':',addr[1])

    while True:

        try:
            datatogcs = client_socket.recv(256)
            datatodrone= gcs_socket.recv(256)
            if not datatogcs:
                print('Disconnected from drone' + addr[0],',',addr[1])
                break

            print('Received from drone' + addr[0],':',addr[1], datatogcs)
            print('Received from gcs' + addr[0],':',addr[1], datatodrone)
            gcs_socket.send(datatogcs)
            client_socket.send(datatodrone)
        except ConnectionResetError as e:
            print('Disconnected by' + addr[0],':',addr[1])
            print('Type of error', e)
            break
    client_socket.close()
    gcs_socket.close()

HOST = ''
PORT = 5760

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind((HOST,PORT))
server_socket.listen()
gcs_socket = socket.socket()
gcs_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
gcs_socket.bind((HOST,9999))
gcs_socket.listen()

print('server start')

while True:
    print('waiting')

    client_socket, addr = server_socket.accept()
    gcs_socket, addr = gcs_socket.accept()
    start_new_thread(threaded, (client_socket, addr))