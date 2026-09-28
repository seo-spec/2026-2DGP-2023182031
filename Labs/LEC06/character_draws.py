# 실습 과제 진행
from pico2d import *

import math
#맨 처음에 해야 할일은, 
open_canvas(800,600)
character = load_image('character.png')

Triangle_A=(100,100)
Triangle_B=(700,100)
Triangle_C=(400,500)

def draw_top():
    print('TOP')
    for x in range(50,750,5):
        draw_character(x, 550)
    pass

def draw_right():
    print('right')
    for y in range(550,50,-5):
        draw_character(750,y)
    pass

def draw_bottom():
    print('BOTTOM')
    for x in range(750,50,-5):
        draw_character(x,50)
    pass

def draw_left():
    print('left')
    for y in range(50,550,5):
        draw_character(50,y)
    pass

def move_circle():
    print('CIRCLE')
    #캐릭터 이미지 표시
    for degree in range(360):
        radians = math.radians(degree)
        x=400+200*math.cos(radians)
        y=300+200*math.sin(radians)
        draw_character(x, y)
    
    pass

def draw_character(x, y):
    clear_canvas()
    character.draw(x,y)
    update_canvas()
    delay(0.01)

def move_rectangle():
    print('RECTANGLE')
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()
    pass


def draw_side1():
    print('triangle_side1')
    x0,y0=Triangle_A #시작점
    x1,y1=Triangle_B #이동 끝점
    n=100
    for step in range (n+1):
        t=step/n
        x=x0+(x1-x0)*t
        y=y0+(y1-y0)*t
        draw_character(x,y)
    pass
def draw_side2():
    print('triangle_side2')
    x0,y0=Triangle_B #시작점
    x1,y1=Triangle_C #끝점
    n=100
    for step in range(n+1):
        t=step/n
        x=x0+(x1-x0)*t
        y=y0+(y1-y0)*t
        draw_character(x,y)    
    pass
def draw_side3():
    print('triangle_side3')
    x0,y0=Triangle_C
    x1,y1=Triangle_A
    n=100
    for step in range(n+1):
        pass
    pass


def move_triangle():
    print('TRIANGLE')
    draw_side1()
    draw_side2()
    draw_side3()
    pass

while True:
    #move_circle()
    #move_rectangle()
    move_triangle()
    pass


close_canvas()