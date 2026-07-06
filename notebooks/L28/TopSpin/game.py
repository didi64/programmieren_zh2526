import random


numbers = list(range(20))


def update(data):
    print(data)


def reset():
    numbers.sort()
    update(numbers)


def shift_left():
    numbers[:] = numbers[1:] + numbers[:1]
    update(numbers)


def shift_right():
    numbers[:] = numbers[-1:] + numbers[:-1]
    update(numbers)


def swap4():
    numbers[:4] = numbers[3::-1]
    update(numbers)


def scramble():
    random.shuffle(numbers)
    update(numbers)