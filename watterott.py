'''
Test code for:
* Watterott
'''

from fbtft import *


prerequisites()

ensure_spi()
ensure_fbtft()

os.environ['DISPLAY'] = ":0"


for rotate in [180,270,0,90]:
	with FBTFTdevice("mi0283qt-v2", dev={ 'rotate':rotate, 'cs':1, 'speed':4000000, 'gpios':"reset:23", 'debug':get_debug() }, autoload=True, wait=2) as dev:
		console_test()
		if rotate == 180:
			bl_power_test(dev)
			bl_pwm_test(dev)

		if rotate == 180:
			startx_test()

		if rotate % 180:
			mplayer_test(240, 320, 2)
		else:
			mplayer_test(320, 240, 2)
