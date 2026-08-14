import widget_helpers as W
import grid_helpers as G
from ipycanvas import hold_canvas


WIDTH, HEIGHT = 300, 180


def init(game):
    global canvas
    canvas = W.get_canvas(width=WIDTH, height=HEIGHT)
    canvas.text_align = 'center'
    canvas.text_baseline = 'middle'
    canvas.fill_text(20, 150, 'Play TopSpin')
    game.update = update


def draw_topspin(canvas, numbers):
    print(numbers)
    # with hold_canvas():
    #     canvas.clear()
    #     stelle Zahlen graphisch dar


def update(numbers):
    draw_topspin(canvas, numbers)