//kniznica pre dht senzor(teplota a vlhkost)
#include "DHT.h"
//kniznica pre mq senzor(kvalita vzduchu)
#include "MQ135.h"

DHT dht(33, DHT11);

const int DGPIN=33;
MQ135 gasSensor = MQ135(DGPIN);

void setup() {
  Serial.begin(9600);

  dht.begin();
}
void loop() {

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
