# -*- coding: utf-8 -*-

#NOTE: you are NOT allowed to use the "requests" library in python in the assignment
from socket import *

#default IP and PORT
IP = '127.0.0.1'
PORT = 8080

hello = [b'HTTP/1.0 200 OK\r\n', b'Connection: close' b'Content-Type:text/html; charset=utf-8\r\n', b'\r\n',
         b'<html><body>Hello World!<body></html>\r\n', b'\r\n']
err404 = [b'HTTP/1.0 404 Not Found\r\n', b'Connection: close' b'Content-Type:text/html; charset=utf-8\r\n', b'\r\n',
          b'<html><body>404 Not Found<body></html>\r\n', b'\r\n']
def proxy():
    # Create a server socket
    ProxySocket = socket(AF_INET, SOCK_STREAM)
    #bind it to the IP and Port,start listening and work
    # Fill in start.
    ProxySocket.bind((IP, PORT))
    ProxySocket.listen(10)
    # Fill in end.
    while 1:
        # Strat receiving data from the client
        print('Ready to serve...')
        Proxy_client_conn, addr = ProxySocket.accept()
        print('Received a connection from:', addr)
        # Proxy the request from the clinet
        # Fill in start.
        data = Proxy_client_conn.recv(2048).decode().split('\r\n')
        print(data[0].split(' '))
        res = err404
        if data[0].split(' ')[1] == '/':
            res = hello
        for line in res:
            Proxy_client_conn.send(line)
        Proxy_client_conn.close()
        # Fill in end.
        Proxy_client_conn.close()

# Fill in start.


if __name__ == "__main__":
    try:
        proxy()
    except KeyboardInterrupt:
        pass
# Fill in end.
