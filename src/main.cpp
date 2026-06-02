#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>
#include <math.h>

#define OLED_DIN 18
#define OLED_CLK 5
#define OLED_DC 27
#define OLED_RES 15
#define OLED_CS 33

#define THERM_PIN 34 // A2 on the ESP32

#define R_FIXED = 100000

Adafruit_SSD1306 display(128, 64,
                         OLED_DIN, OLED_CLK, OLED_DC, OLED_RES, OLED_CS);


void initDisplay() {

  /*
  OLED displays need a higher voltage internally (around 7-9V) to drive the pixels, even though they're powered from 3.3V. 
  The SSD1306 chip has a built-in circuit called a charge pump that steps the voltage up internally — SWITCHCAPVCC tells it to use that internal charge pump.
  */
  display.begin(SSD1306_SWITCHCAPVCC);
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
}

void initSerial() {
  // Start serial communication at 115200 baud for debug output (configured in platformio.ini)
  Serial.begin(115200);
  // Set ADC to 12-bit resolution (readings from 0 to 4095)
  analogReadResolution(12);
  // Set ADC input range to 0-3.3V (default is 0-1V)
  analogSetAttenuation(ADC_11db);
}

void setup()
{
  initSerial();
  initDisplay();
}

/*
Uses Steinhart-Hart equation to estimate temperature from resistance
*/
float calcTemperature(int R, float A, float B, float C) {
  float denom = A + B * log(R) + C * pow(log(R), 3);
  return 1 / denom;
}

void loop()
{
  int raw = analogRead(THERM_PIN);
  Serial.println(raw);

  display.clearDisplay();
  display.setCursor(0, 24);
  display.println(raw);
  display.display();

  delay(500);
}