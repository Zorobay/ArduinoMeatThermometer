# Meat Thermometer Project

## Lingo

* ADC: Analog / Digital Converter (Is used when `analogRead()` is called)

## ESP32

### Pins used

| Pin | Label | Used for |
|---|---|---|
| 3V | 3V | Power to display VCC |
| GND | GND | Ground for display and thermistor |
| 18 | MO | Display DIN (SPI data) |
| 5 | SCK | Display CLK (SPI clock) |
| 27 | 27 | Display D/C |
| 15 | 15 | Display RES |
| 33 | 33 | Display CS |
| 34 | A2 | Thermistor analog input |