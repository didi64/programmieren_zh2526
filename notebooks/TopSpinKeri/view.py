import widget_helpers as W
from ipycanvas import hold_canvas


canvas = None


def init(game):
    global canvas

    canvas = W.get_canvas(600, 180)
    game.update = update
    update(game.numbers)


def update(numbers):
    with hold_canvas():
        canvas.clear()

        canvas.fill_style = 'white'
        canvas.fill_rect(0, 0, 600, 180)

        for i in range(len(numbers)):
            row = i // 10
            column = i % 10

            x = 20 + column * 55
            y = 40 + row * 60

            canvas.fill_style = 'blue'
            canvas.fill_rect(x, y, 50, 40)

            canvas.stroke_style = 'black'
            canvas.stroke_rect(x, y, 50, 40)

            canvas.fill_style = 'black'
            canvas.font = '16px Arial'
            canvas.text_align = 'center'
            canvas.text_baseline = 'middle'
            canvas.fill_text(str(numbers[i]), x + 25, y + 20)

        canvas.stroke_style = 'red'
        canvas.stroke_rect(17, 37, 221, 46)