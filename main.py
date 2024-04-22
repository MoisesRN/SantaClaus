from threading import Semaphore
from threading import Thread
from time import sleep
from random import randint

required_elves = 3
required_reindeers = 9
elves_counter = 0
reindeer_counter = 0
santa_semaphore = Semaphore()
reindeer_semaphore = Semaphore(required_reindeers)
elf_semaphore = Semaphore()
elves_mutex = Semaphore()
mutex = Semaphore()


def prepare_sleigh():
    print("Preparing sleigh")


def help_elves():
    print("Helping elves")


def santa_sleeps():
    print("Santa goes to sleep")


def santa():
    global required_reindeers, required_elves, elves_counter, reindeer_counter
