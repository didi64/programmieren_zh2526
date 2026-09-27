import searching as S


class LevelHelper:
    @staticmethod
    def new_pull_pos(old_box, new_box):
        '''Spielerpos, nachdem Spieler Box von old_pos nach new_pos GEZOGEN hat'''
        return tuple(new_box[i] + (new_box[i] - old_box[i]) for i in range(2))

    @staticmethod
    def get_neighbors(pos, blocked):
        '''liefert alle 4-Nachbarn von pos, die nicht in blocked liegen'''
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (new_pos := (pos[0]+dc, pos[1]+dr)) not in blocked:
                yield new_pos

    @staticmethod
    def get_component(pos, get_ns):
        go_back = S.search_bf(pos, get_ns, None)[1]
        cells = set(go_back)
        return cells

    def __init__(self, level):
        self.level = level
        self.cells = self.get_component(level.player_pos, 
                                        lambda pos: self.get_neighbors(pos, self.level.blocked)
                                        )
        self.G = {pos: set(self.get_neighbors(pos, self.level.blocked)) 
                  for pos in self.cells
                  }
        self.box_cells = self.get_box_cells()
        self.B_push = self.get_B_push()
        self.deadlocks = self.get_deadlocks()
        self.distances = {(p, q): len(self.get_shortest_path(p, q))
                          for p in self.box_cells for q in self.box_cells
                          }

    def get_pulls(self, pos):
        for box in self.G[pos]:
            if self.new_pull_pos(pos, box) in self.cells:
                yield box  
    
    def get_box_cells(self):
        box_cells = set()
        for target in self.level.targets:
            box_cells |= self.get_component(target, self.get_pulls)
        return frozenset(box_cells)

    def get_B_push(self):
        B1 = {pos: set(self.G[pos]) & self.box_cells for pos in self.box_cells}
        B = {p: vs for p, ns in B1.items()
             if (vs := set(q for q in ns if p in self.get_pulls(q)))
             }
        B = dict(sorted(B.items(), key=lambda x: (len(x[1]), x[0])))
    
        B_push = {}
        for box, neighbors in B.items():
            B_push[box] = []
            for bpos in neighbors:
                ppos = self.new_pull_pos(bpos, box)
                B_push[box].append((ppos, bpos))
    
        return B_push
        
    def get_deadlocks(self):
        deadlocks = []
        for c in range(self.level.ncol):
            for r in range(self.level.nrow):
                square = {(c, r), (c+1, r), (c, r+1), (c+1, r+1)}
                # deadlock-Quadrat hat Felder ausserhalb der targets
                if (deadlock := square & self.cells) and deadlock - set(self.level.targets):
                    deadlocks.append(deadlock)
    
        
        deadlocks.sort(key=lambda x: len(x))
    
        n = len(deadlocks)
        to_keep = set(range(n))
        for i in range(n):
            for j in range(i+1, n):
                dl1, dl2 = deadlocks[i], deadlocks[j]
                if dl1.issubset(dl2):
                    to_keep.discard(j)
    
        deadlocks = [deadlocks[i] for i in to_keep]
        return [deadlock for deadlock in deadlocks if deadlock.issubset(self.box_cells)]

    def get_shortest_path(self, p, q, blocked=None):
        '''kuerzerste Weg des Spielers von p nach q unter Vermeidung der Felder in der Menge blocked'''
        blocked = blocked or set()
        node, go_back = S.search_bf(p, lambda pos: self.G[pos] - blocked, lambda x: x == q)
        path = S.get_path_to_goal(node, go_back)
        return path