"""방향키 입력에 따라 소년 캐릭터를 움직이는 단일 파일 뷰어."""

import pico2d
from pathlib import Path
import sys
from dataclasses import dataclass
from time import perf_counter
from math import hypot, isfinite
from ctypes import byref

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SPRITE_SCALE = 1.5
FRAME_INTERVAL = 0.1
MOVE_SPEED = 200.0
LOOP_DELAY = 0.005
ASSET_DIR = Path(__file__).resolve().parent
BACKGROUND_PATH = ASSET_DIR / 'TUK_GROUND.png'
SPRITE_PATH = ASSET_DIR / 'animation_sheet.png'

# 실제 시트: 위에서부터 오른쪽 대기, 왼쪽 대기, 오른쪽 이동, 왼쪽 이동.
# 각 줄은 100×100 셀 8개이며 좌표는 pico2d의 왼쪽 아래 기준이다.
ANIMATIONS = {
    ('idle', 'right'): tuple((i * 100, 302, 100, 100) for i in range(8)),
    ('idle', 'left'): tuple((i * 100, 202, 100, 100) for i in range(8)),
    ('move', 'right'): tuple((i * 100, 102, 100, 100) for i in range(8)),
    ('move', 'left'): tuple((i * 100, 2, 100, 100) for i in range(8)),
}


@dataclass
class Character:
    x: float = CANVAS_WIDTH / 2
    y: float = CANVAS_HEIGHT / 2
    state: str = 'idle'
    facing: str = 'right'
    frame_index: int = 0
    frame_elapsed: float = 0.0

    @property
    def frames(self):
        return ANIMATIONS[(self.state, self.facing)]

    def update(self, dt, pressed_keys):
        if not isfinite(dt) or dt < 0:
            raise ValueError('경과 시간은 유한한 0 이상의 값이어야 합니다.')
        previous_animation = (self.state, self.facing)
        previous_x, previous_y = self.x, self.y
        horizontal = int(pico2d.SDLK_RIGHT in pressed_keys) - int(pico2d.SDLK_LEFT in pressed_keys)
        # 좌우 입력이 없거나 상쇄되면 세로 이동·정지에서도 마지막 방향을 유지한다.
        if horizontal < 0:
            self.facing = 'left'
        elif horizontal > 0:
            self.facing = 'right'
        vertical = int(pico2d.SDLK_UP in pressed_keys) - int(pico2d.SDLK_DOWN in pressed_keys)
        length = hypot(horizontal, vertical)
        if length:
            horizontal /= length
            vertical /= length
        self.x += horizontal * MOVE_SPEED * dt
        self.y += vertical * MOVE_SPEED * dt
        half_width, half_height = display_half_size()
        self.x = max(half_width, min(CANVAS_WIDTH - half_width, self.x))
        self.y = max(half_height, min(CANVAS_HEIGHT - half_height, self.y))
        moved = abs(self.x - previous_x) > 1e-9 or abs(self.y - previous_y) > 1e-9
        self.state = 'move' if moved else 'idle'
        if (self.state, self.facing) != previous_animation:
            self.frame_index = 0
            self.frame_elapsed = 0.0
            return
        self.frame_elapsed += dt
        steps = int((self.frame_elapsed + 1e-9) / FRAME_INTERVAL)
        if steps:
            self.frame_elapsed = max(0.0, self.frame_elapsed - steps * FRAME_INTERVAL)
            self.frame_index = (self.frame_index + steps) % len(self.frames)


def display_scale():
    width = max(frame[2] for frames in ANIMATIONS.values() for frame in frames)
    height = max(frame[3] for frames in ANIMATIONS.values() for frame in frames)
    return min(SPRITE_SCALE, CANVAS_WIDTH / width, CANVAS_HEIGHT / height)


def display_half_size():
    scale = display_scale()
    width = max(frame[2] for frames in ANIMATIONS.values() for frame in frames)
    height = max(frame[3] for frames in ANIMATIONS.values() for frame in frames)
    return width * scale / 2, height * scale / 2


def draw_character(sprite, frame, x, y):
    scale = display_scale()
    sprite.clip_draw(*frame, x, y, frame[2] * scale, frame[3] * scale)


def handle_events(pressed_keys):
    """pico2d에서 제공하는 SDL API로 포커스 이벤트까지 함께 처리한다."""
    direction_keys = {pico2d.SDLK_LEFT, pico2d.SDLK_RIGHT,
                      pico2d.SDLK_UP, pico2d.SDLK_DOWN}
    # pico2d.get_events()는 창 포커스 이벤트를 반환하지 않으므로 직접 폴링한다.
    event = pico2d.SDL_Event()
    while pico2d.SDL_PollEvent(byref(event)):
        if event.type == pico2d.SDL_QUIT:
            return False
        if event.type == pico2d.SDL_WINDOWEVENT:
            if event.window.event in (pico2d.SDL_WINDOWEVENT_FOCUS_LOST,
                                      pico2d.SDL_WINDOWEVENT_FOCUS_GAINED):
                pressed_keys.clear()
        elif event.type == pico2d.SDL_KEYDOWN:
            key = event.key.keysym.sym
            if key == pico2d.SDLK_ESCAPE:
                return False
            if key in direction_keys:
                pressed_keys.add(key)
        elif event.type == pico2d.SDL_KEYUP:
            pressed_keys.discard(event.key.keysym.sym)
    return True


def load_asset(path):
    if not path.is_file():
        raise FileNotFoundError(f'이미지 파일을 찾을 수 없습니다: {path}')
    try:
        return pico2d.load_image(str(path))
    except Exception as error:
        raise RuntimeError(f'이미지 로딩 실패: {path} ({error})') from error


def validate_frames(sprite):
    for (state, facing), frames in ANIMATIONS.items():
        if not frames:
            raise ValueError(f'프레임이 없는 동작: {state}/{facing}')
        for x, y, width, height in frames:
            if (min(x, y) < 0 or min(width, height) <= 0
                    or x + width > sprite.w or y + height > sprite.h):
                raise ValueError(f'스프라이트 범위를 벗어난 프레임: {state}/{facing}')


def main():
    """프로그램 실행 진입점."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        background = load_asset(BACKGROUND_PATH)
        sprite = load_asset(SPRITE_PATH)
        validate_frames(sprite)
        character = Character()
        pressed_keys = set()
        previous_time = perf_counter()
        while handle_events(pressed_keys):
            now = perf_counter()
            character.update(now - previous_time, pressed_keys)
            previous_time = now
            pico2d.clear_canvas()
            background.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                            CANVAS_WIDTH, CANVAS_HEIGHT)
            draw_character(sprite, character.frames[character.frame_index],
                           character.x, character.y)
            pico2d.update_canvas()
            pico2d.delay(LOOP_DELAY)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(f'입력 뷰어 실행 실패: {error}', file=sys.stderr)
        sys.exit(1)
