from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import MySQLdb
import socket
import ConfigParser
import json

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

# pripojenie do databazy
db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)

# otvorenie suboru
try:
    f = open("/home/pi/Documents/poit/zadanie/file/record/txt",'a')
except IOError:
    print("Chyba pri otvarani suboru")

def background_thread(args):
    while True:
        try:
            data, addr = s.recvfrom(1024)
            print("received message %s" % data)
            node = json.loads(data.decode("utf-8"))          
            print(node)
            
            #zapis do suboru
         #   f.write("%s\r\n" %node)
            
            # vlhkost
            humidity = float(node['humidity'])
            # teplota(C)
            temperatureC = float(node['temperature(C)'])
            #teplota(F)
            temperatureF = float(node['temperature(F)'])
            #ppm
            ppm = float(node['ppm'])
            
            #zapis do databazy
            cursor = db.cursor()
            sql_zapis = "INSERT INTO data (temperatureC, temperatureF, humidity, ppm) VALUES ('%s', '%s', '%s', '%s')"
            cursor.execute(sql_zapis, (temperatureC, temperatureF, humidity, ppm))
            db.commit()
            # posielam klientovi opat JSON, aj ked to neni prave najefektivnejsie, aby sa parsoval dvakrat
            socketio.emit('json_data', {'data': data}, namespace='/')  
        except socket.timeout:
            pass
    
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('start_stop_request', namespace='/senzory')
def start_stop(message):
    global thread
    if message['value'] == 'start':
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    if message['value'] == 'stop':
        disconnect()    

# po nadviazani spojenia presmerovat na stranku, kde sa to da spustat a vypinat, po stlaceni disconnect spat na uvodnu stranku s jednym tlacidlom
@app.route('/', methods=['GET', 'POST'])
@socketio.on('connect')
def connect():
    # nastavenie socketov
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 50000))
    s.settimeout(2.5)
    message =b"1"
    print("message: %s" % message)
    s.sendto(message,('192.168.100.24',50000))
    global data, addr   
    # pridat aj kontrolu pripojenia
    return render_template('senzory.html', async_mode=socketio.async_mode)
            
@socketio.on('disconnect', namespace='/senzory')
def disconnect():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message =b"0"
    print("message: %s" % message)
    s.sendto(message,('192.168.100.24',50000))
    print('Client disconnected', request.sid)
    return render_template('index.html', async_mode=socketio.async_mode)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)