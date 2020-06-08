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

# Problemy :
# 1. start/stop - Na stlacenie buttonu sa to spusti, na druhe(stop) to uz nefunguje skusil som nastavit nejaku flag, ktora by mala hodnoty 1 a 0 a podla nej by sa urcovalo, ci sa
# spusti cyklus alebo nie. Fungovalo to na zastavenie, ale ked som opatovne stlacil start, aby sa nastavila
# na jednotku, tak uz to neslo.

# 2. vobec nejde disconnect, ja nechapem preco. Je tam prikaz disconnect a vobec to na to nereaguje

# 3. neni som si isty, ci bude treba aj zastavovat vystup z mojej dosky, alebo nie. Ale ukazuje sa to ako komplikovanejsie,
# nez som predpokladal. Dokazem odoslat na dosku 1(mozno pojde aj nula, ak rozbeham funkciu disconnect_request(), ale ako problem sa javi
# ze ten vypis tam prebieha v cykle, on prijme paketu s jednotkou len raz, to znamena, ze dostane len raz prikaz na vykonanie odoslania nameranych
# dat, vo zvysnych pripadoch uz ma nulu a vysielanie prestane. Ak to bude treba spravit, tak mi napada jedine, ze smerom na dosku bude potrebne odosielat
# nepretrzite bud 1(posielaj) alebo 0(bud uz konecne ticho). Ine mi nenapada, neni som nejaky programator

# 4. Stale sa mi nedari pisat do suboru, asi to bude tym, ze nejde funkcia disconnect_request(), kde je f.close(). Pravdepodobne sa vtedy ulozia vsetky zmeny suboru,
# ak sa funkcia close nevykona, subor ostane aky bol.




def background_thread(args):
    global data, addr  
    
    while flag > 0:
        try:
            data, addr = s.recvfrom(1024)
            print("received message %s" % data)
            node = json.loads(data.decode("utf-8"))          
            
            #zapis do suboru
          #  f.write("%s\n" %node)
            
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
            # posielam klientovi opat JSON, aj ked to neni prave najefektivnejsie, aby sa parsoval dvakrat
            socketio.emit('json_data', {'data': data}, namespace='/')
        except:
            pass
    
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('start_stop_request')
def start_stop(message):
    global thread, flag
    if message['value'] == 'start':
        flag = 1
        # otvorenie suboru
        try:
            f = open("/home/pi/Documents/poit/zadanie/file/record.txt",'a')
        except IOError:
            print("Chyba pri otvarani suboru")
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    if message['value'] == 'stop':
       # f.close()
        flag = 0
           
@socketio.on('disconnect')
def disconnect_request(): 
    message =b"0"
    s.sendto(message,('192.168.100.24',50000))
    print('Client disconnected')
    disconnect()

@socketio.on('connect')
def connect_request():
    global s, db, f
    # socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # pripojenie do db
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    s.bind(('', 50000))
    s.settimeout(0.5)
    message =b"1"
    print("message: %s" % message)
    s.sendto(message,('192.168.100.24',50000))

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)