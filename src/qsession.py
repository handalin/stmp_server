#!/usr/bin/python
import os
class Qsession(object):
  def __init__( self, LOG ):
    self.stat = 0 # waiting for 'helo'
    self.mail_content = ''
    self.LOG = LOG
    self.content_read_cnt = 0
    self.MAX_LEN = 1024 * 1024 # 1MB
    self.tips = [
        "Input Valid. ( 'From: xxx@yy.com' )",
        "Input Valid. ( 'To: xxx@yy.com' )",
        "Input Valid. ( 'Subjext: zzzzzz' )",
        "Input enter, please."
        ]

  def writeFile( self ):
    f = open ( self.filename, 'wa')
    f.write(self.mail_content)
    #f.flush()
    f.close()

  def is_addr_valid( self, addr ):
    x = addr.split('@')
    return x and x[1].split('.')
  
  def checkFormal(self, data, cnt):
    if cnt == 0:
      return data[:6] == "From: " and data[6:] == self.mail_from
    elif cnt == 1:
      return data[:4] == "To: " and data[4:] == self.mail_to
    elif cnt == 2:
      return data[:9] == "Subject: "
    elif cnt == 3:
      return data == ''

  def feed(self, data):
    if data == 'quit' and self.stat != 3 :
      # User Quit.
      return ( '221 Bye', False )
    
    back_msg = None
    if self.stat == 0 :
      if data[:4] == "helo":
        self.stat += 1
        self.filename = 'mails/' + data[5:]
        back_msg = "220 QQMail Ver 1.0"
        # check the file name
        while os.path.isfile( self.filename ):
          self.filename += '#'
      else :
        back_msg = "502 Error\nTips:Log on frist. ( 'helo yourname' )"

    elif self.stat == 1 :
      if data[:11] == "mail from: " and self.is_addr_valid(data[11:]):
        self.stat += 1
        back_msg = "250 OK"
        self.mail_from = data[11:]
      else:
        back_msg = "502 Error\nTips:Input from address. ( 'mail from: xxx@yy.com')"

    elif self.stat == 2 :
      if data[:9] == "rcpt to: " and self.is_addr_valid(data[9:]):
        self.stat += 1
        back_msg = "250 OK"
        self.mail_to = data[9:]
      else:
        back_msg = "502 Error\nTips:Input to address. ( 'rcpt to: xxx@yy.com' )"

    elif self.stat == 3 :
      if data == 'data':
        self.stat += 1
        back_msg = "354 start mail input; en with <CRLF>.<CRLR>"
      else:
        back_msg = "502 Error\nTips: Input 'data'"

    elif self.stat == 4 :
      if self.content_read_cnt < 4:
        if not self.checkFormal(data, self.content_read_cnt):
          back_msg = "502 Error\nTips:" + self.tips[self.content_read_cnt]
        else :
          self.content_read_cnt += 1
      elif data != ".":
        self.mail_content += data + '\n'
        if len(self.mail_content) > self.MAX_LEN :
          self.writeFile( )
          self.mail_content = ''
      elif data == "." :
        # write file
        self.stat = 1 
        back_msg = "250 OK"
        self.writeFile( )

    #self.LOG.write(back_msg)
    return ( back_msg , True )


