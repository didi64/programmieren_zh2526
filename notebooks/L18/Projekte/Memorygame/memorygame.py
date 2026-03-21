from ipycanvas import MultiCanvas
from helpers import (
    draw_grid,
    click_to_cell,
    draw_player,
    generate_path_grid,
    draw_path,
    draw_healthbar,
    draw_score,
    draw_joker,
    click_to_joker,
)
from ipywidgets import Output, Image, VBox, Button, HTML
from IPython.display import display
from time import sleep

out = Output()

# Einstellung Spielgrösse
mcanvas = MultiCanvas(6, width=1600, height=750)
bg, path_layer, stats_layer, fg, popup_layer, score_layer = mcanvas

# Bild laden
amogsus = Image.from_file("amogsus.png")

game_background_grid_config = {
    "width": bg.width - 40,
    "height": bg.height - 240,
    "line_width": 5,
    "line_color": "black",
    "x0": 20,
    "y0": 70,
    "rows": 6,
    "cols": 18,
}

player_config = {
    "width": 70,
    "height": 50,
    "row": 0,
    "col": 0,
    "health": 5,
    "max_health": 5,
    "joker": 3,
    "max_joker": 3,
    "score": 0,
}


def reset_player():
    player_config["health"] = player_config["max_health"]
    player_config["joker"] = player_config["max_joker"]
    # Startposition für Player finden
    for r in range(game_background_grid_config["rows"]):
        if path[r][0] == 1:
            player_config["row"] = r
            draw_player(fg, game_background_grid_config, player_config, amogsus)
            break
    draw_healthbar(stats_layer, game_background_grid_config, player_config["health"],
                   player_config["max_health"])
    draw_joker(stats_layer, game_background_grid_config, player_config["joker"], player_config["max_joker"])
    player_config["col"] = 0
    # Player zeichnen
    draw_player(fg, game_background_grid_config, player_config, amogsus)


def game_over_popup():

    text = HTML("<h2>Game Over</h2>")

    restart = Button(description="Restart", button_style="success")

    popup_layer.clear()
    popup_layer.fill_style = f"rgba(0,0,0,{0.75})"
    popup_layer.fill_rect(0, 0, popup_layer.width, popup_layer.height)

    def restart_clicked(b):
        reset_player()
        player_config["score"] = 0
        draw_score(score_layer, game_background_grid_config, player_config["score"])
        popup_layer.clear()
        popup.close()
        hint_path()

    restart.on_click(restart_clicked)

    popup = VBox([text, restart])
    display(popup)


def hint_path():
    draw_path(path_layer, path, game_background_grid_config)
    sleep(3)
    path_layer.clear()


# Hintergrund zeichnen
draw_grid(bg, game_background_grid_config)

# Weg generieren
path = generate_path_grid(game_background_grid_config["rows"], game_background_grid_config["cols"])

# Player auf Start
reset_player()

# Punkte zeichnen
draw_score(score_layer, game_background_grid_config, player_config["score"])


@out.capture(clear_output=True)
def on_mouse_down(x, y):
    # Zuerst prüfen, ob auf Joker geklickt wurde
    joker_slot = click_to_joker(x, y, game_background_grid_config, player_config["max_joker"])
    if joker_slot is not None and player_config["joker"] > 0 and player_config["health"] > 0:
        player_config["joker"] -= 1
        draw_joker(stats_layer, game_background_grid_config, player_config["joker"],
                   player_config["max_joker"])
        hint_path()
        return
    cell = click_to_cell(x, y, game_background_grid_config)
    # Prüfen ob auf eine Zelle geklickt wurde
    if cell is not None and player_config["health"] > 0:
        col, row = cell
        if (
                (col - player_config["col"] == 1 and row - player_config["row"] == 0) or   # rechts
                (col - player_config["col"] == 0 and row - player_config["row"] == 1) or   # unten
                (col - player_config["col"] == 0 and row - player_config["row"] == -1)     # oben
             ):
            # Player-Position updaten
            player_config["col"] = col
            player_config["row"] = row
            # Player neu zeichnen
            draw_player(fg, game_background_grid_config, player_config, amogsus)
            # Falsch geklickt
            global path
            if path[row][col] != 1:
                player_config["health"] -= 1
                draw_healthbar(stats_layer, game_background_grid_config, player_config["health"],
                               player_config["max_health"])
            # Level geschafft
            if player_config["col"] == game_background_grid_config["cols"] - 1:
                player_config["score"] += 1
                draw_score(score_layer, game_background_grid_config, player_config["score"])
                # Weg generieren
                path = generate_path_grid(game_background_grid_config["rows"], game_background_grid_config["cols"])
                reset_player()
                hint_path()

    if player_config["health"] <= 0:
        game_over_popup()


mcanvas.on_mouse_down(on_mouse_down)
display(mcanvas, out)
hint_path()
