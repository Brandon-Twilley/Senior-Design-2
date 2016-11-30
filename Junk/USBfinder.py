import sys
import usb.core

dev = usb.core.find(find_all=True)

for cfg in dev:
    print("Decimal vendorID= " + str(cfg.idVendor)+ " and productID= " + str(cfg.idProduct))
