#import sys
#print(sys.path)
#print

import usb
import usb.util
import usb.core
idV = 0x0424
idP = 0xec00

#dev = usb.core.find(bDeviceClass = 0)
dev = usb.core.find(idVendor=idV, idProduct=idP)
if dev is None:
    raise ValueError("Device not found")
#try:
#    dev.set_configuration()

#except usb.core.USBError as e:
#    sys.exit("Failed to configure: " + str(e))
reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)
dev.set_configuration()
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None
#for x in range(0,50):
#    try:
msg = '/0x08'
print(ep.bEndpointAddress)
print
dev.write(ep.bEndpointAddress,msg,intf.bInterfaceNumber)
print ('wrote the message')
#assert dev.ctrl_transfer(0x0,7,  0, 0, msg) == len(msg)
#dev.write(0x01,'/0x08',100)
ret = dev.read(0x81,len(msg),intf.bInterfaceNumber)
sret = ''.join([chr(x) for x in ret])
assert sret == msg
#    except usb.core.USBError as e:
#        if e.args == ('Operation timed out',):
#            continue
