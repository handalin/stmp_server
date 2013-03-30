#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#



from astmp_server import ASTMPServer
from tstmp_server import TSTMPServer
import json
import daemon

JSON_CONFIG = "server.config.json"

def main():
    config = json.load(open(JSON_CONFIG, "r"))
    server = ASTMPServer(config)
    # server = TSTMPServer(config)
    with daemon.DaemonContext():
        server.run()



if __name__ == "__main__":
    main()


