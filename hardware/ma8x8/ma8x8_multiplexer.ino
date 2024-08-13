#include <Adafruit_MCP23X17.h>

Adafruit_MCP23X17 mcp[] = {
  Adafruit_MCP23X17(),
  Adafruit_MCP23X17(),
  Adafruit_MCP23X17(),
  Adafruit_MCP23X17()
};

int hw_addr[] = {
  0x20,
  0x21,
  0x22,
  0x23
};

int x;
int n;
int p;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 4; i++) {
    if (!mcp[i].begin_I2C(hw_addr[i])) {
      Serial.println("Error.");
      while (1);
    }
    for (int k = 0; k < 16; k++) {
      mcp[i].pinMode(k, OUTPUT); 
    }
    mcp[i].writeGPIO(LOW, 0);
    mcp[i].writeGPIO(LOW, 1);
  }
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  if (x < 1 || x > 64) {
    for (int i = 0; i < 4; i++) {
      mcp[i].writeGPIO(LOW, 0);
      mcp[i].writeGPIO(LOW, 1);
    }
    Serial.println('0');
  } else {
    n = (x - 1) / 16;
    p = x - (16 * n) - 1;
    for (int i = 0; i < 4; i++) {
      mcp[i].writeGPIO(LOW, 0);
      mcp[i].writeGPIO(LOW, 1);
    }
    mcp[n].digitalWrite(p, HIGH);
    Serial.println('1');
  }
}
