# Raspberry Pi E-Paper Bus and Weather Display

Developed to alleviate the inconvenience of waiting for Iowa State CyRide buses in harsh weather conditions, this project showcases a Raspberry Pi Zero-based system paired with a 2.9-inch E-paper screen to display bus arrival times and current weather conditions. Note: It has ran for 7 months with-out problems.

## Description

This Python script fetches real-time bus arrival data and weather information, displaying it on an E-paper display. The system uses GET requests to retrieve data from public APIs, parses the JSON responses, and updates the display with the relevant information. The project also involved significant customization of the E-paper driver to ensure compatibility. The Script Runs on a Raspberry Pi system Service.

## Features

- **Real-time Bus Arrival Times:** Displays arrival times for Iowa State CyRide buses.
- **Current Weather Information:** Shows current temperature and weather conditions.
- **Date and Time Display:** Displays the current date and time.
- **Custom Enclosure:** 3D printed enclosure designed in Autodesk Inventor for the screen and Raspberry Pi.

## Example Output

- **Bus Arrival Times:**
  - "Cherry in 2 mins (2:42 PM)"
  - "Red in 5 mins (2:40 PM)"
  
- **Weather Information:**
  - "Temp: 75°F"
  - "Condition: Sunny"
  
- **Date and Time:**
  - "Thu, 20th"
  - "10:30 AM"

## E-Paper Drivers

- I found the provided drives from the manufacturer for me screen to be faulty. The Project was orginally designed to be made using a ESP32, but I could not get the display to function correctly.
- The Drivers for Rasberry Pi were better, but in the end needed to be modified slightly to ensure relibility.

##Image
![image](https://github.com/luke-schwieters/Bus-Arrival-Display/assets/82103885/4c7b8df7-0ad8-4514-9099-23cffbd875ff)
