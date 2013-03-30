#!/usr/bin/env python2
# -*- code: utf-8  -*-
#




import daemon
import time
import socket
import threading

HOST = "127.0.0.1"
PORT = 8080
BACKLOG = 5


class TSTMPServer:
    def __init__(self, json_config):
        """docstring for __init__"""
        self.config = json_config

    def create_listenfd(self):
        listenfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listenfd.bind((self.config["host"], self.config["port"]))
        listenfd.listenfd(self.config["backlog"])
        return listenfd

    def run(self):
        listenfd = create_listenfd()
        while True:
            pair = listenfd.accept()
            if pair is not None:
                conn, addr = pair
                worker = threading.Thread(target = stmp_machine, args = (conn, addr, ))
                worker.start()
                # 主线程不需要 close conn ?


def stmp_machine(connfd, addr):
    print "new in "

def main():
    pass

#with daemon.DaemonContext():
#    pass

if __name__ == "__main__":
    main()



