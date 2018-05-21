import sys, pexpect
from time import sleep

file = open('atmo_notice.txt', 'w')
file.close()

def saveData(data): 
    file = open('atmo_notice.txt', 'a')
    file.write(data)
    file.close()
    print(data)

gatt=pexpect.spawn('gatttool -t random -b DE:A5:4F:F0:96:92 -I')
gatt.sendline('connect')
gatt.expect('Connection successful') 
print("success!")

gatt.sendline('char-write-req 0x000c 0100')
gatt.expect('Characteristic value was written successfully')
print("Notice enable")

while True:
    gatt.expect('value.*', timeout=1000)
    param = gatt.after
    param = int(param.split()[2], 16)
    data = '\nVOC: ' + str(param) + ' Time: ' + time()
    saveData(data)
