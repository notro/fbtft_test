'''
Test code for PiOLED
'''

from fbtft import *

prerequisites()

ensure_spi()
ensure_fbtft()


for rotate in [0]:
	with FBTFTdevice("ssd1351fb", dev={ 'rotate':rotate }) as dev:
		console_test()
		with GPIO_MOUSEdevice(dev={ 'pullup':1, 'polarity':1, 'up':23, 'down':17, 'left':18, 'right':21, 'bleft':22 }):
			startx_test()
		mplayer_test(128,128)
		fbtest()
		blank_test(dev)
