'''
https://github.com/PyUserInput/PyUserInput
'''

from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time

m = PyMouse()
k = PyKeyboard()

input_wireshark_file = 'E:\programBase\wireshark\sniffer\wireless\ByPort.pcap'
output_json_file = 'test1.json'

'''
print(x_dim)
#Hello,Hello, World! World!Hello, World!Hello, World!m.click(x_dim/2, y_dim/2, 1)
#m.click(2, 2, 1)
m.click(int(0), int(y_dim), 1)
'''

#Open wireshark
x_dim, y_dim = m.screen_size()
m.click(int(0), int(y_dim), 1)
time.sleep(1)
k.type_string('wireshark')
k.tap_key(k.enter_key)

time.sleep(4)


#Open required file
k.press_key(k.control_key)
k.tap_key('o')
k.release_key(k.control_key)

time.sleep(1)

k.type_string(input_wireshark_file)
k.tap_key(k.enter_key)

time.sleep(3)

#Export to JSON
k.tap_key(k.alt_key)
for i in range(0,10):
    k.tap_key(k.down_key)
k.tap_key(k.enter_key)
for i in range(0,5):
    k.tap_key(k.down_key)
k.tap_key(k.enter_key)

time.sleep(3)

k.type_string(output_json_file)
k.tap_key(k.enter_key)
