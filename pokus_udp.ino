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
const char* ssid = "net";
//heslo
const char* pwd = "operationmincemeat1943";

//nastavenie portu
const uint16_t port = 50000;

//nastavenie IP prijmatela
const char * host = "192.168.100.25";

WiFiUDP udp;

void setup(){
  Serial.begin(9600);

  dht.begin();
  
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
  udp.beginPacket(host, port);
  udp.parsePacket();
  byte x = udp.read();
  if(x > 0){
      float h = dht.readHumidity();
      // teplota(Celsius)
      float t = dht.readTemperature();
      //teplota(Fahrenheit)
      float f = dht.readTemperature(true);
      // Read temperature as Fahrenheit (isFahrenheit = true)
      //kvalita vzduchu
      float ppm = gasSensor.getPPM();
      
      if (isnan(h) || isnan(t) || isnan(f)) {
        Serial.println("Failed to read from DHT sensor");
        return;
      }
      else
        Serial.println("vsetko ok");
    
       //data, ktore sa budu posielat na server
      String string = "{\"humidity\":\"" + String(h) + "\",";
      string = string + "\"temperature_C\":\"" + String(t) + "\",";
      string = string + "\"temperature_F\":\"" + String(f) + "\",";
      string = string + "\"ppm\":\"" + String(ppm) + "\"}";
    
      Serial.println(string);
      udp.print(string);
      udp.endPacket();
    
      delay(5000);
  }
}
