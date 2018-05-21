import serial
import time
import database

#####################################################
##  Connect to Arduino
#####################################################

def connect_arduino():

	print("Start")
	port="/dev/tty.CarPark11-DevB"  #Connect to Arduino using bluetooth address
	bluetooth=serial.Serial(port, 9600)  #Start communications with the bluetooth unit
	print("Connected")
	bluetooth.flushInput()

	return bluetooth

#####################################################
##  Request to Enter
#####################################################

def enter(userName):

	 # Connect to Arduino
	bluetooth = connect_arduino()

	input_data = ''

	#  Wait to Arduino request to recieve Entering or Leaving request
	while ('Entering or Leaving' not in input_data):
		input_data = bluetooth.readline().decode()[:20]

	# Send entering request
	bluetooth.write(b'Entering')
	time.sleep(2) # Delays used for synchronisation
	bluetooth.write(b'Entering')

	time.sleep(0.1)

	#  Wait to Arduino request to recieve User ID
	while (input_data != 'Enter User ID'):
		input_data = bluetooth.readline().decode()[:13]

	# Send User ID
	bluetooth.write(b""+str.encode(userName))

	time.sleep(0.1)

	# Wait to recieve confirmation from Arduino
	while ('User: ' not in input_data):
		input_data = bluetooth.readline().decode()

	message = input_data

	print(message)

	# Wait to Arduino request to recieve Data
	while ('Data' not in input_data):
		input_data = bluetooth.readline().decode()

	# Send data recieved confirmation to Arduino
	bluetooth.write(b"true")

	# Get data from message
	data = input_data.split(':')[1]
	data = data.split(',')
	data[3] = data[3].split('\r')[0]

	# Update databse
	database.set_capacity(int(data[0]),1)
	database.set_battery(int(data[1]), 1)
	database.set_motion(int(data[2]), 1)
	database.set_temp(int(data[3]), 1)


	bluetooth.close()  # Close bluetooth conenction
	print("Done")

	return message

#####################################################
##  Request to Leave
#####################################################

def leave(userName):

	# Connect to Arduino
	bluetooth = connect_arduino()

	#  Wait to Arduino request to recieve Entering or Leaving request
	input_data = ''
	while (input_data != 'Entering or Leaving?'):
		input_data = bluetooth.readline().decode()[:20]

	# Send entering request
	bluetooth.write(b'Leaving')
	time.sleep(2)
	bluetooth.write(b'Leaving')

	time.sleep(0.1)

	#  Wait to Arduino request to recieve User ID
	while (input_data != 'Enter User ID'):
		input_data = bluetooth.readline().decode()[:13]


	# Send User ID
	bluetooth.write(b""+str.encode(userName))
	time.sleep(1)
	bluetooth.write(b"" + str.encode(userName))

	time.sleep(0.1)

	# Wait to recieve confirmation from Arduino
	while ('User: ' not in input_data):
		input_data = bluetooth.readline().decode()

	message = input_data

	print(message)

	time.sleep(2)

	# Wait to Arduino request to recieve Data
	while ('Data' not in input_data):
		input_data = bluetooth.readline().decode()

	# Send data recieved confirmation to Arduino
	bluetooth.write(b"true")

	# Get data from message
	data = input_data.split(':')[1]
	data = data.split(',')
	data[3] = data[3].split('\r')[0]

	# Update databse
	database.set_capacity(int(data[0]), 1)
	database.set_battery(int(data[1]), 1)
	database.set_motion(int(data[2]), 1)
	database.set_temp(int(data[3]), 1)

	bluetooth.close()  # Close bluetooth connection
	print("Done")

	return message

