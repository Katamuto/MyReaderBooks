#/usr/bin/env python3
#-*- coding:utf-8 -*-

# autors:
#  Katamuto - Camilo Sierra
# 
# version: 0.1. 
#

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import subprocess

# variables globales
preading = None
reading = False

# READ FUNCTIONS
def is_reading():
    global preading
    if preading:
        if preading.poll() == None:
            return True
    preading = None
    return False
def stop_reading():
    if is_reading():
        global preading, reading
        preading.kill()
        preading = None
        reading = False
def ajust_text(text):
    reps = {
            "PC": " pese ",
        }
    reps2 = {
            "á":"a",
            "é":"e",
            "í":"i",
            "ó":"o",
            "ú":"u",
            "ñ":"n",
            "ü":"u",
        }
    sample = u" 0123456789.,abcdefghijklmnñopqrstuvwxyz?¿!¡"
    ntext = text
    for k, v in reps.items():
        ntext = ntext.replace(k, v)
    ntext = ntext.lower()
    for k, v in reps2.items():
        ntext = ntext.replace(k, v)
    return ''.join(c for c in ntext if c in sample)
def read_text(text):
    global preading
    # si no hay texto reproduciendo
    if is_reading(): stop_reading()
    # ajustar texto
    text = ajust_text(text)
    # command
    command = 'echo "{}" | festival --tts'.format(text)
    preading = subprocess.Popen(command,
                                shell=True, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
def start_reading(textzone:tk.Text, root):
    global reading
    reading = True
    try:    pstart = textzone.index(tk.INSERT)
    except: pstart = "1.0"
    pfinal = tk.END
    text = textzone.get(pstart, pfinal)
    while reading:
        # si no está leyendo
        if not is_reading():
            # encontrar la siguiente posicion
            # posicion inicial
            T = textzone
            # optener la proxima oracion
            try:
                textread = text[:text.index(".")+1]
            except:
                textread = text
            # quitar lo proxima oracion
            text = text[len(textread):]
            # quitar espacios es blanco y otras cosas
            textread = ''.join(c for c in textread if not c in "\n\t")
            # seleccinar la posicion
            i1 = T.search(textread, pstart, nocase=1, stopindex=tk.END)
            i2 = "{}+{}c".format(i1, len(textread))
            try: T.tag_remove(tk.SEL, 1.0, i2)
            except: pass
            T.tag_add(tk.SEL, i1, i2)
            # leer en voz alta
            read_text(textread)
        # actualizar root
        root.update()

# FILE FUNCTIONS
def load_file(textzone, root):
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath: return
    # cargar
    textzone.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text_file = input_file.read()
        textzone.insert(tk.END, text_file)
    root.title(f"MyReaderBooks - {filepath}")
def save_file(textzone, root):
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath: return
    with open(filepath, "w") as output_file:
        text = textzone.get(1.0, tk.END)
        output_file.write(text)
    root.title(f"MyReaderBooks - {filepath}")

# EDIT FUNCTIONS
def copy(textzone=tk.Text, root=tk.Tk):
    text = textzone.get(tk.SEL_FIRST, tk.SEL_LAST)
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
def cut(textzone=tk.Text, root=tk.Tk):
    text = textzone.get(tk.SEL_FIRST, tk.SEL_LAST)
    textzone.replace("", tk.SEL_FIRST, tk.SEL_LAST)
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
def paste(textzone=tk.Text, root=tk.Tk):
    text = root.clipboard_get()
    root.clipboard_clear()
    if isinstance(text, str):
        textzone.insert(text, index=tk.INSERT)

if __name__=="__main__":
    # raiz
    root = tk.Tk()
    root.title("MyReaderBooks V2")
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    ########## ZONA DE EDICION DE TEXTO
    textzone = tk.Text(root, background="white")
    textzone.grid(row=1, column=0, sticky="nsew")
    scrolltext = tk.Scrollbar(root, command=textzone.yview, width=15)
    textzone['yscrollcommand'] = scrolltext.set
    scrolltext.grid(row=1, column=1, sticky='nsew')
    ###################################
    # barra de menus
    menubar = tk.Menu(root)
    root.config(menu=menubar)  # Lo asignamos a la base
    filemenu = tk.Menu(menubar, tearoff=0)
    #filemenu.add_command(label="Nuevo")
    filemenu.add_command(label="Abrir", command=lambda: load_file(textzone, root))
    filemenu.add_command(label="Guardar", command=lambda: save_file(textzone, root))
    filemenu.add_command(label="Cerrar", command=exit)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.quit)
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label="Cortar")
    editmenu.add_command(label="Copiar")
    editmenu.add_command(label="Pegar")
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Ayuda")
    helpmenu.add_separator()
    helpmenu.add_command(label="Acerca de...")
    # agregar menus a barra de menus
    menubar.add_cascade(label="Archivo", menu=filemenu)
    menubar.add_cascade(label="Editar", menu=editmenu)
    menubar.add_cascade(label="Ayuda", menu=helpmenu)
    #######################################
    # controles de voz
    controls = tk.Frame(root, relief=tk.RAISED)
    controls.grid(row=0, column=0, sticky="we")
    # botones
    btn_open = tk.Button(controls, text="Leer seleccion", command=lambda: read_text(textzone.get(tk.SEL_FIRST, tk.SEL_LAST)))
    btn_save = tk.Button(controls, text="Empezar a leer", command=lambda: start_reading(textzone, root))
    btn_stop = tk.Button(controls, text="Detener", command=stop_reading)
    btn_open.grid(row=0, column=0, sticky="ns")
    btn_save.grid(row=0, column=1, sticky="ns")
    btn_stop.grid(row=0, column=2, sticky="ns")
    # main loop
    root.mainloop()

