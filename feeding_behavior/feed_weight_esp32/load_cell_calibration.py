// Calibrating the load cell
#include <Arduino.h>
#include "soc/rtc.h"
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 39;
const int LOADCELL_SCK_PIN = 19;

HX711 penB;

void setup() {
  Serial.begin(115200);
  rtc_cpu_freq_config_t config;
  rtc_clk_cpu_freq_get_config(&config);
  rtc_clk_cpu_freq_mhz_to_config(80, &config);
  rtc_clk_cpu_freq_set_config_fast(&config);
  penB.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
}


void loop() {

  if (penB.is_ready()) {
    penB.set_scale();    
    Serial.println("Tare... remove any weights from the scale.");
    delay(5000);
    penB.tare();
    Serial.println("Tare done...");
    Serial.print("Place a known weight on the scale...");
    delay(5000);
    long reading = penB.get_units(10);
    Serial.print("Result: ");
    Serial.println(reading);
  } 
  else {
    Serial.println("HX711 not found.");
  }
  delay(1000);
}

//calibration factor will be the (reading)/(known weight)
//Calibration factor_PENA = 47473/450 grams
