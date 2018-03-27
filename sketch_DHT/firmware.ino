#include <mlx90615.h>

#include "DHT.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include <Ethernet.h>

byte mac[] = { 0x70, 0x5A, 0x0F, 0x4D, 0x73, 0x6C };
String message = "";
double t_ir, t_amb, t_sky,  h; 
double flux = -1.0;
IPAddress server(172,27,76,59); 
EthernetClient client;


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
  //Ethernet.begin(mac);
  delay(1000);
  Serial.println("connecting...");

  //if (client.connect(server, 8765)) {
  //Serial.println("connected");
  //  } else {
  //Serial.println("connection failed");
  //}
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
  message = "";
  sensors_event_t event;
  tsl.getEvent(&event);
 
  if (event.light)
  {
   flux = event.light;
   }
  else
  {
    flux = 0;
    }
  h = dht.readHumidity();
  t_amb = dht.readTemperature();
  t_ir = mlx.get_ambient_temp();
  t_sky = mlx.get_object_temp();
  if (isnan(h) || isnan(t_amb)) {
    Serial.println("Failed to read from DHT sensor!");
  }
  message.concat(flux);
  message.concat(" ");
  message.concat(h);
  message.concat(" ");
  message.concat(t_sky);
  message.concat(" ");
  message.concat(t_ir);
  message.concat(" ");
  message.concat(t_amb);
  //client.print(message);
  Serial.println(message);
}


