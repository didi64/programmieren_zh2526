import time
import asyncio
from model_view_controller import Observable, notify


class Timer(Observable):
    def __init__(self):
        self.is_running = False
        self.displayed_time = 0  # nutzt bereits setter

    @property
    def displayed_time(self):
        return self._displayed_time

    @displayed_time.setter
    @notify
    def displayed_time(self, time):
        self._displayed_time = time
        return self.displayed_time


    def start(self):
        if not self.is_running:
            self.t0 = time.time() - self.displayed_time
            self._run()

    def stop(self):
        self.is_running = False

    def reset(self):
        self.displayed_time = 0

    def _run(self):
        async def tick():
            while self.is_running:
                self.displayed_time = time.time() - self.t0
                await asyncio.sleep(0.01)

        self.is_running = True
        self.task = asyncio.create_task(tick(), name='tick')

    def __repr__(self):
        return f'{'running' if self.is_running else 'stopped'} {self.displayed_time}'