#!/usr/bin/env python
import socket
import os

HOST = 'localhost'
PORT = 9900


def server():    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((HOST, PORT))    
    server_socket.listen(1)
    print('Server listening...')
    
    while True:        
        conn, addr = server_socket.accept()        
        print(f'Connected by {addr}')

        data_sum = b''
        data = conn.recv(1024)
        data_sum += data

        while len(data) > 0 :
            data = conn.recv(1024)
            data_sum += data            
        
        with open(os.path.join(os.path.dirname(__file__), "server.png"),"wb") as f:
            f.write(data_sum)
        conn.close()
    server_socket.close()


if __name__ == '__main__':    
    server()