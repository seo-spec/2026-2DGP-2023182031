"""소닉 스프라이트 시트 애니메이션 뷰어."""

import pico2d
from pathlib import Path
import sys

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


def handle_events():
    """창 닫기와 Escape 입력을 처리한다."""
    for event in pico2d.get_events():
        if event.type == pico2d.SDL_QUIT:
            return False
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return False
    return True


def load_sprite():
    """이미지가 없거나 손상된 경우 명확한 오류를 제공한다."""
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 파일을 찾을 수 없습니다: {SPRITE_PATH}')
    try:
        return pico2d.load_image(str(SPRITE_PATH))
    except Exception as error:
        raise RuntimeError(f'스프라이트 이미지 로딩 실패: {SPRITE_PATH}') from error


def main():
    """단일 파일 실행 진입점."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite = load_sprite()
        while handle_events():
            pico2d.clear_canvas()
            sprite.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
            pico2d.update_canvas()
            pico2d.delay(0.01)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(f'뷰어 실행 실패: {error}', file=sys.stderr)
        sys.exit(1)
