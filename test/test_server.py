import os
import threading
import client_han
max_cnt = 1000

def conn():
  os.system("python client_holdon.py")

for i in range(max_cnt):
  t = threading.Thread( target = conn )
  t.setDaemon(1)
  t.start()
  
