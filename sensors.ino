//kniznica pre dht senzor(teplota a vlhkost)
#include "DHT.h"
//kniznica pre mq senzor(kvalita vzduchu)
#include "MQ135.h"
//kniznica na bezdrotove pripojenie
#include <WiFi.h>

DHT dht(33, DHT11);

const int DGPIN=33;
MQ135 gasSensor = MQ135(DGPIN);

//nazov mojej bezdrotovej siete
const char* ssid = "net";
//heslo
const char* password = "operationmincemeat1943";

//nastavenie portu (80)
WiFiServer server(80);

String header;



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
  server.begin();
  
}
void loop() {

  WiFiClient client = server.available();

  delay(5000);
  //vlhkost
  float h = dht.readHumidity();
  // teplota(Celsius)
  float t = dht.readTemperature();
  
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor");
    return;
  }

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print("%  Temperature: ");
  Serial.print(t);
  Serial.print("°C ");
  
  //kvalita vzduchu
  float ppm = gasSensor.getPPM();
  Serial.print(" ppm: ");
  Serial.println(ppm);

}
