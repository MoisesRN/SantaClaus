from threading import Semaphore, Thread
from time import sleep
import tkinter as tk
from PIL import Image, ImageTk
import random

required_elves = 4
required_reindeers = 10
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
                sleep(random.randint(1, 2))
        elif elves_counter == required_elves:
            help_elves()
            for _ in range(required_elves):
                elves_counter -= 1
                sleep(random.randint(1, 2))
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
        sleep(random.randint(1, 2))
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
        sleep(random.randint(1, 2))

def run_program():
    santa_thread = Thread(target=santa)
    elf_threads = Thread(target=elves)
    reindeer_threads = Thread(target=reindeers)

    santa_thread.start()
    elf_threads.start()
    reindeer_threads.start()

def main():
    global elves_counter, reindeer_counter

    # Crear ventana
    window = tk.Tk()
    window.title("North Pole")
    window.geometry("720x720")

    # Cargar imágenes
    santa_image1 = Image.open("resources/Recurso1.png")
    santa_image2 = Image.open("resources/Recurso2.png")
    elf_image = Image.open("resources/Recurso4.png")
    reindeer_image = Image.open("resources/Recurso3.png")

    rs_santa_image1 = santa_image1.resize((200, 200))
    rs_santa_image2 = santa_image2.resize((200, 200))
    rs_elf_image = elf_image.resize((50, 50))
    rs_reindeer_image = reindeer_image.resize((50, 50))

    santa_photo1 = ImageTk.PhotoImage(rs_santa_image1)
    santa_photo2 = ImageTk.PhotoImage(rs_santa_image2)
    elf_photo = ImageTk.PhotoImage(rs_elf_image)
    reindeer_photo = ImageTk.PhotoImage(rs_reindeer_image)

    elves_frame = tk.Frame(window)
    reindeers_frame = tk.Frame(window)
    santa_frame = tk.Frame(window)

    elves_frame.pack(side="left", padx=50)
    reindeers_frame.pack(side="left", padx=50)
    santa_frame.pack(side="left", padx=50)

    elf_labels = []
    reindeer_labels = []

    santa_label = tk.Label(santa_frame, image=santa_photo1)
    santa_label.pack()

    def update_window():
        global elves_counter, reindeer_counter

        for label in elf_labels:
            label.destroy()

        for _ in range(elves_counter):
            elf_label = tk.Label(elves_frame, image=elf_photo)
            elf_label.pack(side="top")
            elf_labels.append(elf_label)

        for label in reindeer_labels:
            label.destroy()

        for _ in range(reindeer_counter):
            reindeer_label = tk.Label(reindeers_frame, image=reindeer_photo)
            reindeer_label.pack(side="top")
            reindeer_labels.append(reindeer_label)

        if elves_counter == 3 or reindeer_counter == 9:
            santa_label.config(image=santa_photo2)
        elif elves_counter == 0 or reindeer_counter == 0:
            santa_label.config(image=santa_photo1)

        window.after(1000, update_window)

    update_window()

    program_thread = Thread(target=run_program)
    program_thread.start()

    window.mainloop()

if __name__ == "__main__":
    main()