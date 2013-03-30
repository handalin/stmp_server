#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#



import sys
sys.path.append('../src')

import nose
import unittest
from qsession import Qsession


class QsessionTest(unittest.TestCase):
    """docstring for QsessionTest"""
    def setup(self):
        """docstring for setup"""
        log = open("./test.log", "w")
        self.session = Qsession(log)

    def test_writeFile(self):
        """docstring for test_writeFile"""
        self.session.filename = "session_test"
        msg = "QSESSION TEST"
        self.mail_content = msg
        self.writeFile()
        with open(self.session.filename) as stream:
            for line in stream.readlines():
                self.assertEqual(line, msg, \
                        "file msg {0} should be equal with {1}".format(line, msg))

    def test_is_addr_valid(self):
        """docstring for is_addr_valid"""
        filename = "invalid_mail_address"
        with open(filename, "r") as stream:
            for address in stream.readlines():
                self.assertEqual(False, self.session.is_addr_valid(address))
        filename = "valid_mail_address"
        with open(filename, "r") as stream:
            for address in stream.readlines():
                self.assertEqual(True, self.session.is_addr_valid(address))

    def test_checkFormal(self):
        """docstring for test_checkFormal"""
        filename = "valid_check_formal"
        # format:  cmd  session_value  data  expected_ret
        with open(filename, "r") as stream:
            for line in stream.readlines():
                items = line.split()
                items = map(items, lambda x: x.strip())
                cmd = items[0]
                if cmd == "0":
                    self.session.mail_from = items[1]
                    ret = self.session.checkFormal(items[2], int(cmd))
                    self.assertEqual(ret, bool(items[3]))
                elif cmd == "1":
                    self.session.mail_to = items[1]
                    ret = self.session.checkFormal(items[2], int(cmd))
                    self.assertEqual(ret, bool(items[3]))
                elif cmd == "2":
                    ret = self.session.checkFormal(items[1], int(cmd))
                    self.assertEqual(ret, bool(items[2]))
                elif cmd == "3":
                    ret = self.session.checkFormal(items[1], int(cmd))
                    self.assertEqual(ret, bool(items[2]))

    def test_feed(self):
        """docstring for test_feed"""
        infile  = "test_feed_data"
        outfile = "test_feed_response"
        with open(infile, "r") as instream:
            with open(outfile, "r") as outstream:
                data = instream.read().split("\r\n")
                response = outstream.read().split()








