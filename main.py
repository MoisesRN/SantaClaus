from threading import Semaphore
from threading import Thread
import time

elves_counter = 0
reindeer_counter = 0
santa_semaphore = Semaphore()
reindeer_semaphore = Semaphore()
mutex = Semaphore(1)


def prepare_sleigh():
    print("Preparing sleigh")


def help_elves():
    print("Helping elves")


def santa():
    global elves_counter, reindeer_counter
    print("Santa Claus")
    while True:
        santa_semaphore.acquire()
        mutex.acquire()
        if reindeer_counter >= 9:
            prepare_sleigh()
            for _ in range(9):
                reindeer_semaphore.release()
            print("Santa Claus delivers gifts")
            reindeer_counter -= 9
            time.sleep(5)
        elif elves_counter == 3:
            help_elves()
        mutex.release()


elf_threads = []
reindeer_thread = []
