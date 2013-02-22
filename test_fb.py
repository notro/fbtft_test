from time import sleep

import termios, fcntl, sys, os

import fb
from gfx import Rect


def keypressed():
	try:
		c = sys.stdin.read(1)
		return True
	except IOError:
		return False

def pause(secs):
	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	paused = False
	t = secs/0.1
	i = 0
	while i<t:
		if keypressed():
			paused = True
			break
		sleep(0.1)
		i += 1

	if paused:
		while True:
			if keypressed():
				break
			sleep(0.1)

	termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



def test_blank(fb, c):
	fb.fill(0)
	fb.putstr(1, fb.yres/2, 'Blank', c, 1)
	pause(1)
	fb.blank(1)
	pause(4)
	fb.fill(0)
	fb.putstr(1, fb.yres/2, 'Unblank', c, 1)
	fb.blank(0)


def test_outline(fb, c):
	fb.fill(0)
	fb.draw.rect(c, Rect(0, 0, fb.xres-1, fb.yres-1), 1)

	fb.draw.rect(c, Rect(2, 2, 4, 4), 0)
	fb.draw.rect(c, Rect(2, fb.yres-6, 4, 4), 0)

	fb.draw.rect(c, Rect(fb.xres-6, 2, 4, 4), 0)
	fb.draw.rect(c, Rect(fb.xres-6, fb.yres-6, 4, 4), 0)


def test_raster(fb, c):
	fb.fill(0)
	for y in range(0, fb.yres, 2):
		for x in range(0, fb.xres, 2):
			fb.putpixel(x, y, c)
			fb.putpixel(x+1, y+1, c)


def test_rgb(fb):
	fb.fill(0)
	width = (fb.xres-1)/3
	fb.draw.rect(fb.rgb(255,0,0), Rect(0, 0, width, fb.yres), 0)
	fb.putstr(5, fb.yres/2, 'RED', 0, 1)

	fb.draw.rect(fb.rgb(0,255,0), Rect(width, 0, width, fb.yres), 0)
	fb.putstr(5+width, fb.yres/2, 'GREEN', 0, 1)

	fb.draw.rect(fb.rgb(0,0,255), Rect(2*width, 0, width, fb.yres), 0)
	fb.putstr(5+2*width, fb.yres/2, 'BLUE', 0, 1)
	


if __name__ == '__main__':
	t = 5
	fb = fb.Framebuffer('/dev/fb1')
	print fb

	t = 5
	red = fb.rgb(255,0,0)
	yellow = fb.rgb(255,255,0)
	green = fb.rgb(0,255,0)

	fb.fill(0)

	# Show name
	width = len(fb.name)*6+2
	if fb.xres > width:
		x = (fb.xres - width)/2
		fb.putstr(x, fb.yres/2, fb.name, red, 1)
	else:
		str = 'Test'
		width = len(str)*6+2
		x = (fb.xres - width)/2
		fb.putstr(x, fb.yres/2, str, red, 1)
	pause(2)

	if (fb.bits_per_pixel != 1):
		test_rgb(fb)
		pause(t)

	test_outline(fb, yellow)
	pause(t)

	test_raster(fb, red)
	pause(t)

	test_blank(fb, red)
	pause(t)

	fb.fill(0)
	fb.close()
