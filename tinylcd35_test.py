'''
Test code for:
* tinylcd35
'''

from fbtft import *

prerequisites()

ensure_spi()
ensure_fbtft()


for rotate in [0,90,180,270]:
	with FBTFTdevice("tinylcd35", dev={ 'rotate':rotate, 'debug':get_debug()}, autoload=True) as dev:
		if rotate == 0:
			console_test()
			fbtest()
			bl_power_test(dev)
			startx_test()
		if rotate % 180:
			mplayer_test(480, 320)
		else:
			mplayer_test(320, 480)
