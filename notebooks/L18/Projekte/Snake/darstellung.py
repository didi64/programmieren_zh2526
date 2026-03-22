from canvas_tools import draw_chessboard, place_stone


def draw_score(canvas, score):
    """Zeichnet den aktuellen Score oben rechts."""
    text = f'Score: {score}'
    canvas.fill_style = 'black'
    canvas.font = '16px sans-serif'
    canvas.fill_text(text, canvas.width - 120, 20)


def draw_game_over(canvas, score, highscore):
    """Zeichnet Dead Screen."""
    canvas.fill_style = 'rgba(0, 0, 0, 0.55)'
    canvas.fill_rect(0, 0, canvas.width, canvas.height)

    canvas.fill_style = 'white'
    canvas.font = '26px sans-serif'
    canvas.fill_text('GAME OVER', 30, canvas.height // 2 - 30)

    canvas.font = '16px sans-serif'
    canvas.fill_text(f'Score: {score}', 30, canvas.height // 2)
    canvas.fill_text(f'Highscore: {highscore}', 30, canvas.height // 2 + 22)
    canvas.fill_text('R = Neustart', 30, canvas.height // 2 + 44)


def draw(canvas, state):
    """Zeichnet das Spiel."""
    canvas.clear()

    draw_chessboard(canvas, colors=('white', '#dddddd'), n=state['n'])

    food_col, food_row = state['food']
    place_stone(canvas, food_col, food_row, color='green', n=state['n'], radius=0.7)

    for i, (col, row) in enumerate(state['snake']):
        color = 'blue' if i == 0 else 'black'
        place_stone(canvas, col, row, color=color, n=state['n'], radius=0.8)

    draw_score(canvas, state['score'])

    if state['game_over']:
        draw_game_over(canvas, state['score'], state['highscore'])