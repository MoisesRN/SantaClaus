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


santa_image = Image.open("resources/Recurso2.png")
santa_sleep_image = Image.open("resources/Recurso1.png")
elf_image = Image.open("resources/Recurso4.png")
reindeer_image = Image.open("resources/Recurso3.png")

rs_santa_image = santa_image.resize((200,200))
rs_santa_sleep_image = santa_sleep_image.resize((200,200))
rs_elf_image = elf_image.resize((50,50))
rs_reindeer_image = reindeer_image.resize((50,50))



def main():
    # Crear ventana
    window = tk.Tk()
    window.title("North Pole")
    window.geometry("720x720")

    # Cargar imágenes

    # Crear marcos para los bloques de imágenes
    elves_frame = tk.Frame(window)
    reindeers_frame = tk.Frame(window)
    santa_frame = tk.Frame(window)

    # Organizar los marcos verticalmente
    elves_frame.pack(side="left",  padx=50)
    reindeers_frame.pack(side="left",  padx=50)
    santa_frame.pack(side="left",  padx=50)
    
    santa_photo = ImageTk.PhotoImage(rs_santa_image)

    
    elf_photo = ImageTk.PhotoImage(rs_elf_image)

    
    reindeer_photo = ImageTk.PhotoImage(rs_reindeer_image)

    tk.Label(elves_frame, image=elf_photo).pack(side="top")
    tk.Label(reindeers_frame, image=reindeer_photo).pack(side="top")
    tk.Label(santa_frame, image=santa_photo).pack(side="top")

    """for _ in range(1):
        tk.Label(elves_frame, image=elf_photo).pack(side="top")
        tk.Label(reindeers_frame, image=reindeer_photo).pack(side="top")"""

    def add_elf():
        elves_counter[0] += 1
        tk.Label(elves_frame, image=elf_photo).pack(side="top")
        window.after(1000, add_elf)

    # Programar la adición periódica de elfos
    window.after(1000, add_elf)
    """""
    # Mostrar imágenes en etiquetas
    santa_label = tk.Label(window, image=santa_photo)
    santa_label.pack(side = "left")

    elf_label = tk.Label(window, image=elf_photo)
    elf_label.pack(side = "left")

    reindeer_label = tk.Label(window, image=reindeer_photo)
    reindeer_label.pack(side = "left")
    """

    # Ejecutar programa en un hilo
    program_thread = Thread(target=run_program)
    program_thread.start()

    # Ejecutar bucle principal de la ventana
    window.mainloop()


if __name__ == "__main__":
    main()
