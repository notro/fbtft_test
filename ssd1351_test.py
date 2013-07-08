'''
Test code for PiOLED
'''

from fbtft import *

prerequisites()

ensure_spi()
ensure_fbtft()

if get_board_revision() == 1:
	P1_13 = 21
else:
	P1_13 = 27

for rotate in [0]:
	with FBTFTdevice("ssd1351fb", dev={ 'rotate':rotate }) as dev:
		console_test()
		with GPIO_MOUSEdevice(dev={ 'pullup':1, 'polarity':1, 'up':23, 'down':17, 'left':18, 'right':P1_13, 'bleft':22 }):
			startx_test()
		mplayer_test(128,128)
		fbtest()
		blank_test(dev)

for rotate in [0]:
	with FBTFTdevice("flexfb", dev={ 'rotate':rotate, 'speed':20000000, 'gpios':"reset:24,dc:25" }, drv={ 'chip':'ssd1351' }) as dev:
		mplayer_test(128, 128)
