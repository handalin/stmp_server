#!/usr/bin/python

import socket

print "Creating socket...",
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "done."

port = 54321
print "Port: %d" % port
print "Connecting to remote host...",
s.connect((s.getsockname()[0], port))
print "done."

print "++++++++++++++++"
print s.getsockname()
print s.getpeername()
k = 0
try:
  while True:
    data = raw_input("DATA to transmit:\n")
    #data = lines[k]
    #k += 1
    s.send(data)
    if data == 'C':
      print "Quit."
      break
    data = s.recv(4096)
    print data + "_____BACK"
except socket.timeout:
  print 'Time out.'
  
