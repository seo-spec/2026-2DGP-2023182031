"""소닉 스프라이트 시트 애니메이션 뷰어."""

import pico2d
from pathlib import Path
import sys
from dataclasses import dataclass
from time import perf_counter
from math import isfinite

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SPRITE_SCALE = 8
ANCHOR_X = CANVAS_WIDTH // 2
BASELINE_Y = 220
FRAME_INTERVAL = 0.1
LOOP_DELAY = 0.005
REPEAT_COUNT = 5
PAUSE_DURATION = 1.0
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')

# 실제 시트의 위에서 아래, 왼쪽에서 오른쪽 순서. 제목/저작자 표기는 제외한다.
ANIMATION_ORDER = (
    'idle', 'look_up', 'crouch', 'walk', 'run', 'spin', 'spin_ball',
    'fast_run', 'dash', 'turn', 'hurt', 'balance', 'death', 'stand',
)
ANIMATIONS = {
    'crouch': (
        (270, 448, 24, 32),
        (302, 448, 29, 26),
    ),
    'walk': (
        (8, 408, 26, 37),
        (37, 408, 27, 37),
        (65, 407, 31, 38),
        (97, 408, 37, 37),
        (135, 410, 32, 35),
        (170, 408, 32, 38),
        (206, 408, 26, 38),
        (238, 408, 24, 37),
        (263, 408, 30, 37),
        (295, 408, 36, 37),
        (334, 409, 32, 36),
        (370, 408, 29, 38),
    ),
    'run': (
        (1, 361, 33, 40),
        (39, 362, 35, 39),
        (89, 362, 35, 38),
        (130, 362, 34, 42),
        (181, 362, 34, 41),
        (228, 363, 33, 40),
    ),
    'spin': (
        (1, 326, 29, 30),
        (35, 327, 29, 31),
        (67, 327, 30, 29),
        (98, 327, 31, 29),
        (131, 327, 29, 30),
        (162, 326, 29, 31),
        (193, 326, 30, 29),
        (230, 326, 31, 29),
        (268, 325, 30, 30),
    ),
    'spin_ball': (
        (1, 292, 30, 27),
        (36, 292, 29, 27),
        (70, 292, 29, 27),
        (105, 292, 29, 27),
        (139, 292, 29, 27),
        (174, 292, 29, 27),
    ),
    'fast_run': (
        (1, 251, 29, 35),
        (36, 251, 30, 35),
        (74, 251, 31, 35),
        (111, 251, 31, 36),
        (149, 251, 30, 35),
        (186, 251, 31, 36),
    ),
    'dash': (
        (1, 207, 29, 35),
        (36, 207, 30, 35),
        (72, 208, 39, 31),
        (123, 208, 39, 32),
        (172, 208, 39, 31),
        (218, 208, 38, 32),
    ),
    'turn': (
        (1, 154, 24, 45),
        (31, 154, 29, 44),
        (65, 154, 20, 44),
        (90, 155, 25, 43),
        (119, 155, 25, 43),
        (149, 154, 20, 44),
    ),
    'hurt': (
        (184, 156, 40, 28),
        (232, 157, 39, 27),
    ),
    'balance': (
        (1, 108, 27, 38),
        (31, 110, 31, 36),
        (64, 110, 31, 36),
        (99, 110, 33, 38),
        (136, 110, 32, 36),
        (176, 110, 33, 36),
        (217, 110, 33, 36),
        (254, 111, 33, 36),
    ),
    'death': (
        (6, 56, 34, 40),
        (49, 56, 34, 43),
    ),
    'stand': (
        (96, 59, 23, 39),
        (125, 59, 23, 39),
    ),
    'look_up': ((212, 448, 28, 38), (240, 448, 29, 38)),
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
    animation_index: int = 0
    completed_loops: int = 0
    waiting: bool = False
    elapsed: float = 0.0

    def update(self, dt):
        """큰 시간 간격도 순차 처리하고 소수점 경계 오차를 방지한다."""
        if not isfinite(dt) or dt < 0:
            raise ValueError('경과 시간은 유한한 0 이상의 값이어야 합니다.')
        self.elapsed += dt
        while True:
            interval = PAUSE_DURATION if self.waiting else FRAME_INTERVAL
            if self.elapsed + 1e-9 < interval:
                break
            self.elapsed = max(0.0, self.elapsed - interval)
            if self.waiting:
                self.waiting = False
                self.animation_index = (self.animation_index + 1) % len(ANIMATION_ORDER)
                self.completed_loops = 0
                self.frame_index = 0
                continue
            self.frame_index += 1
            if self.frame_index == len(self.frames):
                self.frame_index = 0
                self.completed_loops += 1
                if self.completed_loops == REPEAT_COUNT:
                    self.frame_index = len(self.frames) - 1
                    self.waiting = True

    @property
    def name(self):
        return ANIMATION_ORDER[self.animation_index]

    @property
    def frames(self):
        return ANIMATIONS[self.name]

    @property
    def frame(self):
        return self.frames[self.frame_index]


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


def validate_animations(sprite):
    """동작 누락과 이미지 경계를 벗어난 프레임을 시작 시 검사한다."""
    if set(ANIMATION_ORDER) != set(ANIMATIONS):
        raise ValueError('재생 순서와 애니메이션 정의가 일치하지 않습니다.')
    for name in ANIMATION_ORDER:
        if not ANIMATIONS[name]:
            raise ValueError(f'프레임이 없는 동작: {name}')
        for x, y, width, height in ANIMATIONS[name]:
            if (min(x, y) < 0 or min(width, height) <= 0
                    or x + width > sprite.w or y + height > sprite.h):
                raise ValueError(f'이미지 범위를 벗어난 프레임: {name}')


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
    # 확대된 픽셀 경계를 보존한다. 한 프레임은 0.1초(초당 10프레임) 표시한다.
    pico2d.SDL_SetHint(b'SDL_RENDER_SCALE_QUALITY', b'0')
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite = load_sprite()
        validate_animations(sprite)
        playback = Playback()
        previous_time = perf_counter()
        while handle_events():
            now = perf_counter()
            playback.update(now - previous_time)
            previous_time = now
            pico2d.clear_canvas()
            draw_frame(sprite, playback.frame)
            pico2d.update_canvas()
            pico2d.delay(LOOP_DELAY)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(f'뷰어 실행 실패: {error}', file=sys.stderr)
        sys.exit(1)
