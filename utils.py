import tkinter as tk
from tkinter import ttk, filedialog
from subprocess import run
import webbrowser
import os
from Bio import Entrez, SeqIO
import pandas as pd
import requests
from tkinter import messagebox
import os



dirname = os.path.dirname(__file__)
win = tk.Tk()
table = ttk.Treeview(win,  show="headings")

# images
delete_img = tk.PhotoImage(file=os.path.join(dirname, "assets/images/delete.png"))
add_img = tk.PhotoImage(file=os.path.join(dirname, "assets/images/add.png"))
export_img = tk.PhotoImage(file=os.path.join(dirname, "assets/images/excel.png"))
set_img = tk.PhotoImage(file=os.path.join(dirname, "assets/images/set.png"))


def submit(data: tuple):
    codes: tk.Text
    email: tk.Entry
    codes, email = data
    all_codes = codes.get("1.0", tk.END).split("\n")
    codes.delete("1.0", tk.END)
    for code in all_codes:
        Entrez.email = email.get()
        # ID
        id_search = code.strip()
        search = Entrez.efetch(db="protein", id=id_search, rettype="gb", retmode="text")
        record = SeqIO.read(search, "genbank")
        # DBSOURCE
        db_source: str = record.annotations["db_source"].split(" ")[1].strip()
        # organism
        name_organism: str = record.annotations["organism"]
        # sequence
        sequence: str = record.seq
        # if you want to add more information about the proteins, add the field values here in the same order as the columns
        # si quieres agregar más información sobre las proteínas, agrega los valores de los campos en el mismo orden que las columnas
        table.insert("", "end", values=(id_search, name_organism, db_source, sequence))


def delete():
    for row in table.get_children():
        table.delete(row)


def export():
    filename = filedialog.asksaveasfilename(
        title="Select a folder to save the excel",
        filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")),
        defaultextension=".xlsx",
    )
    if filename == "":
        return
    print(filename)
    data = []
    for row in table.get_children():
        data.append(table.item(row)["values"])
    columns = table.cget("columns")
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(filename, index=False)


def set_table(data: tuple):
    delete()
    submit(data)


def add_table(data: tuple):
    submit(data)
def about():
    modal = tk.Toplevel(win)
    modal.title("About")
    modal.geometry("300x200")
    modal.resizable(False, False)
    tk.Label(modal, text="PIDFF").pack()
    tk.Label(modal, text="Version 1.0").pack()
    tk.Label(modal, text="Author: Juan Molina").pack()
    tk.Label(modal, text="Email: juanmolina2001@gmail.com").pack()
    tk.Label(modal, text="Github").pack()
    gh_image = tk.PhotoImage(file=os.path.join(dirname, "assets/images/github.png"))
    btn_gh = tk.Button(
        modal,
        image=gh_image,
        command=lambda: webbrowser.open("https://github.com/JuanMolina2001/PIDFF"),
    )
    btn_gh.pack()
    modal.mainloop()
def set_menu():
    menubar = tk.Menu(win)
    file = tk.Menu(menubar, tearoff=0)
    edit = tk.Menu(menubar, tearoff=0)
    help = tk.Menu(menubar, tearoff=0)
    file.add_command(label="Export Table", command=export)
    file.add_command(label="Exit", command=lambda: win.destroy())
    edit.add_command(label="Clear Table", command=delete)
    help.add_command(label="Help", command=lambda: print("Help"))
    help.add_command(label="about", command=about)
    help.add_command(label="Search for updates", command=check_update)
    menubar.add_cascade(label="File", menu=file)
    menubar.add_cascade(label="Edit", menu=edit)
    menubar.add_cascade(label="Help", menu=help)
    win.config(menu=menubar)

