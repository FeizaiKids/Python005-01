#!/usr/bin/env python
import socket

HOST = 'localhost'
PORT = 9900


def client():
    '''
    clent.py will send the 'client.png' to server folder
    '''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print('Client connected to the server')

    file = open('client.png', "rb")
    
    client_socket.sendall(file.read())
    file.close()    
    client_socket.close()


if __name__ == '__main__':
    client()
