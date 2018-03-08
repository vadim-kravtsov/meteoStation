#include <mlx90615.h>

#include "DHT.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>

#define DHTPIN 2     // what digital pin we're connected to
#define SDA_PIN 20   //define the SDA pin
#define SCL_PIN 21   //define the SCL pin
#define DHTTYPE DHT22
 

DHT dht(DHTPIN, DHTTYPE);
MLX90615 mlx = MLX90615();
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);

void setup()
{
  Serial.begin(9600);
  dht.begin();
  tsl.begin();
  mlx.begin();
  sensor_t sensor;
  tsl.getSensor(&sensor);
  tsl.enableAutoRange(true); 
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);
  //Serial.println("Flux Humidity SkyT AmbT InsideT");
  }

void loop()
{
  delay(1000);
  sensors_event_t event;
  tsl.getEvent(&event);
 
  if (event.light)
  {
   Serial.print(event.light);
   Serial.print(" ");
  }
  else
  {
    Serial.println("Sensor overload");
  }
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  Serial.print(h);
  Serial.print(" ");
  Serial.print(mlx.get_object_temp()); 
  Serial.print(" ");
  Serial.print(t);
  Serial.print(" ");
  Serial.println(mlx.get_ambient_temp());
}


