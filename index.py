#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import cgitb
import cgi
cgitb.enable()
print("Content-Type: text/html; charset=utf-8\n\n")
import threading
import socket
#import pymysql
#import pymysql.cursors
import json
#import requests
from flask import Flask
from flask_mysqldb import MySQL
#import werkzeug

worker = None

app = Flask(__name__)

@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)


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
           # print(node)
            
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
                
            
            #chcelo by to spravit ako samostatnu funkciu, ale nejde. To by connection variable musela byt globalna
            #dat if else na Celius alebo fahrenheit, podla toho sa spravi select
            # mozno sa v plotly da posielat viac udajov a potom len checkboxom vybrat to, co chceme, to by bolo pekne(teraz rozdiel medzi C a 
            
            cur = connection.cursor()
            # Read a single record
            sql_select = "SELECT * FROM data WHERE id = ( SELECT MAX(id) FROM data )"
            cur.execute(sql_select)
            result = cur.fetchone()
            print(result)
            return jsonify(result)
               
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
        
    #pridat vyber medzi Celsius a Fahrenheit

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
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript">
$(document).ready(function()
{ 
     $("#start").click(myFunction);

});

function myFunction()
{

$.ajax({
    url: "index.py",
    type: "GET",
    success: function(data) {
            console.log("This is the returned data: " + JSON.stringify(data));
    },
    error: function(error){
            console.log("Here is the error res: " + JSON.stringify(error));
    }
 });
}
</script>
<body>
    <h1>Zadanie</h1>
    <p>Hello There!</p>
    <p>General Kenobi!</p>
    <button type="button" id="start">Celsius</button> 
    <p>$node</p>
</body>
</html>
'''
print(html)

if name == 'main':
    app.run(debug=True)
