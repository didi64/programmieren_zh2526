import searching as S
from levelhelper import LevelHelper


class Solver:
    @staticmethod
    def _get_box_move(state_1, state_2):
        '''liefert die Box Verschiebung zweier benachbarter Zustaende
           state_1=(boxes1, comp1) und state_2=(boxes2, comp2)
        '''
        old_box = list(state_1[0] - state_2[0])[0]
        new_box = list(state_2[0] - state_1[0])[0]
        return old_box, new_box

    @staticmethod
    def update_frozenset(fs, old_item, new_item):
        '''swap old_item for new_item'''
        s = set(fs)
        s.remove(old_item)
        s.add(new_item)
        return frozenset(s)

    def __init__(self, level):
        self.lh = LevelHelper(level)
        self.player_pos = tuple(level.player_pos)
        self.blocked = frozenset(level.blocked)
        self.boxes = frozenset(level.boxes)
        self.targets = frozenset(level.targets)
        self.cells = frozenset(self.lh.cells)
        self.n_free_cells = len(self.cells) - len(self.targets)
        self.G = self.lh.G
        self.B_push = self.lh.B_push
        self.box_cells = frozenset(self.lh.box_cells)
        self.deadlocks = self.lh.deadlocks
        self.distances = self.lh.distances

    def is_deadlock(self, boxes):
        for deadlock in self.deadlocks:
            if deadlock.issubset(boxes):
                return True

    def box_moves2player_walk(self, box_moves):
        player_pos = self.player_pos
        boxes = set(self.boxes)

        walk = [player_pos]
        for old_box, new_box in box_moves:
            ppos = self.lh.new_pull_pos(new_box, old_box)
            if player_pos != ppos:
                path = self.lh.get_shortest_path(player_pos, ppos, boxes)
                walk += path[1:-1]
            walk += [ppos, old_box]
            player_pos = old_box
            boxes.remove(old_box)
            boxes.add(new_box)

        return walk

    def get_next_states(self, state):
        boxes, comp = state
        for bpos in boxes:
            for ppos, new_bpos in self.B_push.get(bpos, ()):
                if (
                    new_bpos not in boxes
                    and ppos not in boxes
                    and (comp is True or ppos in comp)
                ):
                    new_boxes = self.update_frozenset(boxes, bpos, new_bpos)
                    if not self.is_deadlock(new_boxes):
                        new_comp = self.get_comp_or_true(ppos, new_boxes)
                        yield new_boxes, new_comp

    def get_comp_or_true(self, pos, blocked):
        assert pos not in blocked, 'pos must not be in blocked'
        comp = self.lh.get_component(pos, lambda pos: self.G[pos] - blocked)
        return len(comp) == self.n_free_cells or frozenset(comp)

    def get_box_moves(self, goal, go_back):
        path = S.get_path_to_goal(goal, go_back)
        box_moves = [self._get_box_move(path[i], path[i+1]) for i in range(len(path)-1)]
        return box_moves

    def solve_bf(self):
        comp = self.get_comp_or_true(self.player_pos, self.boxes)
        initial_state = (self.boxes, comp)
        is_goal = lambda goal: goal[0] == self.targets
        goal, go_back = S.search_bf(initial_state, self.get_next_states, is_goal)
        return self.get_box_moves(goal, go_back)

    def solve_greedy(self):
        def h(state):
            score = 0
            targets = set(self.targets)

            for box in state[0]:
                dist, t = min((self.distances[(box, t)], t)
                              for t in targets
                              )
                score += dist
                targets.remove(t)

            return score

        comp = self.get_comp_or_true(self.player_pos, self.boxes)
        initial_state = (self.boxes, comp)
        is_goal = lambda goal: goal[0] == self.targets
        goal, go_back = S.search_greedy(initial_state, self.get_next_states, h, is_goal)
        return self.get_box_moves(goal, go_back)