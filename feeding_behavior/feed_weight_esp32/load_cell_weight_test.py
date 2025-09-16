#include <Arduino.h>
#include "HX711.h"
#include "soc/rtc.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 36;
const int LOADCELL_SCK_PIN = 21;

HX711 penB;

void setup() {
  Serial.begin(115200);
  rtc_cpu_freq_config_t config;
  rtc_clk_cpu_freq_get_config(&config);
  rtc_clk_cpu_freq_mhz_to_config(80, &config);
  rtc_clk_cpu_freq_set_config_fast(&config);
  Serial.println("HX711 Demo");

  Serial.println("Initializing the scale");

  penB.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  Serial.println("Before setting up the scale:");
  Serial.print("read: \t\t");
  Serial.println(penB.read());      // print a raw reading from the ADC

  Serial.print("read average: \t\t");
  Serial.println(penB.read_average(20));   // print the average of 20 readings from the ADC

  Serial.print("get value: \t\t");
  Serial.println(penB.get_value(5));   // print the average of 5 readings from the ADC minus the tare weight (not set yet)

  Serial.print("get units: \t\t");
  Serial.println(penB.get_units(5), 1);  // print the average of 5 readings from the ADC minus tare weight (not set) divided
            // by the SCALE parameter (not set yet)
            
  penB.set_scale(218.42);
  //scale.set_scale(-471.497);                      // this value is obtained by calibrating the scale with known weights; see the README for details
  penB.tare();               // reset the scale to 0

  Serial.println("After setting up the scale:");

  Serial.print("read: \t\t");
  Serial.println(penB.read());                 // print a raw reading from the ADC

  Serial.print("read average: \t\t");
  Serial.println(penB.read_average(20));       // print the average of 20 readings from the ADC

  Serial.print("get value: \t\t");
  Serial.println(penB.get_value(5));   // print the average of 5 readings from the ADC minus the tare weight, set with tare()

  Serial.print("get units: \t\t");
  Serial.println(penB.get_units(5), 1);        // print the average of 5 readings from the ADC minus tare weight, divided
            // by the SCALE parameter set with set_scale

  Serial.println("Readings:");
}

void loop() {
  float weight = penB.get_units(10); //RMS VALUE FOR PEN A; 
  Serial.print("one reading:\t");
  Serial.print(penB.get_units(), 1);
  Serial.print("\t| average:\t");
  Serial.println(weight, 10);

  penB.power_down();    // put the ADC in sleep mode
  delay(5000);
  penB.power_up();
}

//PEN A
//Calibration factor = 224.727
//weight = penA.get_units(10) - 11.86
//const int LOADCELL_DOUT_PIN = 36;
//const int LOADCELL_SCK_PIN = 21;

//PEN B
//Calibration factor = 219.749
//weight = 
//const int LOADCELL_DOUT_PIN = 39;
//const int LOADCELL_SCK_PIN = 19;

//PEN C

//PEN D
