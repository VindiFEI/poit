//kniznica pre dht senzor(teplota a vlhkost)
#include "DHT.h"
//kniznica pre mq senzor(kvalita vzduchu)
#include "MQ135.h"
//kniznica na bezdrotove pripojenie
#include <WiFi.h>

DHT dht(33, DHT11);

const int DGPIN=32;
MQ135 gasSensor = MQ135(DGPIN);

//nazov mojej bezdrotovej siete
const char * ssid = "net";
const char * pwd = "operationmincemeat1943";

//nastavenie portu
const uint16_t port = 50000;

//nastavenie IP prijmatela
const char * host = "192.168.100.16";

//create UDP instance
WiFiUDP udp;

void setup(){
  Serial.begin(115200);
  
  //pripojenie ku sieti
   WiFi.begin(ssid, pwd);
  Serial.println("");

  //cakanie na pripojenie
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Conected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  //inicializacia udp
  udp.begin(port);
}

void loop(){
  
  delay(5000);
  //vlhkost
  float h = dht.readHumidity();
  // teplota(Celsius)
  float t = dht.readTemperature();
  //kvalita vzduchu
  float ppm = gasSensor.getPPM();

  //kontrola udajov z dht
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor");
    return;
  }
  else
    Serial.println("Everything's okay for now");

   //data, ktore sa budu posielat na server
  String string = "{\"humidity\":\"" + String(h) + "\",";
  string = string + "\"temperature\":\"" + String(t) + "\",";
  string = string + "\"ppm\":\"" + String(ppm) + "\"}";

  udp.beginPacket(host, port);
  Serial.println(string);
  udp.print(string);
  udp.endPacket();
//  memset(buff, 0, 50);
  //processing incoming packet, must be called before reading the buffer
//  udp.parsePacket();
  //receive response from server, it will be HELLO WORLD
/*  if(udp.read(buffer, 50) > 0){
    Serial.print("Server to client: ");
    Serial.println((char *)buffer);
  }*/
  //Wait for 1 second
  delay(1000);
}
