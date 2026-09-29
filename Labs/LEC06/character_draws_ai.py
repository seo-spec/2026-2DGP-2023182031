from pico2d import *
import math

open_canvas(800, 600)
character = load_image('character.png')

TRIANGLE_POINTS = ((100, 100), (700, 100), (400, 500))

def draw_character(x, y):
	clear_canvas()
	character.draw(x, y)
	update_canvas()
	delay(0.01)

def walk_segment(start, end, steps=None):
	start_x, start_y = start
	end_x, end_y = end
	if steps is None:
		distance = max(abs(end_x - start_x), abs(end_y - start_y))
		steps = distance // 5

	for step in range(steps + 1):
		ratio = step / steps
		x = start_x + (end_x - start_x) * ratio
		y = start_y + (end_y - start_y) * ratio
		draw_character(x, y)

def move_circle():
	print('CIRCLE')
	for degree in range(360):
		radians = math.radians(degree)
		x = 400 + 200 * math.cos(radians)
		y = 300 + 200 * math.sin(radians)
		draw_character(x, y)

def move_rectangle():
	print('RECTANGLE')
	rectangle_path = ((50, 550), (750, 550), (750, 50), (50, 50), (50, 550))
	for start, end in zip(rectangle_path, rectangle_path[1:]):
		walk_segment(start, end)

def move_triangle():
	print('TRIANGLE')
	triangle_path = TRIANGLE_POINTS + (TRIANGLE_POINTS[0],)
	for start, end in zip(triangle_path, triangle_path[1:]):
		walk_segment(start, end)

while True:
	move_circle()
	move_rectangle()
	move_triangle()

close_canvas()
_