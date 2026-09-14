import asyncio
from model_view_controller import Observable, notify
from cannon import Cannon


class Game(Observable):
    cannon_pos = (50, 50)
    cannon_size = 10
    size = 100

    def __init__(self):
        self.cannon = Cannon(self.cannon_pos, self.cannon_size)
        self.bullets = set()  # Menge von Bullet-Objekten, siehe shoot
        self.is_running = False

    @notify
    def new_game(self):
        self.bullets.clear()
        if not self.is_running:
            self._run()

    @notify
    def increase_angle(self):
        self.cannon.increase_angle()

    @notify
    def decrease_angle(self):
        self.cannon.decrease_angle()

    @notify
    def shoot(self):
        self.bullets.add(self.cannon.shoot())

    @notify
    def step(self):
        self._move_bullets()

    def _move_bullets(self):
        for bullet in self.bullets:
            x_new, y_new = bullet.pos + bullet.speed
            bullet.speed.x = bullet.speed.x * (1 if 0 <= x_new <= self.size else -1)
            bullet.speed.y = bullet.speed.y * (1 if 0 <= y_new <= self.size else -1)
            bullet.move()

        self.bullets = {bullet for bullet in self.bullets if bullet.health > 0}

    def _run(self):
        async def move_bullets():
            while self.running:
                self.step()
                await asyncio.sleep(0.2)

        self.running = True
        self.task = asyncio.create_task(move_bullets(), name='move_bullets')

    def __repr__(self):
        return f'Bullets({self.bullets})'
