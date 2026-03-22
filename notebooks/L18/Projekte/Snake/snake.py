import asyncio
import ipywidgets as widgets
from ipycanvas import Canvas, hold_canvas
from IPython.display import display
import game
import darstellung


n = 18
cell_px = 20
canvas_size = n * cell_px

canvas = Canvas(
    width=canvas_size,
    height=canvas_size,
    layout=widgets.Layout(
        width=f'{canvas_size}px',
        height=f'{canvas_size}px'
    )
)

btn_start = widgets.Button(description='Start')
btn_pause = widgets.Button(description='Pause')

info = widgets.HTML('')

ui = widgets.VBox([
    canvas,
    widgets.HBox([btn_start, btn_pause]),
    info
])


def update(event, **kwargs):
    with hold_canvas(canvas):
        darstellung.draw(canvas, game.state)

    if game.state['game_over']:
        info.value = (
            f"<b>Game Over</b> — "
            f"Score: {game.state['score']} | "
            f"Highscore: {game.state['highscore']}")

    elif game.state['running']:
        info.value = (
            f"<b>Läuft</b> — "
            f"Score: {game.state['score']} | "
            f"Highscore: {game.state['highscore']}")
    else:
        info.value = (
            f"<b>Pausiert</b> — "
            f"Score: {game.state['score']} | "
            f"Highscore: {game.state['highscore']}")


game.update = update


def on_key_down(key, *flags):
    game.handle_key(key)


canvas.on_key_down(on_key_down)


def on_start_clicked(b):
    game.new_game(n)  # added
    game.start()
    start_loop()
    canvas.focus()  # added


def on_pause_clicked(b):
    game.pause()


btn_start.on_click(on_start_clicked)
btn_pause.on_click(on_pause_clicked)


async def move_snake():
    while game.state['running']:
        game.step()
        await asyncio.sleep(game.state['tick_seconds'])


snake_task = None


def start_loop():
    global snake_task
    if snake_task and not snake_task.done():
        return
    if game.state['running']:
        snake_task = asyncio.create_task(move_snake())


game.new_game(n=n, highscore_file='highscore.txt')
display(ui)
canvas.focus()