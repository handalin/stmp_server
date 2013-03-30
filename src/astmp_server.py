#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import asyncore
import asynchat
import socket


##
# @brief
class ASTMPServer(asyncore.dispatcher):
    """docstring for STMPServer"""
    def __init__(self, json_config):
        asyncore.dispatcher.__init__(self)
        self.config = json_config
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((self.config["host"], self.config["port"] ))
        self.listen(self.config["backlog"])


    ##
    # @brief
    #
    # @return
    def handle_accept(self):
        """docstring for handle_accpet"""
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            # log
            handler = ASTMPHandler(sock, addr)


##
# @brief
class ASTMPHandler(asynchat.async_chat):
    """docstring for STMPHandler"""
    def __init__(self, sock, addr, log = None):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        #self.sessions = sessions
        self.ibuffer = []
        self.obuffer = ""
        self.log = log
        # 服务器回应数据很小
        self.ac_out_buffer_size = 512

        self.mail_from = None
        self.mail_to   = None
        # 初始终止条件
        self.state = 0
        self.set_terminator("\r\n")


    ##
    # @brief
    #
    # @param data
    #
    # @return
    def collect_incoming_data(self, data):
        """docstring for collect_incoming_data"""
        self.ibuffer.append(data)


    ##
    # @brief
    #
    # @return
    def found_terminator(self):
        """docstring for fname"""
        #self.set_terminator("\r\n")
        cmd = "".join(self.ibuffer)
        self.ibuffer = []
        print cmd
        if cmd == "quit":
            self.close_when_done()


if __name__ == "__main__":
    stmp = ASTMPServer("127.0.0.1", 8080)
    asynchat.asyncore.loop()
