import sys, pexpect
from time import sleep

file = open('atmo.txt', 'w')
file.close()

gatt=pexpect.spawn('gatttool -t random -b DE:A5:4F:F0:96:92 -I')
gatt.sendline('connect')
gatt.expect('Connection successful') 
print("success!")
gatt.sendline('char-read-uuid db450002-8e9a-4818-add7-6ed94a328ab2')
gatt.expect('value.*')
param = gatt.after
param = int(param.split()[1], 16)

def saveData(data): 
    file = open('atmo.txt', 'a')
    file.write(data)
        file.close()
    print(data)

data = 'VOC: ' + str(param)
saveData(data)

gatt.sendline('char-read-uuid db450003-8e9a-4818-add7-6ed94a328ab2')
gatt.expect('value.*')
param = gatt.after
param = int(param.split()[1], 16)

data = '\nHumidity: ' + str(param)
saveData(data)

gatt.sendline('char-read-uuid db450004-8e9a-4818-add7-6ed94a328ab2')
gatt.expect('value.*')
param = gatt.after
param = int(param.split()[1], 16)

data = '\nTemperature: ' + str(param)
saveData(data)