#!/usr/bin/python3
import urllib.parse as urlparse
from urllib.parse import parse_qs
import http.server
import socketserver
import os
import subprocess
from os import path
import json
import psutil
from gpiozero import CPUTemperature


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
        
        elif pathSection[1] == "stats.json":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            outputJson={"ramfree":str(self.get_ramFree())+"MB","ramtotal":str(self.get_ramTotal())+"MB","cpuspeed":str(self.get_cpu_speed())+"MHz","cputemp":str(self.get_temperature())+"°C","cpuuse":str(self.get_cpu_use())+"%","load":str(self.get_load()),"ip":str(self.get_ipaddress()),"uptime":str(self.get_uptime())}
            return self.wfile.write(bytes(json.dumps(outputJson), "utf-8"))
        
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
                elif pathSection[2] == "service":
                    if pathSection[3] == "start" and pathSection[4] is not None:
                        self.wfile.write(bytes('{"html":"Starting the ' + pathSection[4] + ' service.","cmd":null}', "utf-8"))
                        os.system("sudo systemctl start " + pathSection[4])   
                    elif pathSection[3] == "stop" and pathSection[4] is not None:
                        self.wfile.write(bytes('{"html":"Stoping the ' + pathSection[4] + ' service.","cmd":null}', "utf-8"))
                        os.system("sudo systemctl stop " + pathSection[4])
                    elif pathSection[3] == "restart" and pathSection[4] is not None:
                        self.wfile.write(bytes('{"html":"Re-starting the ' + pathSection[4] + ' service.","cmd":null}', "utf-8"))
                        os.system("sudo systemctl restart " + pathSection[4])
                    else:
                        self.wfile.write(bytes('{"html":"Unknown service command","cmd":null}', "utf-8"))
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

    def get_ramTotal(self):
        memory = psutil.virtual_memory()
        return round(memory.total/1024.0/1024.0,1)
        
    def get_ramFree(self):
        memory = psutil.virtual_memory()
        return round(memory.available/1024.0/1024.0,1)       
    
    def get_cpu_use(self):
        return psutil.cpu_percent()

    def get_temperature(self):
        cpu = CPUTemperature()
        return cpu.temperature

    def get_uptime(self):
        try:
            s = subprocess.check_output(["uptime","-p"])
            return s.decode().replace("\n","")
        except:
            return "n/a"

    def get_load(self):
        try:
            s = subprocess.check_output(["uptime"])
            load_split = s.decode().split("load average:")
            return load_split[1].replace("\n","")
        except:
            return "n/a"
    
    def get_ipaddress(self):
        try:
            s = subprocess.check_output(["hostname","-I"])
            return s.decode().replace("\n","")
        except:
            return "0.0.0.0"
    
    def get_cpu_speed(self):
        try:
            f = os.popen('/opt/vc/bin/vcgencmd get_config arm_freq')
            cpu = f.read()
            if cpu != "":
                return cpu.split("=")[1].replace("\n","")
            else:
                return "n/a"
        except:
            return "n/a"

handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()