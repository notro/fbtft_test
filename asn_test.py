'''
Test code for protoboard with:
* Adafruit 2.2"
* Sainsmart 1.8"
* Nokia 3310
'''

import subprocess
import time
import os

MPG_TEST = "/home/pi/test.mpg"

def call(*args):
	if subprocess.call(*args) != 0:
		raise OSError

def sudocall(cmd, *args):
	if subprocess.call(["sudo"] + cmd, *args) != 0:
		raise OSError

def sudoecho(file, str):
	os.system("sudo sh -c \"echo '%s' > %s\"" % (str, file))


def apt_get_install(*args):
	sudocall(["apt-get", "-y", "install"] + [item for item in args])

def prerequisites():
	dir = os.getcwd()
	os.chdir(os.path.dirname(__file__))
	os.chdir("..")

	if not os.path.isdir("fbtest/"):
		print("\nInstalling fbtest\n-----------------\n\n")
		sudocall(["apt-get", "-y", "install", "libnetpbm10-dev"])
		call(["git", "clone", "https://git.kernel.org/pub/scm/linux/kernel/git/geert/fbtest.git"])
		text = open("fbtest/fb.c").read()
		with open("fbtest/fb.c", "w") as f:
			f.write(text.replace("#include <asm/page.h>", "/* #include <asm/page.h> */"))
		os.chdir("fbtest")
		call(["make"])

	if not os.path.isfile(MPG_TEST):
		print("\nInstalling mplayer\n------------------\n\n")
		apt_get_install("mplayer")
		call(["wget", "--directory-prefix=%s" % MPG_TEST, "http://fredrik.hubbe.net/plugger/test.mpg"])

	os.chdir(dir)

def ensure_spi():
	sudocall(["modprobe", "spi_bcm2708"])

def ensure_fbtft():
	sudocall(["modprobe", "fbtft"])

class FBTFTdevice:
	def __init__(self, name, dev={}, drv={}):
		self.name = name
		cmd = ["modprobe", "--first-time", "fbtft_device", "name=%s" % name] + ["%s=%s" %(k,v) for k,v in dev.iteritems()]
#		print " ".join(cmd)
		sudocall(cmd)
		sudocall(["modprobe", self.name] + ["%s=%s" %(k,v) for k,v in drv.iteritems()])

	def __enter__(self):
		return self

	def __exit__(self, type, value, trace):
		self.remove()

	def remove(self):
		sudocall(["rmmod", self.name])
		sudocall(["rmmod", "fbtft_device"])

def lsmod():
#	if not "fbtft" in subprocess.check_output("lsmod"):
	print subprocess.check_output("lsmod")

def fbtest():
	dir = os.getcwd()
	os.chdir(os.path.dirname(__file__))
	os.chdir("..")
	sudocall(["./fbtest/fbtest", "-f", "/dev/fb1"])
	os.chdir(dir)

def mplayer_test(x, y):
	sudocall(["mplayer", "-nolirc", "-vo", "fbdev2:/dev/fb1", "-endpos", "8", "-vf", "scale=%s:%s" % (x,y), MPG_TEST])

def startx_test():
	os.environ['FRAMEBUFFER'] = "/dev/fb1"
	print "\n\n    To end the startx test, click Off button in lower right corner and press Alt-l (lowercase L) to logout"
	call(["startx"])

def bl_power_test():
	file="/sys/class/backlight/%s/bl_power" % dev.name
	if os.path.isfile(file):
		time.sleep(1)
		sudoecho(file, "1")
		time.sleep(2)
		sudoecho(file, "0")
		time.sleep(1)

def blank_test():
	file="/sys/class/graphics/fb1/blank"
	if os.path.isfile(file):
		time.sleep(1)
		sudoecho(file, "4")
		time.sleep(2)
		sudoecho(file, "0")
		time.sleep(1)

prerequisites()
#quit()

ensure_spi()
ensure_fbtft()



with FBTFTdevice("adafruit22fb", dev={'gpios' : "reset:25,led:18"}) as dev:
	fbtest()
	mplayer_test(176, 220)
	startx_test()

	bl_power_test()
	blank_test()

# Rotate
with FBTFTdevice("adafruit22fb", drv={'rotate':3}, dev={'gpios' : "reset:25,led:18"}) as dev:
	mplayer_test(220, 176)


with FBTFTdevice("sainsmart18fb", dev={'cs':1, 'gpios':"reset:23,dc:24"}) as dev:
	fbtest()
	mplayer_test(128, 160)
	startx_test()

# Rotate
with FBTFTdevice("sainsmart18fb", drv={'rotate':1}, dev={'cs':1, 'gpios':"reset:23,dc:24"}) as dev:
	mplayer_test(160, 128)


flexfb_drv_args = { 'width':176, 'height':220, 'buswidth':9, 'init':"-1,0xC1,0xFF,0x83,0x40,-1,0x11,-2,150,-1,0xCA,0x70,0x00,0xD9,-1,0xB0,0x01,0x11,-1,0xC9,0x90,0x49,0x10,0x28,0x28,0x10,0x00,0x06,-2,20,-1,0xC2,0x60,0x71,0x01,0x0E,0x05,0x02,0x09,0x31,0x0A,-1,0xC3,0x67,0x30,0x61,0x17,0x48,0x07,0x05,0x33,-2,10,-1,0xB5,0x35,0x20,0x45,-1,0xB4,0x33,0x25,0x4C,-2,10,-1,0x3A,0x05,-1,0x29,-2,10,-3" }
with FBTFTdevice("flexfb", drv=flexfb_drv_args, dev={'gpios':"reset:25,led:18"}) as dev:
	mplayer_test(176, 220)



#dev = FBTFTdevice("nokia3310fb", cs=1, gpios="reset:22,dc:21,led:17")
