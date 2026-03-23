def count_neighbor_mines(col, row, grid):
    '''
    Zählt Minen in den acht Nachbarfeldern eines Feldes.

    Args:
        row (int): Zeilenindex.
        col (int): Spaltenindex.

    Returns:
        int: Anzahl Minen in der direkten Nachbarschaft.
    '''
    count = 0
    size = len(grid)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            r = row + dr
            c = col + dc
            if 0 <= r < size and 0 <= c < size:
                count += grid[r][c]

    return count


def get_neighbors(col, row, grid):
    '''
    Liefert alle gültigen Nachbarfelder eines Feldes.

    Args:
        row (int): Zeilenindex.
        col (int): Spaltenindex.

    Returns:
        list[tuple[int, int]]: Liste der Nachbarpositionen als (row, col).
    '''
    neighbors = []
    size = len(grid)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            r = row + dr
            c = col + dc

            if 0 <= r < size and 0 <= c < size:
                neighbors.append((c, r))

    return neighbors


def flood_reveal(col,
                 row,
                 visibility_grid,
                 mines_grid,
                 flag_grid,
                 neighbor_mine_counts):
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
    stack = [(col, row)]
    visited = set()
    revealed = set()

    while stack:
        col, row = stack.pop()

        if (col, row) in visited:
            continue
        visited.add((col, row))

        for neighbor_col, neighbor_row in get_neighbors(col, row, mines_grid):
            if visibility_grid[neighbor_row][neighbor_col]:
                continue

            if flag_grid[neighbor_row][neighbor_col]:
                continue

            if mines_grid[neighbor_row][neighbor_col]:
                continue

            visibility_grid[neighbor_row][neighbor_col] = True
            revealed.add((neighbor_col, neighbor_row))

            if neighbor_mine_counts[neighbor_row][neighbor_col] == 0:
                stack.append((neighbor_col, neighbor_row))

    return revealed