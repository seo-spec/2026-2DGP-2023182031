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
	walk_frames = animations['walk']['frames']
	for path_index in range(5):
		if path_index % 2 == 0:
			positions = range(0, 801, 5)
			flip = 'h'
		else:
			positions = range(800, -1, -5)
			flip = ''

		for frame_index, position_x in enumerate(positions):
			frame_rect = walk_frames[frame_index % len(walk_frames)]
			clear_canvas()
			grass.draw(400, 30)
			sonic.clip_composite_draw(
				*frame_rect, 0, flip, position_x, 90, 100, 100
			)
			update_canvas()
			delay(0.1)


def run():
	run_frames = animations['run']['frames']
	for frame_rect in run_frames:
		clear_canvas()
		grass.draw(400, 30)
		sonic.clip_composite_draw(
			*frame_rect, 0, 'h', 400, 90, 100, 100
		)
		update_canvas()
		delay(0.1)


def roll():
	pass


def jump():
	pass


while True:
	run()
