from time import sleep


move = None  # ueberschreibe mit Funktion, die vom Eventloop aufgerufen wird 

running = True
event_queue = []


def event_loop():
    while running:
        if event_queue:
            direction = event_queue.pop()
            last_direction = direction
        else:
            direction = last_direction

        if direction is not None:
            dx, dy = direction
            move(dx, dy)
 
        sleep(1)