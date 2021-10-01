# -*- coding: utf-8 -*-

#NOTE: you are NOT allowed to use the "requests" library in python in the assignment

#default IP and PORT
import socket
import requests

IP = '127.0.0.1'
PORT = 8080
bufferSize = 2048
def proxy():
    # Create a server socket
    ProxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind it to the IP and Port,start listening and work
    # Fill in start.
    ProxySocket.bind((IP, PORT))
    ProxySocket.listen(10)

    # Fill in end.
    while 1:
        # Strat receiving data from the client
        print('Ready to serve...')
        # client to proxy
        Proxy_client_conn, addr = ProxySocket.accept()
        print('Received a connection from:', addr)
        # Proxy the request from the clinet
        # Fill in start.
        data = Proxy_client_conn.recv(bufferSize)
        data_decode = data.decode().split('\r\n')
        #proxy to web
        web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        webserver = data_decode[1].split(' ')[1]
        web.connect((webserver, 80))
        web.send(data)
        while 1:
            web.settimeout(2)
            try:
                web_reponse = web.recv(bufferSize)
            except socket.error:
                break

            if (len(web_reponse) > 0):
                Proxy_client_conn.send(web_reponse)
        Proxy_client_conn.close()
        web.close()

        # Fill in end.


# Fill in start.


if __name__ == "__main__":
    try:
        proxy()
    except KeyboardInterrupt:
        pass
# Fill in end.
