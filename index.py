#!/usr/bin/python3
# -*- coding: utf-8 -*-
#print("Content-Type: text/html\n\n")

import cgitb
cgitb.enable()
print("Content-Type: text/html;charset=utf-8")
print()
print("Hello World!")

import socket
import json
#from flask import Flask, render_template
import time
#import MySQLdb
import cgi
import unicodedata
import codecs
import sys
from string import Template

s = socket.socket()

s.bind(('0.0.0.0', 8090))
s.listen(0)

while True:

    client, addr = s.accept()

    while True:
        content = client.recv(1024)

        if len(content) == 0:
            break

        else:
            print(content.decode("utf-8"))
            node = json.loads(content.decode("utf-8"))
            print("<p></p>")

            # vlhkost, vytiahnem z json stringu
            humidity = float(node["humidity"])

            # teplota
            temperature = float(node["temperature"])

            # ppm
            ppm = float(node["ppm"])

            # f = open("/file/zapis", "a")
            # f.write(node)
            # f.close()
    
    client.close()
    
html = '''\
<!DOCTYPE html>
<html>
    <title>moje kuzelne zadanie</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<body>
    <h1>Zadanie</h1>
    <p>Hello There!</p>
    <p>General Kenobi!</p>
    <p>$node</p>
</body>
</html>
'''
print(html)

cele = Template(html)
print(cele)

# https://stackoverflow.com/questions/58880873/run-a-python-module-in-a-flask-html-template



