'''
Test code for protoboard with:
* Sainsmart 3.2" SPI
'''

from fbtft import *


prerequisites()

ensure_spi()
ensure_fbtft()

os.environ['DISPLAY'] = ":0"


for rotate in [0,1,2,3]:
#for rotate in [0]:
	with FBTFTdevice("sainsmart32fb", devname="sainsmart32spifb", drv={'rotate':rotate}, dev={'gpios':"reset:25,dc:24"}) as dev:
		console_test()
#		ads7846args = { 'debug':2, 'cs':1, 'speed':2000000, 'model':7846, 'x_min':230, 'x_max':3900, 'y_min':200, 'y_max':3700, 'x_plate_ohms':80, 'pressure_max':255, 'gpio_pendown':23, 'keep_vref_on':1 }
#		if rotate % 2:
#			ads7846args['swap_xy'] = 1
#		with ADS7846device(dev=ads7846args):
#			x = startx_test(wait=False)
#			time.sleep(3)
#			if rotate == 1:
#				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '0', '1'])
#			if rotate == 2:
#				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '1', '1'])
#			if rotate == 3:
#				call(["xinput", "--set-prop", 'ADS7846 Touchscreen', 'Evdev Axis Inversion', '1', '0'])
#			while x.poll() == None:
#				time.sleep(0.5)

		if rotate % 2:
			mplayer_test(320, 240)
		else:
			mplayer_test(240, 320)
		if rotate == 0:
			fbtest()
#			bl_power_test(dev)
#			blank_test(dev)


# flexfb
with FBTFTdevice("flexfb", dev={'speed':16000000,'gpios':"reset:25,dc:24"}, drv={ 'rotate':0, 'width':240, 'height':320, 'regwidth':16, 'setaddrwin':2, 'init':"-1,0x00,0x0001,-1,0x03,0xA8A4,-1,0x0C,0x0000,-1,0x0D,0x080C,-1,0x0E,0x2B00,-1,0x1E,0x00B7,-1,0x01,0x2B3F,-1,0x02,0x0600,-1,0x10,0x0000,-1,0x11,0x6070,-1,0x05,0x0000,-1,0x06,0x0000,-1,0x16,0xEF1C,-1,0x17,0x0003,-1,0x07,0x0233,-1,0x0B,0x0000,-1,0x0F,0x0000,-1,0x41,0x0000,-1,0x42,0x0000,-1,0x48,0x0000,-1,0x49,0x013F,-1,0x4A,0x0000,-1,0x4B,0x0000,-1,0x44,0xEF00,-1,0x45,0x0000,-1,0x46,0x013F,-1,0x30,0x0707,-1,0x31,0x0204,-1,0x32,0x0204,-1,0x33,0x0502,-1,0x34,0x0507,-1,0x35,0x0204,-1,0x36,0x0204,-1,0x37,0x0502,-1,0x3A,0x0302,-1,0x3B,0x0302,-1,0x23,0x0000,-1,0x24,0x0000,-1,0x25,0x8000,-1,0x4f,0x0000,-1,0x4e,0x0000,-1,0x22,-3" }) as dev:
	mplayer_test(240, 320)
