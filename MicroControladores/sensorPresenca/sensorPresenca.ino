#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "wi-fi";
const char* password = "senha";

WiFiUDP Udp;
unsigned int localUdpPort = 4210;  // local port to listen on

#include <OSCBundle.h>

void setup()
{
  pinMode (5, INPUT);
  digitalWrite(5, LOW);
  
  Serial.begin(115200);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");

  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
}


//=======================================================================================
// Loop do Programa
//=======================================================================================

void loop()
{ 
  int sensor = digitalRead(5);
  
  if (digitalRead(5))
  {
    Serial.println("SIM");
  }
  else
  {
    Serial.println("NÃO");
  }

  OSCMessage mensagem("/buzu/sensor");
  mensagem.add(sensor);
  Udp.beginPacket("192.168.0.255", 6660);
  mensagem.send(Udp);
  Udp.endPacket();
  mensagem.empty();
  delay(1200);
}
