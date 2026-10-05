"""소닉 스프라이트 시트 애니메이션 뷰어."""

import pico2d
from pathlib import Path
import sys

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SPRITE_SCALE = 8
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')

# 실제 시트의 위에서 아래, 왼쪽에서 오른쪽 순서. 제목/저작자 표기는 제외한다.
ANIMATION_ORDER = (
    'idle', 'look_up', 'crouch', 'walk', 'run', 'spin', 'spin_ball',
    'fast_run', 'dash', 'turn', 'hurt', 'balance', 'death', 'stand',
)
ANIMATIONS = {'idle': ((1, 447, 29, 38),)}


def draw_frame(sprite, frame):
    """pico2d의 왼쪽 아래 기준 좌표로 프레임을 자른다."""
    width, height = frame[2:]
    sprite.clip_draw(*frame, CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
                     width * SPRITE_SCALE, height * SPRITE_SCALE)


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
            draw_frame(sprite, ANIMATIONS['idle'][0])
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
