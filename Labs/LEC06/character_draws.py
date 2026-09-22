# 실습 과제 진행
from pico2d import *

#맨 처음에 해야 할일은, 
open_canvas(800,600)
character = load_image('character.png')


def move_circle():
    print('CIRCLE')
    #캐릭터 이미지 표시
    character.draw(400,300)
    update_canvas()
    pass

def move_rectangle():
    print('RECTANGLE')
    pass

def move_triangle():
    print('TRIANGLE')
    pass


while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass


close_canvas()