#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#


from logging import Logger


class STMPLog:
    """docstring for STMPLog"""
    def __init__(self, logger, clientip):
        self.log = logger
        self.extra = {'clientip': clientip }

    def write(self, msg):
        self.log.warning(msg)







