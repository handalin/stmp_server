#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import asyncore
import asynchat
import socket
import logging
import pdb
from stmp_log import STMPLog

##
# @brief
class ASTMPServer(asyncore.dispatcher):
    """docstring for STMPServer"""
    def __init__(self, json_config):
        asyncore.dispatcher.__init__(self)
        self.config = json_config

    def setup(self):
        # 准备日志对象
        logging.basicConfig(format=self.config["log_format"], \
                filename=self.config["log_file"])
        self.logger = logging.getLogger(self.config["server_name"])
        # 准备监听socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((self.config["host"], self.config["port"] ))
        self.listen(self.config["backlog"])
        #

    def run(self):
        self.setup()
        asyncore.loop()


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
            handler = ASTMPHandler(sock, addr, self.config)


##
# @brief
class ASTMPHandler(asynchat.async_chat):
    """docstring for STMPHandler"""
    def __init__(self, sock, addr, json_config):
        asynchat.async_chat.__init__(self, sock=sock)
        # 创建STMP 日志对象
        self.addr = addr
        self.ibuffer = []
        self.config = json_config
        self.log = STMPLog(logging.getLogger(self.config["server_name"]), self.addr)
        # 服务器回应数据很小
        self.ac_out_buffer_size = 512

        self.init()
        # 初始终止条件
        # self.set_terminator("\r\n")

    def init(self):
        """docstring for init"""
        self.log.write("begin")
        self.session = Qsession(self.log)
        self.max_buf_size = self.config["buf_size"]
        # ASTMPHandler 的默认状态是一直接收数据, 当ibuffer中数据大于限定值时,
        # 由collect_incomming_data()　负责调用found_terminator()
        self.set_terminator(None)



    ##
    # @brief
    #
    # @param data
    #
    # @return
    def collect_incoming_data(self, data):
        """docstring for collect_incoming_data"""
        self.ibuffer.append(data)
        if len(self.ibuffer) >= self.max_buf_size:
            self.found_terminator()


    ##
    # @brief
    #
    # @return
    def found_terminator(self):
        # 形成字串, 清空ibuffer
        data = "".join(self.ibuffer)
        self.ibuffer = []
        # Qsession 负责STMP协议的逻辑部分
        response, is_quit = self.session.feed(data)
        # response 为None时表示本次无需响应, 可能是由于当前待
        # 接收数据不完整
        if response is not None:
            self.push(response)
        if is_quit:
        # 执行关闭, 效果是待发送数据发送完毕, 则关闭对应链接
            self.close_when_done()

    def close_when_done(self):
        self.log.write("end")
        super(ASTMPHandler, self).close_when_done()



if __name__ == "__main__":
    stmp = ASTMPServer("127.0.0.1", 8080)
    asynchat.asyncore.loop()
