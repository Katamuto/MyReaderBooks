#/usr/bin/env python3
#-*- coding:utf-8 -*-

# autors:
#  Katamuto - Camilo Sierra
# 
# version: 0.000... n ...001

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import subprocess

class App(object):
    def __init__(self):
        # all text
        self.process = None
        self.reading = False
        self.last_i2 = None
        # tk
        self.window = tk.Tk()
        self.window.title("MyReaderBooks")
        self.window.rowconfigure(0, minsize=5, weight=1)
        self.window.columnconfigure(1, minsize=5, weight=1)
        # text entry
        self.txt_edit = tk.Text(self.window)
        # scrool
        scrollb = tk.Scrollbar(self.window, command=self.txt_edit.yview)
        self.txt_edit['yscrollcommand'] = scrollb.set
        # buttons
        self.fr_buttons = tk.Frame(self.window, relief=tk.RAISED)
        self.btn_open = tk.Button(self.fr_buttons, text="Open", command=self.open_file)
        self.btn_save = tk.Button(self.fr_buttons, text="Save As...", command=self.save_file)
        # read
        self.btn_read    = tk.Button(self.fr_buttons, text="Read Selection", command=self.read_selected)
        self.btn_reading = tk.Button(self.fr_buttons, text="Start Reading", command=self.start_reading)
        self.btn_stop    = tk.Button(self.fr_buttons, text="Stop", command=self.stop_reading)
        # positions
        self.fr_buttons.grid(row=0, column=0, sticky="we")
        self.txt_edit.grid(row=1, column=0, sticky="nsew")
        scrollb.grid(row=1, column=1, sticky='nse')
        self.btn_open.grid(row=0, column=0, sticky="ns")
        self.btn_save.grid(row=0, column=1, sticky="ns")
        self.btn_read.grid(row=0, column=3, sticky="ns")
        self.btn_reading.grid(row=0, column=4, sticky="ns")
        self.btn_stop.grid(row=0, column=5, sticky="ns")
        # start
        self.window.mainloop()
    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        self.txt_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            self.alltext = input_file.read()
            self.txt_edit.insert(tk.END, self.alltext)
        self.window.title(f"MyReaderBooks - {filepath}")
    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txt_edit.get(1.0, tk.END)
            output_file.write(text)
        self.window.title(f"MyReaderBooks - {filepath}")
    def read_text(self, text:str):
        # edit string
        text = text.lower()
        text = text.replace('"',"")
        text = text.replace("á","a")
        text = text.replace("é","e")
        text = text.replace("í","i")
        text = text.replace("ó","o")
        text = text.replace("ú","u")
        text = text.replace("ñ","n")
        text = text.replace("ü","u")
        sample = u" 0123456789.,abcdefghijklmnñopqrstuvwxyz?¿!¡"
        # command
        command = 'echo "{}" | festival --tts'.format(text)
        # en paralelo
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    def running_process(self):
        if self.process:
            if self.process.poll() == None:
                return True
        self.procces = None
        return False
    def read_selected(self):
        T = self.txt_edit
        try:
            if not self.running_process():
                text = T.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.process = self.read_text(text)
        except tk.TclError:
            pass
    def start_reading(self):
        self.reading = True
        while self.reading:
            if not self.running_process():
                # posicion inicial
                T = self.txt_edit
                if self.last_i2 == None:
                    try:
                        rest = T.get(tk.INSERT, tk.END)
                    except:
                        rest = T.get("1.0", tk.END)
                else: rest = T.get(self.last_i2, tk.END)

                try: i = rest.index(".\n")
                except:
                    try: i = rest.index("\n")
                    except:
                        i = len(rest)
                        self.reading = False
                text = rest[:i+1]
                i1 = self.txt_edit.search(text, "1.0", nocase=1, stopindex=tk.END)
                i2 = "{}+{}c".format(i1, len(text))
                # limpiar
                try: T.tag_remove(tk.SEL, 1.0, i2)
                except: pass
                # marcar
                self.txt_edit.tag_add(tk.SEL, i1, i2)
                # leer en voz alta
                self.process = self.read_text(text)
                # progresar
                self.last_i2 = T.index(tk.SEL_LAST)
            self.window.update()
    def stop_reading(self):
        if self.running_process():
            #os.kill(self.process.pid, signal.SIGINT)
            self.process.kill()
            self.reading = False

if __name__=="__main__":
    window = App()

    


