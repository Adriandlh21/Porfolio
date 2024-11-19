from tkinter import messagebox
from tkcalendar import Calendar
import tkinter as tk
import json

# Archivo de almacenamiento
ARCHIVO_TAREAS = "tareas.json"

# Lista global para almacenar las tareas
tareas = []

# Cargar tareas desde el archivo JSON
def cargar_tareas():
    try:
        with open(ARCHIVO_TAREAS, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Guardar tareas en el archivo JSON
def guardar_tareas():
    with open(ARCHIVO_TAREAS, "w") as archivo:
        json.dump(tareas, archivo, indent=4)

# Actualizar la lista de tareas mostrada
def actualizar_lista(fecha):
    lista_tareas.delete(0, tk.END)
    for tarea in tareas:
        if tarea["fecha_limite"] == fecha:
            estado = "✔️" if tarea["completada"] else "❌"
            lista_tareas.insert(tk.END, f"{tarea['descripcion']} - {estado}")

from datetime import datetime

def resaltar_dias_pendientes():
    # Eliminar etiquetas existentes en el calendario
    calendario.calevent_remove("all")
    
    for tarea in tareas:
        if not tarea["completada"]:
            try:
                # Convertir la fecha de cadena ("dd/mm/yyyy") a un objeto datetime.date
                fecha_tarea = datetime.strptime(tarea["fecha_limite"], "%d/%m/%Y").date()
                # Agregar una etiqueta para resaltar el día
                calendario.calevent_create(fecha_tarea, "Tarea Pendiente", "pendiente")
            except ValueError:
                print(f"Error al procesar la fecha: {tarea['fecha_limite']}")
    # Configurar el estilo de la etiqueta "pendiente"
    calendario.tag_config("pendiente", background="lightcoral", foreground="white")

# Cambiar la fecha seleccionada y actualizar la lista de tareas
def cambiar_fecha(event):
    fecha_seleccionada = calendario.get_date()
    actualizar_lista(fecha_seleccionada)

# Agregar una nueva tarea
def agregar_tarea():
    descripcion = entrada_descripcion.get()
    fecha_limite = calendario.get_date()
    if descripcion:
        tarea = {"descripcion": descripcion, "fecha_limite": fecha_limite, "completada": False}
        tareas.append(tarea)
        guardar_tareas()
        actualizar_lista(fecha_limite)
        entrada_descripcion.delete(0, tk.END)
        resaltar_dias_pendientes()  # Actualizar colores en el calendario
        messagebox.showinfo("Éxito", "Tarea añadida.")
    else:
        messagebox.showerror("Error", "Por favor, ingresa una descripción.")

# Completar una tarea
def completar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        # Obtener el índice de la tarea seleccionada en la lista visual
        indice = seleccion[0]
        # Obtener la descripción de la tarea seleccionada en la lista visual
        tarea_en_lista = lista_tareas.get(indice)

        # Buscar la tarea en la lista de tareas global usando el índice de la selección visual
        tarea_a_completar = tareas[indice]

        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar", f"¿Deseas marcar como completada y eliminar la tarea '{tarea_a_completar['descripcion']}'?")
        if respuesta:
            # Eliminar la tarea de la lista de tareas global usando el índice
            tareas.pop(indice)
            guardar_tareas()  # Guardar cambios en el archivo JSON
            actualizar_lista(calendario.get_date())  # Actualizar la lista de tareas
            resaltar_dias_pendientes()  # Actualizar el calendario
            messagebox.showinfo("Éxito", "Tarea completada y eliminada.")
    else:
        messagebox.showerror("Error", "Por favor, selecciona una tarea.")

# Configurar la ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Tareas")

# Entradas para añadir tareas
tk.Label(ventana, text="Descripción:").grid(row=0, column=0, padx=5, pady=5)
entrada_descripcion = tk.Entry(ventana, width=40)
entrada_descripcion.grid(row=0, column=1, padx=5, pady=5)

tk.Button(ventana, text="Añadir Tarea", command=agregar_tarea).grid(row=0, column=2, padx=5, pady=5)

# Calendario para seleccionar fechas
tk.Label(ventana, text="Selecciona una fecha:").grid(row=1, column=0, padx=5, pady=5)
calendario = Calendar(ventana, selectmode="day", date_pattern="dd/mm/yyyy")
calendario.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
calendario.bind("<<CalendarSelected>>", cambiar_fecha)

# Lista de tareas
lista_tareas = tk.Listbox(ventana, width=60, height=10)
lista_tareas.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

tk.Button(ventana, text="Completar Tarea", command=completar_tarea).grid(row=3, column=0, columnspan=3, pady=10)

# Cargar tareas iniciales y resaltar días pendientes
tareas = cargar_tareas()
resaltar_dias_pendientes()

# Iniciar la aplicación
ventana.mainloop()