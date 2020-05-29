//data spracujem do JSON formatu a potom odoslem
#include <ArduinoJson.h>
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
const char* password = "operationmincemeat1943";

//nastavenie portu
const uint16_t port = 8090;

//nastavenie IP prijmatela
const char * host = "192.168.100.16";

StaticJsonDocument<200> message;

void setup() {
  Serial.begin(9600);

  dht.begin();

  //pripojenie ku sieti
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  //IP
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
}
void loop() {

  WiFiClient client;

  if (!client.connect(host, port)) {

        Serial.println("Connection to host failed");

        delay(10000);
        return;
    }

  delay(10000);
  //vlhkost
  float h = dht.readHumidity();
  // teplota(Celsius)
  float t = dht.readTemperature();
  //kvalita vzduchu
  float ppm = gasSensor.getPPM();
  
    Serial.println("Failed to read from DHT sensor");
    return;
  }

  message["humidity"] = h;
  message["temperature"] = t;
  message["ppm"] = ppm;
  
  serializeJsonPretty(message, client);
}
