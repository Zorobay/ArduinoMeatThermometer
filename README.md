# Meat Thermometer Project

## Lingo

* ADC: Analog / Digital Converter (Is used when `analogRead()` is called)

## Temperature Probe

The temperature probe is an NTC (Negative Temperature Coefficient) Thermistor. The resistance goes down as temperature goes up. At room temperature the thermistor is approximately 20kΩ.

![](docs/meat_thermometer.jpg)

## ESP32

### Pins used

| Pin | Label | Used for                          |
| --- | ----- | --------------------------------- |
| 3V  | 3V    | Power to display VCC              |
| GND | GND   | Ground for display and thermistor |
| 18  | MO    | Display DIN (SPI data)            |
| 5   | SCK   | Display CLK (SPI clock)           |
| 27  | 27    | Display D/C                       |
| 15  | 15    | Display RES                       |
| 33  | 33    | Display CS                        |
| 34  | A2    | Thermistor analog input           |

## Digital reading to temperature conversion

### Voltage divider at pin A2

The voltage divider created at A2 should read a voltage $V_{out}$ according to the formula:

$$
V_{out} = V_{in} \frac{R_2}{R_{1}R_{2}}
$$

where $V_{in}$ is our input voltage (3.3V), $R_1$ is the fixed 100kΩ resistor and $R_2$ is the voltage from our thermistor.

### ADC integer to voltage to resistance

In order to estimate a temperature from the probe, we need to calculate the resistance. This is not known by the program, but the digital integer value is, so we have to work backwards:

$$
R_2 = R_1\frac{V_{out}}{V_{in}-V_{out}}
$$

But since we are working with digital values, $V_{in}$, being 3.3V is equivalent to the highest digital value of 4095, lets call it $ADC_{max}$. $R_1$ is also known, 100kΩ and finally we get $V_{out}$ from reading the pin using `analogRead(THERM_PIN)`, let's call it $ADC_{therm}$.

$$
R_2 = R_{100k}\frac{ADC_{therm}}{ADC_{max}-ADC_{therm}}
$$

### Converting resistance to temperature