import pygatt

# The BGAPI backend will attemt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.BGAPIBackend()

try:
    adapter.start()
    device = adapter.connect('DA:A3:03:1C:41:05')
    value = device.char_read("a1e8f5b1-696b-4e4c-87c6-69dfe0b0093b")
finally:
    adapter.stop()




