import random
import search_strategies_ as S
from model_view_controller import Observable, notify


class Maze(Observable):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, ncol=10, nrow=10):
        self.ncol = ncol
        self.nrow = nrow
        self.start = (0, 0)
        self.goal = (self.ncol-1, self.nrow-1)
        self.new_maze()

    @notify
    def new_maze(self):
        '''besuche mit DFS alle Knoten.
           Der go-back Dict enthaelt alle Verbindungen zw. Feldern
        '''
        go_back = S.search_df(self.start, self.get_random_neighbors, goal=None)[1]
        self.connections = set(go_back.items())

    def is_inside(self, pos):
        col, row = pos
        return 0 <= col < self.ncol and 0 <= row < self.nrow

    @notify
    def add_random_connections(self):
        '''fuege zufaellige Verbindungen zw. benachbarten Feldern hinzu'''
        for _ in range(10):
            pos = random.randrange(self.ncol), random.randrange(self.nrow)
            p = next(self.get_random_neighbors(pos))
            self.connections.add((p, pos))

    def get_random_neighbors(self, pos):
        col, row = pos
        for dc, dr in random.sample(self.directions, 4):
            pos_new = col + dc, row + dr
            if self.is_inside(pos_new):
                yield pos_new

    def get_connected_neighbors(self, pos):
        for p in self.get_random_neighbors(pos):
            if (pos, p) in self.connections or (p, pos) in self.connections:
                yield p

    @notify
    def solve(self, df=True):
        '''finde Weg mit DFS falls df gleich True, sond BFS'''
        if df:
            node, go_back = S.search_df(self.start, self.get_connected_neighbors, self.goal)[:2]
        else:
            node, go_back = S.search_bf(self.start, self.get_connected_neighbors, self.goal)[:2]
        path = S.get_path_home(node, go_back)[::-1]
        return path, df