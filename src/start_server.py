#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#



from astmp_server import ASTMPServer
from tstmp_server import TSTMPServer
import json
import daemon
import pdb

JSON_CONFIG = "server.config.json"

def main():
    #pdb.set_trace()
    config = json.load(open(JSON_CONFIG))
    server = ASTMPServer(config)
    # server = TSTMPServer(config)
    server.run()
    with daemon.DaemonContext():
        pdb.set_trace()
        server.run()



if __name__ == "__main__":
    main()


