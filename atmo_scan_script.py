import pexpect

results = open("scan_results.txt", 'w')
results.close()
child = pexpect.spawn("bluetoothctl")
child.logfile = open("/tmp/mylog", "wb")
child.send("scan on\n")
bdaddrs = []

try:
    while True:
##        child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})) ATMOTUBE")
        child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2}))", timeout=1000)
        bdaddr = child.match.group(1)
        results = open("scan_results.txt", 'a')
        results.write(str(bdaddr))
        results.close()
        print(bdaddr)

        
##        bdaddr = child.match.group(1)
##        param = child.after
##        if 'ATMOTUBE' in str(param):
##            param = child.match.group(0)
##            print(bdaddr)
        
##        print(param)

##        if bdaddr not in bdaddrs:
##            bdaddrs.append(bdaddr)
##            results.write(str(bdaddr))
except KeyboardInterrupt:
    child.close()
    results.close()
