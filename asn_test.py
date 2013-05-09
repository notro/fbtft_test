'''
Test code for protoboard with:
* Adafruit 2.2"
* Sainsmart 1.8"
* Nokia 3310
'''

from fbtft import *

prerequisites()

ensure_spi()
ensure_fbtft()


for rotate in [0,1,2,3]:
	with FBTFTdevice("adafruit22fb", drv={'rotate':rotate}, dev={'gpios' : "reset:25,led:18"}) as dev:
		console_test()
		if rotate % 2:
			mplayer_test(220,176)
		else:
			mplayer_test(176, 220)
		if rotate == 0:
			fbtest()
			bl_power_test(dev)
			blank_test()
			startx_test()


for rotate in [0,1,2,3]:

	with FBTFTdevice("sainsmart18fb", drv={'rotate':rotate}, dev={'cs':1, 'gpios':"reset:23,dc:24"}) as dev:
		console_test()
		if rotate % 2:
			mplayer_test(160,128)
		else:
			mplayer_test(128, 160)
		if rotate == 0:
			fbtest()
			startx_test()


flexfb_drv_args = { 'width':176, 'height':220, 'buswidth':9, 'init':"-1,0xC1,0xFF,0x83,0x40,-1,0x11,-2,150,-1,0xCA,0x70,0x00,0xD9,-1,0xB0,0x01,0x11,-1,0xC9,0x90,0x49,0x10,0x28,0x28,0x10,0x00,0x06,-2,20,-1,0xC2,0x60,0x71,0x01,0x0E,0x05,0x02,0x09,0x31,0x0A,-1,0xC3,0x67,0x30,0x61,0x17,0x48,0x07,0x05,0x33,-2,10,-1,0xB5,0x35,0x20,0x45,-1,0xB4,0x33,0x25,0x4C,-2,10,-1,0x3A,0x05,-1,0x29,-2,10,-3" }
with FBTFTdevice("flexfb", drv=flexfb_drv_args, dev={'gpios':"reset:25,led:18"}) as dev:
	mplayer_test(176, 220)



#dev = FBTFTdevice("nokia3310fb", cs=1, gpios="reset:22,dc:21,led:17")
