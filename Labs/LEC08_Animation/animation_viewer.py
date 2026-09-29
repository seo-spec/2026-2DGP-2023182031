from pico2d import *

open_canvas()
sonic = load_image('sonic-spritesheet.png')
grass = load_image('grass.png')

def idle():
	pass


def walk():
	pass


def jump():
	pass


def attack():
	pass


while True:
	clear_canvas()
	grass.draw(400, 30)
	idle()
	walk()
	jump()
	attack()
	update_canvas()