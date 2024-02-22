import tkinter as tk
from tkinter import Label, ttk, Scrollbar
from PIL import Image, ImageTk, ImageSequence
import re
import pyperclip
import os

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("División de Gastos")
        self.geometry("800x600")
        self.resizable(True, True)
        self.configure(bg="white")
        
        icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iconos.ico") 
        self.iconbitmap(icono)

        
        self.font = ("Comic Sans MS", 12)
        

        self.imagen_participantes = Image.open("participantes.png")
        self.imagen_participantes = ImageTk.PhotoImage(self.imagen_participantes)

        self.label_participantes = Label(self, image=self.imagen_participantes, bg="white")
        self.label_participantes.place(relx=0.5, rely=0.32, anchor="n")

        self.imagen_nombre = Image.open("nombre.png")
        self.imagen_nombre = ImageTk.PhotoImage(self.imagen_nombre)

        self.label_nombre = Label(self, image=self.imagen_nombre, bg="white")
        self.label_nombre.place(relx=0.1, rely=0.08, anchor="w")

        self.nombre_input = ttk.Entry(self, font=self.font, foreground="black", background="white")
        self.nombre_input.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.05)

        self.imagen_monto = Image.open("monto.png")
        self.imagen_monto = ImageTk.PhotoImage(self.imagen_monto)

        self.label_monto = Label(self, image=self.imagen_monto, bg="white")
        self.label_monto.place(relx=0.50, rely=0.08, anchor="w")

        self.monto_input = ttk.Entry(self, font=self.font, foreground="black", background="white")
        self.monto_input.place(relx=0.50, rely=0.1, relwidth=0.3, relheight=0.05)
        self.monto_input.configure(validate="key")
        self.monto_input.configure(validatecommand=(self.register(self.validar_monto), "%P"))

        self.imagen_agregar = Image.open("agregar.png")
        self.imagen_agregar = ImageTk.PhotoImage(self.imagen_agregar)

        self.agregar_button = ttk.Button(self, image=self.imagen_agregar, command=self.agregar)
        self.agregar_button.place(relx=0.35, rely=0.2)

        self.imagen_limpiar = Image.open("borrar.png")
        self.imagen_limpiar = ImageTk.PhotoImage(self.imagen_limpiar)

        self.limpiar_button = ttk.Button(self, image=self.imagen_limpiar, command=self.limpiar_lista)
        self.limpiar_button.place(relx=0.10, rely=0.80)

        self.lista_datos = []
        self.lista_font = ("Comic Sans MS", 12)

        self.lista_frame = ttk.LabelFrame(self)
        self.lista_frame.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.4)

        self.lista_canvas = tk.Canvas(self.lista_frame, bg="grey95")
        self.lista_canvas.pack(side="left", fill="both", expand=True)

        self.lista_scrollbar = Scrollbar(self.lista_frame, orient="vertical", command=self.lista_canvas.yview)
        self.lista_scrollbar.pack(side="right", fill="y")

        self.lista_canvas.configure(yscrollcommand=self.lista_scrollbar.set)
        self.lista_canvas.bind("<Configure>", self.on_canvas_configure)

        self.lista_inner_frame = ttk.Frame(self.lista_canvas)
        self.lista_canvas.create_window((0, 0), window=self.lista_inner_frame, anchor="nw")
        self.lista_inner_frame.bind("<Configure>", self.on_frame_configure)

        self.gif_frame = ttk.Frame(self)
        self.gif_frame.place(relx=0.80, rely=0.72, anchor="s")
        self.cargar_gif()

        style = ttk.Style()
        style.configure("My.TLabelframe", background="white")

        self.imagen_calcular = Image.open("calcular.png")
        self.imagen_calcular = ImageTk.PhotoImage(self.imagen_calcular)

        self.calcular_button = ttk.Button(self, image=self.imagen_calcular, command=self.calcular)
        self.calcular_button.place(relx=0.67, rely=0.80)

    def cargar_gif(self):
        try:
            gif_image = Image.open("")
            self.gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]
            self.current_frame = 0

            self.label_gif = Label(self.gif_frame, image=self.gif_frames[self.current_frame], bg="white")
            self.label_gif.config(width=150, height=120)
            self.label_gif.pack()

            self.animate()

        except Exception as e:
            print(f"Error al cargar el GIF: {e}")

    def animate(self):
        self.label_gif.config(image=self.gif_frames[self.current_frame])

        self.current_frame += 1
        if self.current_frame >= len(self.gif_frames):
            self.current_frame = 0

        self.after(100, self.animate)

    def agregar(self):
        nombre = self.nombre_input.get()
        monto = self.monto_input.get()

        if nombre.strip() and monto.strip():
            self.lista_datos.append((nombre, monto))
            self.actualizar_lista()
            self.nombre_input.delete(0, tk.END)
            self.monto_input.delete(0, tk.END)

    def actualizar_lista(self):
        for widget in self.lista_inner_frame.winfo_children():
            widget.destroy()

        for (nombre, monto) in self.lista_datos:
            label = ttk.Label(self.lista_inner_frame, text=f"{nombre}    ${monto}", font=self.lista_font)
            label.pack(anchor="w")

    def limpiar_lista(self):
        self.lista_datos = []
        self.actualizar_lista()

    def validar_monto(self, valor):
        return re.match(r'^\d*\.?\d*$', valor) is not None

    def on_canvas_configure(self, event):
        self.lista_canvas.configure(scrollregion=self.lista_canvas.bbox("all"))

    def on_frame_configure(self, event):
        self.lista_canvas.configure(scrollregion=self.lista_canvas.bbox("all"))

    def calcular(self):
        total_gastos = sum(float(monto) for _, monto in self.lista_datos)
        numero_participantes = len(self.lista_datos)

        if numero_participantes > 0:
            costo_equitativo = total_gastos / numero_participantes
            resultados = []

            for nombre, monto in self.lista_datos:
                diferencia = costo_equitativo - float(monto)
                resultado = f"{nombre}: ${diferencia:.2f}"
                resultados.append(resultado)

            resultados_window = tk.Toplevel(self)
            resultados_window.title("Resultados")
            resultados_window.iconbitmap("iconos.ico")

            # Configura la ventana emergente para que tenga el mismo tamaño que la ventana principal
            ancho_ventana_principal = self.winfo_width()
            alto_ventana_principal = self.winfo_height()
            resultados_window.geometry(f"{ancho_ventana_principal}x{alto_ventana_principal}")

            # Establece el fondo blanco
            resultados_window.configure(bg="white")

            # Agregar la imagen "listadegastos.png" al comienzo de la ventana emergente
            imagen_resultados = Image.open("listadegastos.png")
            imagen_resultados = ImageTk.PhotoImage(imagen_resultados)

            label_imagen_resultados = Label(resultados_window, image=imagen_resultados, bg="white")
            label_imagen_resultados.image = imagen_resultados
            label_imagen_resultados.pack()

            # Crear un marco para la lista con fondo blanco y sin espacio arriba
            lista_frame = tk.Frame(resultados_window, bg="white")
            lista_frame.pack(fill="both", expand=True)

            # Crear la lista dentro del marco blanco
            lista_label = tk.Label(lista_frame, text="\n".join(resultados), font=("Comic Sans MS", 14), bg="white", anchor="n")
            lista_label.pack(fill="both", expand=True)

            # Alinear la imagen "ventana1.png" justo debajo de la lista
            imagen_ventana = Image.open("ventana.png")
            imagen_ventana = ImageTk.PhotoImage(imagen_ventana)
            label_ventana = Label(resultados_window, image=imagen_ventana, bg="white")
            label_ventana.image = imagen_ventana
            label_ventana.pack()

            # Agregar un marco para los botones y colocarlos uno al lado del otro, separados y más arriba
            botones_frame = tk.Frame(resultados_window, bg="white")
            botones_frame.pack(side="bottom", pady=20)  # Agregar un espacio vertical de 20 píxeles

            # Agregar un botón para cerrar la ventana con una imagen
            imagen_cerrar = Image.open("cerrar.png")
            imagen_cerrar = ImageTk.PhotoImage(imagen_cerrar)
            boton_cerrar = ttk.Button(botones_frame, image=imagen_cerrar, command=resultados_window.destroy)
            boton_cerrar.image = imagen_cerrar
            boton_cerrar.pack(side="left", padx=20)  # Colocar a la izquierda y agregar un espacio horizontal de 20 píxeles

            # Agregar un espacio adicional entre los botones
            espacio = tk.Frame(botones_frame, width=20, bg="white")
            espacio.pack(side="left")

            # Agregar un botón para compartir la ventana con una imagen
            imagen_compartir = Image.open("compartir.png")
            imagen_compartir = ImageTk.PhotoImage(imagen_compartir)
            boton_compartir = ttk.Button(botones_frame, image=imagen_compartir, command=self.compartir_resultados)
            boton_compartir.image = imagen_compartir
            boton_compartir.pack(side="left", padx=20)  # Colocar a la izquierda y agregar un espacio horizontal de 20 píxeles

    def compartir_resultados(self):
        resultados = "\n".join([f"{nombre}: ${float(monto):.2f}" for nombre, monto in self.lista_datos])  # Crear una lista de cadenas con formato
        pyperclip.copy(resultados)  # Copiar la cadena al portapapeles
        print("Resultados copiados al portapapeles:", resultados)

if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
