#!/usr/bin/python
import sys
import usb.core
dev = usb.core.find(find_all = True)

for cfg in dev:
	sys.stdout.write('Decimal VendorID=' +str(cfg.idVendor)+ ' & ProductID=' + str(cfg.idProduct) + '\n')
	sys.stdout.write('HEX VendorID=' +hex(cfg.idVendor)+ ' & ProductID=' + hex(cfg.idProduct) + '\n')

