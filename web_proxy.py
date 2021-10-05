# -*- coding: utf-8 -*-

# NOTE: you are NOT allowed to use the "requests" library in python in the assignment

# default IP and PORT
import os
import socket
import threading
import time

import requests


class Proxy(threading.Thread):
    def __init__(self, conn, address):
        threading.Thread.__init__(self)
        self.Proxy_client_conn = conn
        self.address = address

    def run(self):
        data = self.Proxy_client_conn.recv(bufferSize)
        data_decode = data.decode().split('\r\n')
        # get filename
        url = data_decode[0].split(' ')[1]

        last_index = url.rfind('/')
        filename = url[last_index:]
        if (filename == '/'):
            filename = 'index.html'
        else:
            filename = url[last_index + 1:]
        cacheFolder = data_decode[1].split(' ')[1]

        if (data_decode[0].split(' ')[0] == 'HEAD'):
            filename = 'HEAD' + filename

        try:
            # check in cache
            self.GetContentFromCache(filename, cacheFolder)
        except FileNotFoundError:
            # get from server
            self.GetContentFromServer(data, data_decode, filename, cacheFolder)

    def GetContentFromCache(self, filename, cacheFolder):
        fin = open(cacheFolder + '/cache' + filename, 'rb')
        #cache_response = fin.read()
        # last_index = cache_response.rfind('\n\n\n')

        self.Proxy_client_conn.sendfile(fin)
        fin.close()
        print('Read From Cache')
        # self.Proxy_client_conn.send('Read From Cache'.encode())
        # self.Proxy_client_conn.close()

    def GetContentFromServerNoCaching(self, data, data_decode):
        web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        webserver = data_decode[1].split(' ')[1]
        web.connect((webserver, 80))
        web.send(data)
        while 1:
            web.settimeout(2)
            try:
                web_reponse = web.recv(bufferSize)
                print('get Content from web')
                web_response_decode = web_reponse.decode()

            except socket.error:
                break

            if (len(web_reponse) > 0):
                self.Proxy_client_conn.send(web_reponse)

    def GetContentFromServer(self, data, data_decode, filename, cacheFolder):
        # proxy to web
        web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        webserver = data_decode[1].split(' ')[1]
        web.connect((webserver, 80))
        web.send(data)
        if not os.path.exists(cacheFolder):
            os.makedirs(cacheFolder)
        cached_file = open(cacheFolder + '/cache' + filename, 'wb')
        while 1:
            web.settimeout(2)
            try:
                web_reponse = web.recv(bufferSize)
                print('get Content from web')
                web_response_decode = web_reponse.decode()
                cached_file.write(web_reponse)
            except socket.error:
                break

            print('Write Content to Caches')
            if (len(web_reponse) > 0):
                self.Proxy_client_conn.send(web_reponse)
        cached_file.close()


IP = '127.0.0.1'
PORT = 8080
bufferSize = 2048


def proxy():
    # Create a server socket
    ProxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind it to the IP and Port,start listening and work
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
        Proxy(Proxy_client_conn, addr).start()


if __name__ == "__main__":
    try:
        proxy()
    except KeyboardInterrupt:
        pass
# Fill in end.
