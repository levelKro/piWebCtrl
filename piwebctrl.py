#!/usr/bin/python3
import urllib.parse as urlparse
from urllib.parse import parse_qs
import http.server
import socketserver
import os
from os import path

PORT = 9000
PASS = "42758"
WEBPATH = "web"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        pathSplit = self.path.split("?")
        pathSection = pathSplit[0].split("/")
        if self.path == '/':
            self.path = WEBPATH+'/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif path.exists(WEBPATH+pathSplit[0]) is True:
            self.path = WEBPATH+pathSplit[0]
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif pathSection[1] == "run":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if self.getPass(self.path) == PASS:
                if pathSection[2] == "reboot":
                    self.wfile.write(bytes('{"html":"Rebooting the Raspberry Pi","cmd":null}', "utf-8"))
                    os.system("sudo reboot &")
                elif pathSection[2] == "poweroff":
                    self.wfile.write(bytes('{"html":"Powering off the Raspberry Pi","cmd":null}', "utf-8"))
                    os.system("sudo poweroff &")
                else:
                    self.wfile.write(bytes('{"html":"Wrong command","cmd":null}', "utf-8"))
            else:
                self.wfile.write(bytes('{"html":"Wrong password","cmd":null}', "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes('Document requested is not found.', "utf-8"))
        return
        
    def getPass(self,url):
        parsed = urlparse.urlparse("http://localhost"+url)
        return str(parse_qs(parsed.query)['pass']).replace("['","").replace("']","")

handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()