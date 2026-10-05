"""소닉 스프라이트 시트 애니메이션 뷰어."""

import pico2d

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800


def main():
    """단일 파일 실행 진입점."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        pico2d.clear_canvas()
        pico2d.update_canvas()
    finally:
        pico2d.close_canvas()


if __name__ == '__main__':
    main()
