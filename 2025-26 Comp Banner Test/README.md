# 2025-26 Competition Banner Tow Test

`BannerTest-Sensors.ino` contains the program to collect data from the sensors and is made to run off an Arduino Nano. Don't forget to calibrate your sensors!
`BannerTestSch.pdf` contains a schematic of the electrical hardware.

The goal of the test is to experimentally determine the aerodynamic drag created by a banner of varying dimensions, being towed by a small RC aircraft.
The test will consist of the banner in question being towed from a mast erected from a truck (2010 Toyota Tacoma) moving up to 50mph groundspeed. 
In order to simulate typical flight conditions, the banner will be towed from a height such that it is outside the truck's aerodynamic wake region and thus is exposed minimal aerodynamic effects that it would not experience during typical flight.
During this test, the aerodynamic effects of the RC aircraft will be assumed to have a negligibly small impact on the banner and will not be simulated during the test.

Force (F) will be gathered by a load cell to determine the raw drag force from the banner
Airspeed (v) will be gathered by an anemometer to account for differences in ground speed and actual airspeed (wind)
Air humidity, temperature, and pressure will be gathered by an environmental combo sensor for air density (p) calculations

F = 1/2pCAv^2
    => X = CA
  
Author: Joey Ungerleider

Version: 1-27-2026