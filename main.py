from threading import Semaphore
from threading import Thread
from time import sleep
from random import randint
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

ventana = tk.Tk()
ventana.config(width=800, height=600)
ventana.title("Aplicación con imagen")
ventana.mainloop()

imagen1 = Image.open("resources/Recurso1")
#imagen = imagen.resize((200, 200))
imagen1 = ImageTk.PhotoImage(imagen1)

imagen2 = Image.open("resources/Recurso2")
#imagen = imagen.resize((200, 200))
imagen2 = ImageTk.PhotoImage(imagen2)

imagen3 = Image.open("resources/Recurso3")
#imagen = imagen.resize((200, 200))
imagen3 = ImageTk.PhotoImage(imagen3)

imagen4 = Image.open("resources/Recurso4")
#imagen = imagen.resize((200, 200))
imagen4 = ImageTk.PhotoImage(imagen4)

imagen5 = Image.open("resources/Recurso5")
#imagen = imagen.resize((200, 200))
imagen5 = ImageTk.PhotoImage(imagen5)

imagen6 = Image.open("resources/Recurso6")
#imagen = imagen.resize((200, 200))
imagen6 = ImageTk.PhotoImage(imagen6)

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
    print("Santa Claus")
    while True:
        santa_semaphore.acquire()
        mutex.acquire()
        if reindeer_counter == required_reindeers:
            prepare_sleigh()
            for _ in range(required_reindeers):
                reindeer_counter -= 1
                reindeer_semaphore.release()
                sleep(randint(1, 2))
        elif elves_counter == required_elves:
            help_elves()
            for _ in range(required_elves):
                elves_counter -= 1
                sleep(randint(1, 2))
        mutex.release()
        santa_sleeps()


def elves():
    global elves_counter, required_elves
    while True:
        elves_mutex.acquire()
        mutex.acquire()
        elves_counter += 1
        if elves_counter == required_elves:
            santa_semaphore.release()
        else:
            elves_mutex.release()
        mutex.release()
        print(f"Elf {elves_counter}")
        sleep(randint(1, 2))
        mutex.acquire()
        if not elves_counter:
            elves_mutex.release()
        mutex.release()


def reindeers():
    global reindeer_counter, required_reindeers
    while True:
        mutex.acquire()
        reindeer_counter += 1
        if reindeer_counter == required_reindeers:
            santa_semaphore.release()
        mutex.release()
        print(f"Reindeer {reindeer_counter}")
        reindeer_semaphore.acquire()
        sleep(randint(1, 2))


if __name__ == "__main__":
    santa_thread = Thread(target=santa)
    elf_threads = Thread(target=elves)
    reindeer_threads = Thread(target=reindeers)

    santa_thread.start()
    elf_threads.start()
    reindeer_threads.start()
