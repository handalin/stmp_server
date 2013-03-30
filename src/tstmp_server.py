#!/usr/bin/env python2
# -*- coding: utf-8  -*-
#




import daemon
import time
import socket
import threading
import logging
from stmp_log import STMPLog
from qsession import Qsession

HOST = "127.0.0.1"
PORT = 8080
BACKLOG = 5


class TSTMPServer:
    def __init__(self, json_config):
        """docstring for __init__"""
        self.config = json_config
        self.setup()

    def setup(self):
        # 准备日志对象
        logging.basicConfig(format=self.config["log_format"], \
                filename=self.config["log_file"])
        self.logger = logging.getLogger(self.config["server_name"])


    def create_listenfd(self):
        listenfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listenfd.bind((self.config["host"], self.config["port"]))
        listenfd.listen(self.config["backlog"])
        return listenfd


    ##
    # @brief
    #
    # @return
    def run(self):
        listenfd = self.create_listenfd()
        while True:
            pair = listenfd.accept()
            if pair is not None:
                conn, addr = pair
                log = STMPLog(self.logger, addr)
                stmp_machine = STMPMachine(conn, addr, log, self.config)
                worker = threading.Thread(target = stmp_machine.run, args = (stmp_machine, ))
                worker.start()
                # 主线程不需要 close conn ?



class STMPMachine:
    """docstring for STMPMachine"""
    def __init__(self, conn, addr, log, json_config):
        self.conn = conn
        self.addr = addr
        self.log  = log
        self.config  = json_config
        self.session = Qsession(log)
        self.timeout = self.config["timeout"]
        self.bufsize = self.config["bufsize"]

    def write(self, msg):
        self.send(msg)

    def read(self):
        self.conn.settimeout(self.timeout)
        try:
            data = self.conn.recv(bufsize)
        except socket.timeout:
            # 直接设置为None, data中应该没有数据??
            data = None
        return data

    def close(self):
        self.conn.close()


    def run(self):
        is_close = True
        bye_msg = None
        while is_close:
            data = self.read()
            if data is None:
                bye_msg = "用户长时间无响应, 强制关闭连接"
                break
            response, is_quit = self.session.feed(data)
            if response is not None:
                self.write(response)
            if is_quit:
                bye_msg = "用户正常退出，关闭连接"
                break
        self.log.write(bye_msg)
        self.close()


def main():
    pass

#with daemon.DaemonContext():
#    pass

if __name__ == "__main__":
    main()



