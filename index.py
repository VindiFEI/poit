#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgitb
import cgi
cgitb.enable()
print("Content-Type: text/html; charset=utf-8\n\n")
import threading
import socket
import pymysql
import pymysql.cursors

worker = None

def socket_worker():
    
    connection = pymysql.connect(host='localhost', user='adamko', password='FCST1923', db='zadanie', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO data (temperature, humidity, ppm) VALUES ('%s', '%s', '%s')"
            cursor.execute(sql, (float(20), float(20), float(40)))
            connection.commit()

 #       with connection.cursor() as cursor:
#            # Read a single record
#            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#            cursor.execute(sql, ('webmaster@python.org',))
 #           result = cursor.fetchone()
#            print(result)
    finally:
        connection.close()
    
    #while True: #tuto vyriesit pisanie do databazy, nieco na styl nekonecny cyklus caka na data zo socketu a vzdy ked pridu, tak vykona insert. Ked data pridu s rozumnym odstupom, napr 1sec, tak by to malo byt thread safe
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 50001))
    s.settimeout(0.5)
    global data, addr
    while True:
        try:    
            data, addr = s.recvfrom(1024)
            node = json.loads(data.decode("utf-8"))
            
            print(str(data.decode()) + " " + str(addr))
        except:
            pass

def start_worker():
    global worker
    worker = threading.Thread(target=socket_worker)
    worker.daemon = True
    worker.start()

# sem dopisat strukturu web stranky a pushnut to do browseru
print("henlo\n")
print("before worker\n")

# start worker by mal byt pusteny cez button
start_worker()#!/usr/bin/python3
# -*- coding: utf-8 -*-

# system("pkill -9 python")

#import socket
#import json
#from flask import Flask, render_template
#import time
#import MySQLdb
#import cgi
#import unicodedata
#import codecs
#import sys
#from string import Template
# from receiver import receiver
#import logging
#from _thread import *

#udp_port = 50001
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # nech zere IP addr v intoch, udp
#sock.bind(("0.0.0.0", udp_port))
#sock.settimeout(0.1)
#data = "" # globalka na ukladanie prichadzajucich dat
#addr = "" # globalka na ukladanie odkial to ide
...
# nekonecny cyklus na pozadi, cize v threade
#def socket_worker():
#    while True:
 #       try:
  #          global data, addr
   #         data, addr = sock.recvfrom(1024)
    #        write(str(data.decode()) + " " + str(addr))
     #   except socket.timeout:
      #      write("no data recv")
       # time.sleep(2)


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


#while True:

#    client, addr = s.accept()
    
#    print('Connected with ' + addr[0] + ':' + str(addr[1]))

 #   while True:
      #  content = client.recv(1024)

     #   if len(content) == 0:
      #      break

    #    else:
        #    print(content.decode("utf-8"))
         #   node = json.loads(content.decode("utf-8"))
         #   print("<p></p>")

            # vlhkost, vytiahnem z json stringu
         #   humidity = float(node["humidity"])

            # teplota
          #  temperature = float(node["temperature"])

            # ppm
          #  ppm = float(node["ppm"])

            # f = open("/file/zapis", "a")
            # f.write(node)
            # f.close()
    
  #  client.close()




#cele = Template(html)
#print(cele)


