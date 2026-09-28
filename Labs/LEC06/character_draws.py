# 실습 과제 진행
from pico2d import *

import math
#맨 처음에 해야 할일은, 
open_canvas(800,600)
character = load_image('character.png')



def move_circle():
    print('CIRCLE')
    #캐릭터 이미지 표시
    for degree in range(360):
        radians = math.radians(degree)
        x=400+200*math.cos(radians)
        y=300+200*math.sin(radians)
        clear_canvas()
        character.draw(x,y)
        update_canvas()
    
        delay(0.01)
    
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