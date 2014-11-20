
#include <OPC.h>
#include <Bridge.h>
#include <Ethernet.h>
#include <SPI.h>

OPCSerial aOPCSerial;
const int analogInPin = A0; 

float lightValue(const char *itemID, const opcOperation opcOP, const float value) {
  return analogRead(analogInPin);
}

void setup() {
  Serial.begin(9600);

  aOPCSerial.setup();
  aOPCSerial.addItem("lightValue",opc_read,opc_float,lightValue);
}

void loop() {
  aOPCSerial.processOPCCommands();
}

