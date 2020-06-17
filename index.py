from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import MySQLdb
import socket
import ConfigParser
import json
import os

async_mode = None

app = Flask(__name__)

# nacitanie suboru s prihlasovacimi udajmi a adresou do nasej databazy
config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
thread2 = None
thread2_lock = Lock()

def background_thread(args):
    global data, addr  
    
    while flag > 0:
        try:
            data, addr = s.recvfrom(1024)
            print("received message %s" % data)
            node = json.loads(data.decode("utf-8"))          
            # vlhkost
            humidity = float(node['humidity'])
            # teplota(C)
            temperatureC = float(node['temperature_C'])
            #teplota(F)
            temperatureF = float(node['temperature_F'])
            #ppm
            ppm = float(node['ppm'])
            
            #zapis do databazy
            cursor = db.cursor()
            sql_zapis = "INSERT INTO data (temperatureC, temperatureF, humidity, ppm) VALUES ('%s', '%s', '%s', '%s')"     
            cursor.execute(sql_zapis, (temperatureC, temperatureF, humidity, ppm))
            db.commit()

            # otvorenie suboru
            try:
                if os.path.exists("/home/pi/Documents/poit/zadanie/file/record.txt"):
                    f = open("/home/pi/Documents/poit/zadanie/file/record.txt",'a')
                else:
                    f = open("/home/pi/Documents/poit/zadanie/file/record.txt",'w')
            except IOError:
                print("Chyba pri otvarani suboru")
                
            f.write(data)
            f.write("\n")
            f.close()
          
            # posielam klientovi opat JSON, aj ked to neni prave najefektivnejsie, aby sa parsoval dvakrat
            socketio.emit('json_data', {'data': data}, namespace='/')
        except:
            pass

def connection_thread():
    while 1:
        message =b"1"
        print("message: %s" % message)
        s.sendto(message,('192.168.100.24',50000))
        
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('start_stop_request')
def start_stop(message):
    global thread, flag
    if message['value'] == 'start':
        print("Henlo")
        flag = 1
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    if message['value'] == 'stop':
        flag = 0
        thread = None
           
@socketio.on('disconnect_request')
def disconnect_request(): 
    message =b"0"
    s.sendto(message,('192.168.100.24',50000))
    print('Client disconnected')
    thread2 = None
    disconnect()

@socketio.on('connect_request')
def connect_request():
    global s, db, f
    # socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # pripojenie do db
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    s.bind(('', 50000))
    s.settimeout(0.5)
    with thread2_lock:
        if thread is None:
            thread2 = socketio.start_background_task(target=connection_thread)
    
@socketio.on('delete_request')
def delete_request():
    cursor = db.cursor()
    sql = "DELETE FROM data"
    cursor.execute(sql)
    db.commit()

@socketio.on('delete_request_file')
def delete_request_file():
    if os.path.exists("/home/pi/Documents/poit/zadanie/file/record.txt"):
        os.remove("/home/pi/Documents/poit/zadanie/file/record.txt")
        
@socketio.on('load_request')
def load_request():
    cursor = db.cursor()
    sql = "SELECT temperatureC, temperatureF, humidity, ppm FROM data"
    cursor.execute(sql)
    result = cursor.fetchall()
  #  send_result = json.dumps(result)
    socketio.emit('db_data', {'data': result}, namespace='/')
    
@socketio.on('load_request_file')
def load_request_file():
    try:
        if os.path.exists("/home/pi/Documents/poit/zadanie/file/record.txt"):
            f = open("/home/pi/Documents/poit/zadanie/file/record.txt",'r')
    except IOError:
        print("Chyba pri otvarani suboru")
            
    with open("/home/pi/Documents/poit/zadanie/file/record.txt",'r') as openfileobject:
        for line in openfileobject:
            result = f.readline()
            socketio.emit('file_data', {'data': result}, namespace='/')
    f.close()
         
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)