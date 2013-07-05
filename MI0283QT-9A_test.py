'''
Test code for:
* Watterott MI0283QT-9A
'''

from fbtft import *


prerequisites()

ensure_spi()
ensure_fbtft()

os.environ['DISPLAY'] = ":0"


for rotate in [0,1,2,3]:
#for rotate in [0]:
	with FBTFTdevice("ili9341fb", dev={'rotate':rotate, 'gpios':"reset:25,led:18", 'speed':16000000}) as dev:
		console_test()
		if rotate == 0:
			fbtest()
			bl_power_test(dev)
		ads7846args = { 'x_min':250, 'x_max':3780, 'y_min':160, 'y_max':3930, 'x_plate_ohms':60, 'pressure_max':255, 'gpio_pendown':23 }
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


for rotate in [0,1]:
	if rotate == 0:
		flexfb_drv_args = { 'chip':'ili9341', 'buswidth':9 }
	elif rotate == 1:
		flexfb_drv_args = { 'chip':'ili9341', 'buswidth':9, 'init':'-1,0x28,-2,20,-1,0xCF,0x00,0x83,0x30,-1,0xED,0x64,0x03,0x12,0x81,-1,0xE8,0x85,0x01,0x79,-1,0xCB,0x39,0x2c,0x00,0x34,0x02,-1,0xF7,0x20,-1,0xEA,0x00,0x00,-1,0xC0,0x26,-1,0xC1,0x11,-1,0xC5,0x35,0x3E,-1,0xC7,0xBE,-1,0xB1,0x00,0x1B,-1,0xB6,0x0a,0x82,0x27,0x00,-1,0xB7,0x07,-1,0x3A,0x55,-1,0x36,0x38,-1,0x11,-2,120,-1,0x29,-2,20,-3' }
	with FBTFTdevice("flexfb", dev={ 'rotate':rotate, 'gpios':"reset:25,led:18", 'speed':16000000 }, drv=flexfb_drv_args) as dev:
		if rotate in [0,2]:
			mplayer_test(240, 320)
		else:
			mplayer_test(320, 240)
