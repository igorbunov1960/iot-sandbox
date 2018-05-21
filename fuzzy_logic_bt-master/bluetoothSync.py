import serial
import time

def run(bluetooth):
    bluetooth.write(b"BOOP "+str.encode(str(1)))#These need to be bytes not unicode, plus a number
    input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
    print('>>>data: ' + input_data.decode())#These are bytes coming in so a decode is needed
    time.sleep(0.1) #A pause between bursts
    # bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
    temperature = input_data.decode()
    temperature = temperature[:-2]
    return float(temperature)
