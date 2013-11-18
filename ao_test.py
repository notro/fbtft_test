'''
Test code for protoboard with:
* The new Adafruit 2.2"
* Adafruit 1.3" Monochrome OLED
'''

from fbtft import *

prerequisites()

ensure_spi()
ensure_fbtft()


for rotate in [0,90,180,270]:
	with FBTFTdevice("adafruit22a", dev={ 'rotate':rotate, 'gpios' : "reset:25,dc:24,led:18", 'debug':get_debug()}, autoload=True) as dev:
		console_test()
		if rotate == 0:
			fbtest()
			bl_power_test(dev)
			startx_test()
		if rotate % 180:
			mplayer_test(320, 240)
		else:
			mplayer_test(240, 320)

with FBTFTdevice("adafruit13m", dev={ 'cs':1, 'gpios':"reset:23,dc:22", 'debug':get_debug() }, autoload=True) as dev:
	console_test()
	blank_test(dev)
