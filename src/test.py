# -*- coding: utf-8 -*-
def fib():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b


def process(str):
    pass
