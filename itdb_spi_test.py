'''
Test code for protoboard with:
* ITDB02-2.8 SPI and Touch
'''

from fbtft import *


prerequisites()

ensure_spi()
ensure_fbtft()

os.environ['DISPLAY'] = ":0"

for rotate in [180,270,0,90]:
	with FBTFTdevice("itdb28_spi", dev={'rotate':rotate, 'gpios':"reset:25,dc:24,led:18"}, autoload=True) as dev:
		console_test()
		ads7846args = { 'x_min':230, 'x_max':3900, 'y_min':200, 'y_max':3700, 'x_plate_ohms':80, 'pressure_max':255, 'gpio_pendown':17 }
		if rotate % 180:
			ads7846args['swap_xy'] = 1
		with ADS7846device(dev=ads7846args):
			x = startx_test(wait=False)
			time.sleep(3)
			if rotate == 270:
				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '0', '1'])
			if rotate == 180:
				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '1', '1'])
			if rotate == 90:
				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '1', '0'])
			while x.poll() == None:
				time.sleep(0.5)

		if rotate % 180:
			mplayer_test(320, 240)
		else:
			mplayer_test(240, 320)
		if rotate == 180:
			fbtest()
			bl_power_test(dev)
