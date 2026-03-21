# controller.py

import helpers as H
from game import BattleshipGame
from darstellung import View


class Controller:
    # verbindet Spiellogik und Darstellung
    def __init__(self):
        self.game = BattleshipGame(n=8, ship_lengths=(4, 3, 2, 2))
        self.view = View(self.game)

        # klick-events für beide spielfelder
        self.view.player.on_mouse_down(lambda x, y: self.on_player_click(x, y))
        self.view.cpu.on_mouse_down(lambda x, y: self.on_cpu_click(x, y))

        # mausbewegung für die platzierungs-vorschau
        self.view.player.on_mouse_move(lambda x, y: self.on_player_move(x, y))
        self.view.player.on_mouse_out(lambda x, y: self.on_player_out(x, y))

        # button-events
        self.view.btn_rotate.on_click(self.on_rotate)
        self.view.btn_reset.on_click(self.on_reset)

        self.view.set_status("Platziere links deine 4 Schiffe.")
        self.view.redraw()

    # dreht die ausrichtung des nächsten schiffs
    def on_rotate(self, _):
        if self.game.phase == 'place':
            self.game.toggle_orientation()
            self.view.update_rotate_button()
            self.view.player[2].clear()
            self.view.redraw()

    # startet das spiel neu
    def on_reset(self, _):
        self.game.reset()
        self.view.update_rotate_button()
        self.view.player[2].clear()
        self.view.set_status("Neues Spiel gestartet. Platziere links deine 4 Schiffe.")
        self.view.redraw()

    # zeigt beim bewegen der maus eine vorschau für das nächste schiff
    def on_player_move(self, x, y):
        rc = H.xy_to_rc(x, y, self.game.n, self.view.CELL)
        if rc is None:
            self.view.player[2].clear()
            return

        row, col = rc
        self.view.draw_preview(row, col)

    # entfernt die vorschau wenn die maus das feld verlässt
    def on_player_out(self, x, y):
        self.view.player[2].clear()

    # setzt ein schiff auf dem spielerfeld
    def on_player_click(self, x, y):
        rc = H.xy_to_rc(x, y, self.game.n, self.view.CELL)
        if rc is None:
            return

        row, col = rc
        result = self.game.place_player_ship(row, col)

        self.view.set_status(result['msg'])
        self.view.player[2].clear()
        self.view.redraw()

    # verarbeitet den schuss des spielers auf das computerfeld
    def on_cpu_click(self, x, y):
        rc = H.xy_to_rc(x, y, self.game.n, self.view.CELL)
        if rc is None:
            return

        row, col = rc
        result = self.game.player_turn(row, col)

        if not result['ok']:
            self.view.set_status(result['msg'])
            return

        r1, c1, res1 = result['player_move']

        if res1 == 'hit':
            msg = f"Treffer auf ({row}, {col})!"
        else:
            msg = f"Wasser auf ({row}, {col})."

        if result['player_sunk']:
            msg = msg + " Du hast ein Schiff versenkt!"

        if result['cpu_move'] is not None and result['cpu_sunk']:
            msg = msg + " Der Computer hat eines deiner Schiffe versenkt!"

        self.view.set_status(msg)
        self.view.redraw()

        if result['winner'] == 'player':
            self.view.set_status("✅ Du hast gewonnen!")
            self.view.redraw()

        if result['winner'] == 'cpu':
            self.view.set_status("💀 Der Computer hat gewonnen.")
            self.view.redraw()