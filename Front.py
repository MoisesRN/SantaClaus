import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Función que se ejecutará cuando se presione el botón
def mostrar_mensaje():
    messagebox.showinfo("Mensaje", "¡Hola! Has presionado el botón.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Aplicación con imagen")

# Cargar la imagen
imagen = Image.open("/Users/jimmycastellanos/Downloads/123.png")
imagen = imagen.resize((200, 200))  # Redimensionar la imagen si es necesario
imagen = ImageTk.PhotoImage(imagen)

# Crear un marco para contener los widgets
marco = tk.Frame(ventana)
marco.pack(expand=True, fill='both')

# Crear una etiqueta con la imagen en el marco
etiqueta_imagen = tk.Label(marco, image=imagen)
etiqueta_imagen.pack(pady=10)

# Crear una etiqueta de texto en el marco
etiqueta_texto = tk.Label(marco, text="Presiona el botón para mostrar un mensaje.")
etiqueta_texto.pack()

# Crear un botón en el marco
boton = tk.Button(marco, text="Mostrar mensaje", command=mostrar_mensaje)
boton.pack(pady=5)

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()