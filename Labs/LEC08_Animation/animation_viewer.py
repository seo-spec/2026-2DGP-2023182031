from pico2d import *

open_canvas()
sonic = load_image('sonic-spritesheet.png')
grass = load_image('grass.png')

animations = {
	'walk': {'row': 6, 'frames': 9},
	'run': {'row': 5, 'frames': 7},
	'roll': {'row': 3, 'frames': 8},
	'jump': {'row': 0, 'frames': 6},
}

frame_width = 47
frame_height = 59


def walk():
	pass


def run():
	pass


def roll():
	pass


def jump():
	pass


while True:
	clear_canvas()
	grass.draw(400, 30)
	walk()
	run()
	roll()
	jump()
	update_canvas()