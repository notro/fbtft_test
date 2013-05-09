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
	sudocall(["mplayer", "-nolirc", "-vo", "fbdev2:/dev/fb1", "-endpos", "6", "-vf", "scale=%s:%s" % (x,y), MPG_TEST])

def startx_test():
	os.environ['FRAMEBUFFER'] = "/dev/fb1"
	print "\n\n    To end the startx test, click Off button in lower right corner and press Alt-l (lowercase L) to logout"
	call(["startx"])

def console_test():
	sudocall(["con2fbmap", "1", "1"])
	time.sleep(2)
	sudocall(["con2fbmap", "1", "0"])

def bl_power_test(dev):
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
