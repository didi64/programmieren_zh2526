def draw_bg(canvas):
    canvas.fill_text('Schiebespiel', 20, 20)


def update(canvas, state):
    canvas.clear()
    canvas.fill_text(f'state: {state}', 20, 50)