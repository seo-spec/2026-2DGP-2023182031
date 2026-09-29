from pico2d import *

open_canvas()
sonic = load_image('sonic-spritesheet.png')
grass = load_image('grass.png')

animations = {
	'walk': {
		'frames': [
			(67, 368, 30, 42), (107, 368, 24, 42), (144, 368, 27, 42),
			(182, 368, 27, 42), (223, 368, 26, 42), (265, 368, 23, 42),
			(302, 368, 35, 42), (339, 368, 28, 42), (375, 368, 32, 42),
		],
	},
	'run': {
		'frames': [
			(71, 320, 37, 43), (110, 320, 42, 43), (153, 320, 41, 43),
			(200, 320, 55, 43), (263, 320, 37, 43), (303, 320, 48, 43),
			(366, 320, 39, 43),
		],
	},
	'roll': {
		'frames': [
			(80, 174, 28, 39), (120, 174, 30, 39), (157, 174, 30, 39),
			(193, 174, 47, 39), (240, 174, 47, 39), (287, 174, 47, 39),
			(334, 174, 47, 39), (381, 174, 26, 39),
		],
	},
	'jump': {
		'frames': [
			(83, 22, 46, 46), (141, 22, 44, 46), (191, 22, 40, 46),
			(243, 22, 44, 46), (302, 22, 38, 46), (351, 22, 42, 46),
		],
	},
}


def walk():
	for frame_rect in animations['walk']['frames']:
		clear_canvas()
		grass.draw(400, 30)
		sonic.clip_draw(*frame_rect, 400, 90, 100, 100)
		update_canvas()
		delay(0.1)


def run():
	pass


def roll():
	pass


def jump():
	pass


while True:
	walk()
