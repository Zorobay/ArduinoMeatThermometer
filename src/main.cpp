#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>

#define OLED_DIN 18
#define OLED_CLK 5
#define OLED_DC 27
#define OLED_RES 15
#define OLED_CS 33

#define THERM_PIN 34 // A2

Adafruit_SSD1306 display(128, 64,
                         OLED_DIN, OLED_CLK, OLED_DC, OLED_RES, OLED_CS);

void setup()
{
  display.begin(SSD1306_SWITCHCAPVCC);
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 24);
  // display.println("Hello!");
  // display.display();

  Serial.begin(115200);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
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