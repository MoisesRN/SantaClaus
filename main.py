from threading import Semaphore, Thread
from time import sleep, time
from random import randint
import tkinter as tk
from PIL import Image, ImageTk

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


def run_program():
    santa_thread = Thread(target=santa)
    elf_threads = Thread(target=elves)
    reindeer_threads = Thread(target=reindeers)

    santa_thread.start()
    elf_threads.start()
    reindeer_threads.start()


def main():
    # Crear ventana
    window = tk.Tk()
    window.title("North Pole")

    # Cargar imágenes
    santa_image = Image.open("resources/Recurso1.png")
    santa_photo = ImageTk.PhotoImage(santa_image)

    elf_image = Image.open("resources/Recurso4.png")
    elf_photo = ImageTk.PhotoImage(elf_image)

    reindeer_image = Image.open("resources/Recurso3.png")
    reindeer_photo = ImageTk.PhotoImage(reindeer_image)

    # Mostrar imágenes en etiquetas
    santa_label = tk.Label(window, image=santa_photo)
    santa_label.pack()

    elf_label = tk.Label(window, image=elf_photo)
    elf_label.pack()

    reindeer_label = tk.Label(window, image=reindeer_photo)
    reindeer_label.pack()

    # Ejecutar programa en un hilo
    program_thread = Thread(target=run_program)
    program_thread.start()

    # Ejecutar bucle principal de la ventana
    window.mainloop()


if __name__ == "__main__":
    main()
