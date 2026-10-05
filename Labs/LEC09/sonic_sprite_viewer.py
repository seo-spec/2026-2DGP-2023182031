"""소닉 스프라이트 시트 애니메이션 뷰어."""

import pico2d
from pathlib import Path
import sys
from dataclasses import dataclass
from time import perf_counter

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SPRITE_SCALE = 8
ANCHOR_X = CANVAS_WIDTH // 2
BASELINE_Y = 220
FRAME_INTERVAL = 0.1
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')

# 실제 시트의 위에서 아래, 왼쪽에서 오른쪽 순서. 제목/저작자 표기는 제외한다.
ANIMATION_ORDER = (
    'idle', 'look_up', 'crouch', 'walk', 'run', 'spin', 'spin_ball',
    'fast_run', 'dash', 'turn', 'hurt', 'balance', 'death', 'stand',
)
ANIMATIONS = {
    'idle': (
        (1, 447, 29, 39), (31, 447, 26, 38), (58, 447, 30, 39),
        (88, 447, 28, 38), (118, 447, 30, 38), (150, 447, 30, 38),
        (182, 447, 30, 38),
    ),
}


@dataclass
class Playback:
    """렌더링과 독립적으로 경과 시간에 따라 프레임을 전환한다."""

    frame_index: int = 0
    completed_loops: int = 0
    elapsed: float = 0.0

    def update(self, dt):
        self.elapsed += dt
        while self.elapsed >= FRAME_INTERVAL:
            self.elapsed -= FRAME_INTERVAL
            self.frame_index += 1
            if self.frame_index == len(ANIMATIONS['idle']):
                self.frame_index = 0
                self.completed_loops += 1

    @property
    def frame(self):
        return ANIMATIONS['idle'][self.frame_index]


def draw_frame(sprite, frame):
    """pico2d의 왼쪽 아래 기준 좌표로 프레임을 자른다."""
    width, height = frame[2:]
    sprite.clip_draw(*frame, ANCHOR_X, BASELINE_Y + height * SPRITE_SCALE / 2,
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
        playback = Playback()
        previous_time = perf_counter()
        while handle_events():
            now = perf_counter()
            playback.update(now - previous_time)
            previous_time = now
            pico2d.clear_canvas()
            draw_frame(sprite, playback.frame)
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
