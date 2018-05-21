# Prototyping a Car Park Billing/ Reservation System

## Synposis

Intercom: Arduino Uno - user's connect to intercom via Bluetooth to enter/ leave car park and recieve billing. Using a Bluetooth Shield module for bluetooth communication to device.

User Device: Wep Application GUI - Allows users to connect to Car Park, recieve billing and check availability of Car Park prior to leaving.

Database: PGSQL Server - Used to store data about Car Park and intercom devices so users and administrators can acess intercom data remotely through GUI

Sensors: Temperature - for temperature around Intercom, Motion - to detect unstable movement of intercom and Battery Level -  to check level of back up power source for Arduino.

## Code Example

### Example 1
USER: Opens web site GUI to Home page

GUI: Navbar at top allows user to go to: Home, Connect, Admin Login ( Shown on every page). Home - Displays all Car Parks, their max capacity, availability, price per hour and address. Grabbing these values from the PGSQL Database.

USER: Select Connect page.

GUI: Shows form: Entering or Leaving?, Select Car Park and Enter username.

USER: Entering, Car Park 1, lfet.

GUI: Calls procedure to connect to Car Park 1 intercom (Arduino), if succesfull requests to enter user in car park. Intercom returns confirmation of time entering.

GUI: Displays confirmation and time entering (User: lfet entered at H: 12 M: 34).

--- 2 Hours Later ---

USER: Opens web site GUI to Home page

GUI: Displays home page

USER: Select Connect page.

GUI: Shows form: Entering or Leaving?, Select Car Park and Enter username.

USER: Leaving, Car Park 1, lfet.

GUI: Calls procedure to connect to Car Park 1 intercom (Arduino), if succesfull requests to leave user from car park. Intercom returns confirmation and total time spent occupying car park.

GUI: Displays reciept by getting price per hour from DB and time spent from Arduino. (User: lfet stayed in Car Park 1 for H: 2 M: 30. Cost $12)

### Example 2

ADMIN: Opens web sit GUI to Home Page

GUI: Displays home page.

Admin: Select Admin Login.

GUI: Shows login form for Admin.

Admin: Username: dmit, Password: 000

GUI: Shows information for all Car Parks including state of sensors, Battery Level, Temperature and Motion.

### Example 3

Temperature sensor detects overheating at Intercom

LCD: Displays warning on LCD so Admin can easily check at the Car Park

## Installation

Arduino:
- Arduino DUE or other model (other model may need adapations).
- Arduino IDE and Arduino STL Library ( download link and copyright information in citation of report)
- Sensors and Hardware as described in Report, see Hardware Componets and Schematic.

User Application
- Python 3.7
- All modules as in file structure
- Bootstrap

## Motivation

For our University of Sydney, Embedded Systems Project. To understand and be able to implement a working prototype of an embedded system.

## Contributers

Dylan Mitri and Luke Fetin

## Licence

GNU and MitriFetin Licence. See LICENCE files.



