from ipycanvas import Canvas
from IPython.display import display
import ipywidgets as widgets
from ipywidgets import Output


canvas = Canvas(width=600, height=400, layout={'border': '1px solid black'})
info = widgets.HTML(value="Spielzüge: 0")
restart_button = widgets.Button(description="Restart")


out = Output( layout={'border': '1px solid black'})


ndisks = 3
stacks = []
selected_stack = None
moves = 0
won = False


def update_info():
    text = f"<b>Spielzüge:</b> {moves}"

    if selected_stack is not None:
        text += f" | Ausgewählt: Stapel {selected_stack+1}"

    if won:
        text += " | Gewonnen!"

    info.value = text


def show_stacks(stacks):
    canvas.clear()

    canvas.fill_style = "white"
    canvas.fill_rect(0, 0, 600, 400)

    canvas.fill_style = "black"
    canvas.fill_rect(50, 320, 500, 10)

    x_positions = [125, 300, 475]

    for x in x_positions:
        canvas.fill_rect(x-5, 120, 10, 200)

    colors = ["red", "green", "blue"]

    for col in range(3):
        stack = stacks[col]

        for row, disk in enumerate(stack):

            width = 60 + disk*40
            height = 20

            x = x_positions[col] - width/2
            y = 300 - row*25

            canvas.fill_style = colors[disk]
            canvas.fill_rect(x, y, width, height)

            canvas.stroke_style = "black"
            canvas.stroke_rect(x, y, width, height)

    update_info()


def new_game():
    global stacks, selected_stack, moves, won

    stacks = [list(range(ndisks))[::-1], [], []]
    selected_stack = None
    moves = 0
    won = False

    show_stacks(stacks)


def move_disk(src, dst):
    global moves, won

    if src == dst:
        return

    if len(stacks[src]) == 0:
        return

    disk = stacks[src][-1]

    if len(stacks[dst]) > 0 and stacks[dst][-1] < disk:
        return

    stacks[src].pop()
    stacks[dst].append(disk)

    moves += 1

    # Gewonnen prüfen
    if len(stacks[2]) == ndisks:
        won = True

    show_stacks(stacks)



def get_stack_from_x(x):
    if x < 200:
        return 0
    elif x < 400:
        return 1
    else:
        return 2


@out.capture()
def handle_click(x, y):
    global selected_stack

    clicked_stack = get_stack_from_x(x)
    if selected_stack is None:
        if len(stacks[clicked_stack]) > 0:
            selected_stack = clicked_stack
    else:
        move_disk(selected_stack, clicked_stack)
        selected_stack = None

    show_stacks(stacks)


def restart_game(button):
    new_game()


canvas.on_mouse_down(handle_click)
restart_button.on_click(restart_game)


new_game()


display(info)
display(restart_button)
display(canvas)
