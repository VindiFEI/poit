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
    # pripojenie do databazy
    connection = pymysql.connect(host='localhost', user='adamko', password='FCST1923', db='zadanie', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO data (temperature, humidity, ppm) VALUES ('%s', '%s', '%s')"
            cursor.execute(sql, (float(18), float(22), float(41)))
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
    s.bind(('0.0.0.0', 50000))
    s.settimeout(0.5)
    global data, addr
    while True:
        try:
            data, addr = s.recvfrom(1024)
            print(addr)
            print(data.decode("utf-8"))
            node = json.loads(data.decode("utf-8"))
            print(node)
            
            print(str(data.decode()) + " " + str(addr[1]))
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

# pridat button na premazanie dat, to by bola fajn vec navyse

# start worker by mal byt pusteny cez button
start_worker()

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


