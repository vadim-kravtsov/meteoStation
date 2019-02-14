#include <TroykaMeteoSensor.h>

#include <mlx90615.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include <Ethernet.h>

byte mac[] = { 0x70, 0x5A, 0x0F, 0x4D, 0x73, 0x6C };
byte ip[] = { 192, 168, 1, 41 };    
String message = "";
String comment = "";
double t_ir, t_out, t_sky, h_out; 
double flux = -1.0;
int DO_RESET_ETH_SHIELD = 5;
int state; 
int numbOfFails = 0;
IPAddress server(172,27,76,59);
//IPAddress server(195,19,241,156);
EthernetClient client;


#define SDA_PIN 20   //define the SDA pin
#define SCL_PIN 21   //define the SCL pin
void itit_ethernet(void);
    
MLX90615 mlx = MLX90615();
TroykaMeteoSensor tms;

void setup(){
  delay(1000);
  //Serial.begin(9600);
  //Serial.println("connecting...");
  init_ethernet();
  //Serial.println("all ok...");
  Ethernet.begin(mac);
  delay(5000);
  while (client.connect(server, 8765)!=0) {
  Serial.println("connecting...");
  }
  //Serial.println("serial");
  mlx.begin();
  tms.begin();
  //Serial.println("H_out T_out H_in T_in T_ir T_sky");
  }

void loop(){
  delay(30000);
  if (client.connected()){
    message = "";
    //comment = "";
    
    state = tms.read();
   
    if (state == 0){
        h_out = tms.getHumidity();
        t_out = tms.getTemperatureC();
        //comment.concat("#TroykaMeteoSensor is OK");
        //client.print(comment);
        //Serial.print(comment);
    }
    t_ir = mlx.get_ambient_temp();
    t_sky = mlx.get_object_temp();
    if (t_ir>300 || isnan(t_out)) {
          //Serial.println("Failed to read from sensors!");
          return;
      } 
    else {
          message.concat(h_out);
          //message.concat(h_in);
          message.concat(" ");
          message.concat(t_out);
          message.concat(" ");
          message.concat(h_out);
          message.concat(" ");
          message.concat(t_out);
          message.concat(" ");
          message.concat(t_ir);
          message.concat(" ");
          message.concat(t_sky);
    }  
  client.print(message);
  numbOfFails = 0;
  //Serial.println(message);
  } else {  
      //Serial.println("kjhgkjhg");
      numbOfFails = numbOfFails + 1;
      client.stop();
      delay(500);
      client.connect(server, 8765);
      client.print(message);
      if (numbOfFails > 5){
        init_ethernet();
        }
    }
  }

void init_ethernet(void)
{
 //Serial.print("reset...");
 numbOfFails = 0;
 pinMode(DO_RESET_ETH_SHIELD, OUTPUT);      // sets the digital pin as output
 digitalWrite(DO_RESET_ETH_SHIELD, LOW);
 delay(1000);  //for ethernet chip to reset
 digitalWrite(DO_RESET_ETH_SHIELD, HIGH);
 delay(1000);  //for ethernet chip to reset
 pinMode(DO_RESET_ETH_SHIELD, INPUT);      // sets the digital pin input
 delay(1000);  //for ethernet chip to reset
 Ethernet.begin(mac);
 delay(1000);
}
