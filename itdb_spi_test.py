'''
Test code for protoboard with:
* ITDB02-2.8 SPI and Touch
'''

from fbtft import *


prerequisites()

ensure_spi()
ensure_fbtft()

os.environ['DISPLAY'] = ":0"

for rotate in [0,1,2,3]:
#for rotate in [1]:
	with FBTFTdevice("itdb28fb", devname="itdb28spifb", dev={'rotate':rotate, 'gpios':"reset:25,dc:24,led:18"}) as dev:
		console_test()
		ads7846args = { 'x_min':230, 'x_max':3900, 'y_min':200, 'y_max':3700, 'x_plate_ohms':80, 'pressure_max':255, 'gpio_pendown':17 }
		if rotate % 2:
			ads7846args['swap_xy'] = 1
		with ADS7846device(dev=ads7846args):
			x = startx_test(wait=False)
			time.sleep(3)
			if rotate == 1:
				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '0', '1'])
			if rotate == 2:
				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '1', '1'])
			if rotate == 3:
				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '1', '0'])
			while x.poll() == None:
				time.sleep(0.5)

		if rotate % 2:
			mplayer_test(320, 240)
		else:
			mplayer_test(240, 320)
		if rotate == 0:
			fbtest()
			bl_power_test(dev)
			blank_test(dev)
