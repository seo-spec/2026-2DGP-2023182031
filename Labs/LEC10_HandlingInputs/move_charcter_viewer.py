"""방향키 입력에 따라 소년 캐릭터를 움직이는 단일 파일 뷰어."""

import pico2d
from pathlib import Path

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
ASSET_DIR = Path(__file__).resolve().parent
BACKGROUND_PATH = ASSET_DIR / 'TUK_GROUND.png'
SPRITE_PATH = ASSET_DIR / 'animation_sheet.png'


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
        background = pico2d.load_image(str(BACKGROUND_PATH))
        while handle_events():
            pico2d.clear_canvas()
            background.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                            CANVAS_WIDTH, CANVAS_HEIGHT)
            pico2d.update_canvas()
            pico2d.delay(0.005)
    finally:
        pico2d.close_canvas()


if __name__ == '__main__':
    main()
