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
import json

worker = None

def socket_worker():
    # pripojenie do databazy
    connection = pymysql.connect(host='localhost', user='adamko', password='FCST1923', db='zadanie', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    # otvorenie suboru  
    try:
        f = open("/var/www/html/cgi-enabled/file/record.txt", "w")
    except IOError:
        print("chyba pri otvarani suboru")

 #       with connection.cursor() as cursor:
#            # Read a single record
#            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#            cursor.execute(sql, ('webmaster@python.org',))
 #           result = cursor.fetchone()
#            print(result)
    
    
    #while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 50000))
    s.settimeout(0.5)
    global data, addr
    
    while True:              
        try:
            data, addr = s.recvfrom(1024)
            node = json.loads(data.decode("utf-8"))
            print(node)
            
            #zapis do suboru
      #      f.write(str(Node))
            f.write("ahoj")
            
            # vlhkost, vytiahnem z json stringu
            humidity = float(node['humidity'])
            
             # teplota(C)
            temperatureC = float(node["temperature(C)"])
            
             # teplota(F)
            temperatureF = float(node["temperature(F)"])

            # ppm
            ppm = float(node["ppm"])
            
            with connection.cursor() as cursor:
                # zapis do db
                sql = "INSERT INTO data (temperatureC, temperatureF, humidity, ppm) VALUES ('%s', '%s', '%s', '%s')"
                cursor.execute(sql, (temperatureC, temperatureF, humidity, ppm))
                connection.commit()
                
                # dopplnit button, ktory vysle signal, aby sme vyskocili z cyklu
                
        except :
            pass
    
    # spytat sa, preco mi nejde zatvorit suboru a tym padom aj ulozit udaje
    f.close()
    print(f.closed)
    print("zatvaram subor")
    # ukoncenie zapisu do db
    connection.close()
    
def start_worker():
    global worker
    worker = threading.Thread(target=socket_worker)
    worker.daemon = True
    worker.start()
    
def open():
    
    #pridat vyber medzi Celsius a Fahrenheit
    
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)

# sem dopisat strukturu web stranky a pushnut to do browseru
print("henlo\n")
print("before worker\n")


# pridat button na premazanie dat, to by bola fajn vec navyse

#pridat button na vypisanie najvyssej nameranej teploty alebo vlhkosti

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


