"""방향키 입력에 따라 소년 캐릭터를 움직이는 단일 파일 뷰어."""

import pico2d
from pathlib import Path
import sys

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
ASSET_DIR = Path(__file__).resolve().parent
BACKGROUND_PATH = ASSET_DIR / 'TUK_GROUND.png'
SPRITE_PATH = ASSET_DIR / 'animation_sheet.png'

# 실제 시트: 위에서부터 오른쪽 대기, 왼쪽 대기, 오른쪽 이동, 왼쪽 이동.
# 각 줄은 100×100 셀 8개이며 좌표는 pico2d의 왼쪽 아래 기준이다.
ANIMATIONS = {
    ('idle', 'right'): tuple((i * 100, 300, 100, 100) for i in range(8)),
    ('idle', 'left'): tuple((i * 100, 200, 100, 100) for i in range(8)),
    ('move', 'right'): tuple((i * 100, 100, 100, 100) for i in range(8)),
    ('move', 'left'): tuple((i * 100, 0, 100, 100) for i in range(8)),
}


def draw_character(sprite, frame, x, y):
    sprite.clip_draw(*frame, x, y)


def handle_events():
    for event in pico2d.get_events():
        if event.type == pico2d.SDL_QUIT:
            return False
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return False
    return True


def load_asset(path):
    if not path.is_file():
        raise FileNotFoundError(f'이미지 파일을 찾을 수 없습니다: {path}')
    try:
        return pico2d.load_image(str(path))
    except Exception as error:
        raise RuntimeError(f'이미지 로딩 실패: {path} ({error})') from error


def main():
    """프로그램 실행 진입점."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        background = load_asset(BACKGROUND_PATH)
        sprite = load_asset(SPRITE_PATH)
        while handle_events():
            pico2d.clear_canvas()
            background.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                            CANVAS_WIDTH, CANVAS_HEIGHT)
            draw_character(sprite, ANIMATIONS[('idle', 'right')][0],
                           CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
            pico2d.update_canvas()
            pico2d.delay(0.005)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(f'입력 뷰어 실행 실패: {error}', file=sys.stderr)
        sys.exit(1)
