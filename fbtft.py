import subprocess
import time
import os

from test_fb import Framebuffer, show_name, msg

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
	if not os.path.isfile("/usr/bin/xinput"):
		print("\nInstalling xinput\n------------------\n\n")
		apt_get_install("xinput")

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
		call(["wget", "-O", "%s" % MPG_TEST, "http://fredrik.hubbe.net/plugger/test.mpg"])

	os.chdir(dir)

def ensure_spi():
	sudocall(["modprobe", "spi_bcm2708"])

def ensure_no_spi():
	sudocall(["modprobe", "-r", "spi_bcm2708"])

def ensure_fbtft():
	sudocall(["modprobe", "fbtft"])

class FBTFTdevice:
	def __init__(self, name, dev={}, drv={}, devname=""):
		self.name = name
		if not devname: devname = name
		self.devname = devname
		cmd = ["modprobe", "--first-time", "fbtft_device", "name=%s" % devname] + ["%s=%s" %(k,v) for k,v in dev.iteritems()]
		print("\n")
		print " ".join(cmd)
		sudocall(cmd)
		cmd = ["modprobe", self.name] + ["%s=%s" %(k,v) for k,v in drv.iteritems()]
		print " ".join(cmd)
		sudocall(cmd)
		time.sleep(0.5)
		self.fbdev = Framebuffer("/dev/fb1")
		show_name(self.fbdev, self.fbdev.rgb(255,0,0))

	def __enter__(self):
		return self

	def __exit__(self, type, value, trace):
		self.remove()

	def remove(self):
		self.fbdev.close()
		while True:
			time.sleep(1)
			try:
				sudocall(["rmmod", self.name])
			except OSError:
				continue
			break
		sudocall(["rmmod", "fbtft_device"])

class ADS7846device:
	def __init__(self, dev={}, drv={}):
		cmd = ["modprobe", "--first-time", "ads7846_device"] + ["%s=%s" %(k,v) for k,v in dev.iteritems()]
		print("")
		print " ".join(cmd)
		sudocall(cmd)
		cmd = ["modprobe", "ads7846"] + ["%s=%s" %(k,v) for k,v in drv.iteritems()]
		print("")
		print " ".join(cmd)
		sudocall(cmd)

	def __enter__(self):
		return self

	def __exit__(self, type, value, trace):
		self.remove()

	def remove(self):
		while True:
			try:
				sudocall(["rmmod", "ads7846_device"])
			except OSError:
				time.sleep(2)
				continue
			break

class GPIO_MOUSEdevice:
	def __init__(self, dev={}, drv={}):
		cmd = ["modprobe", "--first-time", "gpio_mouse_device"] + ["%s=%s" %(k,v) for k,v in dev.iteritems()]
		print("")
		print " ".join(cmd)
		sudocall(cmd)
		cmd = ["modprobe", "gpio_mouse"] + ["%s=%s" %(k,v) for k,v in drv.iteritems()]
		print("")
		print " ".join(cmd)
		sudocall(cmd)

	def __enter__(self):
		return self

	def __exit__(self, type, value, trace):
		self.remove()

	def remove(self):
		while True:
			try:
				sudocall(["rmmod", "gpio_mouse_device"])
			except OSError:
				time.sleep(2)
				continue
			break

def lsmod():
#	if not "fbtft" in subprocess.check_output("lsmod"):
	print subprocess.check_output("lsmod")

# by BlackJack
def get_revision():
	with open('/proc/cpuinfo') as lines:
		for line in lines:
			if line.startswith('Revision'):
				return int(line[line.index(':') + 1:], 16) & 0xFFFF
	raise RuntimeError('No revision found.')

def get_board_revision():
	revision = get_revision()
	if revision in (2, 3):
		return 1
	return 2

def fbtest():
	print("\nfbtest")
	dir = os.getcwd()
	os.chdir(os.path.dirname(__file__))
	os.chdir("..")
	sudocall(["./fbtest/fbtest", "-f", "/dev/fb1"])
	os.chdir(dir)

def mplayer_test(x, y):
	print("\nMplayer test")
	sudocall(["mplayer", "-nolirc", "-vo", "fbdev2:/dev/fb1", "-endpos", "6", "-vf", "scale=%s:%s" % (x,y), MPG_TEST])

def startx_test(wait=True):
	os.environ['FRAMEBUFFER'] = "/dev/fb1"
	print("\nX test")
	print "    To end the test, click Off button in lower right corner and press Alt-l (lowercase L) to logout (if screen is too small)"
	if wait:
		call(["startx"])
		return
	return subprocess.Popen(["startx"])

def console_test():
	print("\nConsole test")
	sudocall(["con2fbmap", "1", "1"])
	time.sleep(2)
	sudocall(["con2fbmap", "1", "0"])

def bl_power_test(dev):
	file="/sys/class/backlight/%s/bl_power" % dev.name
	if os.path.isfile(file):
		print("\nBacklight test")
		dev.fbdev.fill(0)
		c = dev.fbdev.rgb(255,0,0)
		msg(dev.fbdev, 'Backlight off', c, 2)
		time.sleep(1)
		sudoecho(file, "1")
		time.sleep(2)
		dev.fbdev.fill(0)
		msg(dev.fbdev, 'Backlight on', c, 2)
		sudoecho(file, "0")
		time.sleep(1)

def blank_test(dev):
	file="/sys/class/graphics/fb1/blank"
	if os.path.isfile(file):
		print("\nBlanking test")
		c = dev.fbdev.rgb(255,0,0)
		dev.fbdev.fill(0)
		msg(dev.fbdev, 'Blank=4', c, 2)
		time.sleep(1)
		sudoecho(file, "4")
		dev.fbdev.fill(0)
		msg(dev.fbdev, 'Blank=0', c, 2)
		time.sleep(2)
		sudoecho(file, "0")
		time.sleep(1)
