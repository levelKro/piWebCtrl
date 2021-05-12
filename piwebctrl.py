#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
from os import path

hostName = ""
hostPort = 80

class piWebCtrl(BaseHTTPRequestHandler):

    #GET is for clients geting the predi
    def do_GET(self):
        thisPath = self.path.split("?")
        if thisPath[0] == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            fstr = open(r"web/index.html", encoding="utf-8").read()
            self.wfile.write(bytes(fstr, "utf-8"))
        elif thisPath[0] == "/run/reboot":
            self.send_response(200)
            self.wfile.write(bytes('{"html":"Rebooting the Raspberry Pi","cmd":null}', "utf-8"))
            os.system("sudo reboot &")
        elif thisPath[0] == "/run/poweroff":
            self.send_response(200)
            self.wfile.write(bytes('{"html":"Powering off the Raspberry Pi","cmd":null}', "utf-8"))
            os.system("sudo poweroff &")
        else:
            if path.exists("web"+thisPath[0]) is True:
                self.send_response(200)
                fstr = open("web"+thisPath[0],"rb").read()
                self.wfile.write(fstr)                
            else:
                self.send_response(404)
                self.wfile.write(bytes("<p>You accessed path: '%s', is not found on this server</p>" % thisPath[0], "utf-8"))

    #POST is for submitting data.
    def do_POST(self):
        print( "incomming http: ", self.path )
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self.send_response(200)

        client.close()

        #import pdb; pdb.set_trace()


myWebCtrl = HTTPServer((hostName, hostPort), piWebCtrl)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myWebCtrl.serve_forever()
except KeyboardInterrupt:
    pass

myWebCtrl.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))