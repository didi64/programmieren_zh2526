import random
import asyncio
import ipywidgets as widgets
from IPython.display import display


def start_memory_game():

    symbols_base = ["■","■","▲","▲","★","★","●","●"]

    state = {
        "cards": [],
        "buttons": [],
        "matched": [False]*8,
        "matched_by": [0]*8,
        "first_card": None,
        "second_card": None,
        "current_player": 1,
        "scores": [0,0],
        "mode": "Mensch gegen Mensch",
        "lock": False,
        "game_over": False,
        "turn_id": 0
    }

    title = widgets.HTML("<h2>Memory-Spiel</h2>")

    mode_selector = widgets.ToggleButtons(
        options=["Mensch gegen Mensch","Mensch gegen Computer"],
        description="Modus:"
    )

    turn_label = widgets.HTML()
    score_label = widgets.HTML()
    info_label = widgets.HTML("<b>Spiel gestartet</b>")


    restart_button = widgets.Button(
        description="Neustart",
        button_style="warning",
        layout=widgets.Layout(width="80px",height="80px")
    )


    def player_name(p):
        if state["mode"]=="Mensch gegen Mensch":
            return f"Spieler {p}"
        return "Mensch" if p==1 else "Computer"


    def update_scores():
        p1 = state["matched_by"].count(1)//2
        p2 = state["matched_by"].count(2)//2
        state["scores"]=[p1,p2]


    def update_labels():

        update_scores()

        if state["mode"]=="Mensch gegen Mensch":
            score_label.value=f"<b>Punkte:</b> Spieler 1 = {state['scores'][0]} | Spieler 2 = {state['scores'][1]}"
        else:
            score_label.value=f"<b>Punkte:</b> Mensch = {state['scores'][0]} | Computer = {state['scores'][1]}"

        if state["game_over"]:
            turn_label.value="<b>Spiel beendet</b>"
        else:
            turn_label.value=f"<b>Am Zug:</b> {player_name(state['current_player'])}"


    def reset_buttons():
        for b in state["buttons"]:
            b.description="?"
            b.disabled=False
            b.style.button_color=None


    def restart_game(_=None):

        state["cards"]=symbols_base[:]
        random.shuffle(state["cards"])

        state["matched"]=[False]*8
        state["matched_by"]=[0]*8
        state["first_card"]=None
        state["second_card"]=None
        state["current_player"]=1
        state["scores"]=[0,0]
        state["lock"]=False
        state["game_over"]=False
        state["mode"]=mode_selector.value
        state["turn_id"]+=1

        reset_buttons()

        info_label.value="<b>Neues Spiel gestartet</b>"

        update_labels()


    def finish_game():

        state["game_over"]=True
        state["lock"]=True
        update_labels()

        if state["scores"][0]>state["scores"][1]:
            info_label.value=f"<b>{player_name(1)} gewinnt!</b>"
        elif state["scores"][1]>state["scores"][0]:
            info_label.value=f"<b>{player_name(2)} gewinnt!</b>"
        else:
            info_label.value="<b>Unentschieden!</b>"


    async def resolve_turn(turn,first,second):

        await asyncio.sleep(1.2)

        if turn!=state["turn_id"]:
            return

        same=state["cards"][first]==state["cards"][second]

        if same:

            state["matched"][first]=True
            state["matched"][second]=True

            state["matched_by"][first]=state["current_player"]
            state["matched_by"][second]=state["current_player"]

            state["buttons"][first].style.button_color="lightgreen"
            state["buttons"][second].style.button_color="lightgreen"

            state["buttons"][first].disabled=True
            state["buttons"][second].disabled=True

            info_label.value=f"<b>{player_name(state['current_player'])} hat ein Paar gefunden und bleibt am Zug!</b>"

        else:

            state["buttons"][first].description="?"
            state["buttons"][second].description="?"

            state["current_player"]=2 if state["current_player"]==1 else 1

            info_label.value=f"<b>Kein Paar</b> – {player_name(state['current_player'])} ist am Zug"


        state["first_card"]=None
        state["second_card"]=None
        state["lock"]=False

        update_labels()

        if all(state["matched"]):
            finish_game()
            return

        if state["mode"]=="Mensch gegen Computer" and state["current_player"]==2:
            asyncio.create_task(computer_turn())


    def click_card(i):

        if state["game_over"] or state["lock"]:
            return

        if state["matched"][i]:
            return

        if state["mode"]=="Mensch gegen Computer" and state["current_player"]==2:
            return

        if i==state["first_card"]:
            return

        state["buttons"][i].description=state["cards"][i]

        if state["first_card"] is None:

            state["first_card"]=i

        else:

            state["second_card"]=i
            state["lock"]=True
            state["turn_id"]+=1
            t=state["turn_id"]

            asyncio.create_task(resolve_turn(t,state["first_card"],state["second_card"]))


    async def computer_turn():

        await asyncio.sleep(1)

        free=[i for i in range(8) if not state["matched"][i]]

        a,b=random.sample(free,2)

        state["buttons"][a].description=state["cards"][a]
        await asyncio.sleep(0.7)
        state["buttons"][b].description=state["cards"][b]

        state["first_card"]=a
        state["second_card"]=b

        state["turn_id"]+=1
        t=state["turn_id"]

        await resolve_turn(t,a,b)


    for i in range(8):

        btn=widgets.Button(
            description="?",
            layout=widgets.Layout(width="80px",height="80px")
        )

        btn.on_click(lambda b,i=i: click_card(i))

        state["buttons"].append(btn)


    grid = widgets.GridBox(
        children=[
            state["buttons"][0],state["buttons"][1],state["buttons"][2],
            state["buttons"][3],restart_button,state["buttons"][4],
            state["buttons"][5],state["buttons"][6],state["buttons"][7]
        ],
        layout=widgets.Layout(
            grid_template_columns="repeat(3,80px)",
            grid_gap="10px"
        )
    )


    restart_button.on_click(restart_game)

    display(widgets.VBox([
        title,
        mode_selector,
        turn_label,
        score_label,
        info_label,
        grid
    ]))

    restart_game()


start_memory_game()
