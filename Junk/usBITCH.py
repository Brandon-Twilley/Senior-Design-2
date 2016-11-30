import usb.core
import usb.util
dev = usb.core.find(idVendor=0xea0, idProduct=0x2209)
#dev = usb.core.find(bDeviceClass = 9)

if dev is None:
    raise ValueError("Device not found")

dev.set_configuration()

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

for cfg in device :
	for intf in cfg:
		if device.is_kernel_driver_active(intf.bInterfaceNumber):
			try:
				device.detach_kernel_driver(intf.bInterfaceNumber)
			except usb.core.USBError as e:
				sys.exit("coult not detach kernel driver from interface (0)")

assert ep is not None

ep.write("test")
