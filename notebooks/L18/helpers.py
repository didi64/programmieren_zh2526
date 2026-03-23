
def count_neighbor_mines(row, col):
    '''
    Zählt Minen in den acht Nachbarfeldern eines Feldes.

    Args:
        row (int): Zeilenindex.
        col (int): Spaltenindex.

    Returns:
        int: Anzahl Minen in der direkten Nachbarschaft.
    '''
    count = 0

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            r = row + dr
            c = col + dc

            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if mines_grid[r][c]:
                    count += 1

    return count


def get_neighbors(row, col):
    '''
    Liefert alle gültigen Nachbarfelder eines Feldes.

    Args:
        row (int): Zeilenindex.
        col (int): Spaltenindex.

    Returns:
        list[tuple[int, int]]: Liste der Nachbarpositionen als (row, col).
    '''
    neighbors = []

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            r = row + dr
            c = col + dc

            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                neighbors.append((r, c))

    return neighbors












def flood_reveal(start_row, start_col):
    '''
    Deckt zusammenhängende leere Bereiche automatisch auf.

    Ausgangspunkt ist ein Feld mit 0 Nachbarminen. Alle benachbarten Felder
    werden aufgedeckt. Falls ein Nachbarfeld ebenfalls 0 Nachbarminen hat,
    wird die Suche von dort fortgesetzt.

    Minen werden dabei nie aufgedeckt, und markierte Felder mit Flagge werden
    übersprungen.

    Args:
        start_row (int): Start-Zeilenindex.
        start_col (int): Start-Spaltenindex.
    '''
    stack = [(start_row, start_col)]
    visited = set()

    while stack:
        row, col = stack.pop()

        if (row, col) in visited:
            continue
        visited.add((row, col))

        for neighbor_row, neighbor_col in get_neighbors(row, col):
            if visibility_grid[neighbor_row][neighbor_col]:
                continue

            if flag_grid[neighbor_row][neighbor_col]:
                log(f'Kettenreaktion überspringt Flagge auf ({neighbor_row}, {neighbor_col}).')
                continue

            if mines_grid[neighbor_row][neighbor_col]:
                continue

            visibility_grid[neighbor_row][neighbor_col] = True
            log(
                f'Kettenreaktion deckt Feld auf: '
                f'({neighbor_row}, {neighbor_col}), '
                f'Nachbarminen: {neighbor_mine_counts[neighbor_row][neighbor_col]}'
            )

            if neighbor_mine_counts[neighbor_row][neighbor_col] == 0:
                stack.append((neighbor_row, neighbor_col))
