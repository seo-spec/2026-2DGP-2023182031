"""방향키 입력에 따라 소년 캐릭터를 움직이는 단일 파일 뷰어."""

import pico2d

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


def handle_events():
    for event in pico2d.get_events():
        if event.type == pico2d.SDL_QUIT:
            return False
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return False
    return True


def main():
    """프로그램 실행 진입점."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        while handle_events():
            pico2d.clear_canvas()
            pico2d.update_canvas()
            pico2d.delay(0.005)
    finally:
        pico2d.close_canvas()


if __name__ == '__main__':
    main()
