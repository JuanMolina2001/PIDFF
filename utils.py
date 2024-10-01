import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from subprocess import Popen
import webbrowser
import os
from Bio import Entrez, SeqIO
import pandas as pd
import os
import threading
import sys
import json

dirname = os.path.dirname(__file__)
win = tk.Tk()
win.iconbitmap(os.path.join(dirname, "assets/images/icon.ico"))
table = ttk.Treeview(win, show="headings")



info = json.load(open("info.json"))
if info["open"] is False:     
    modal = tk.Toplevel(win)
    modal.title("Notes")
    modal.geometry("500x400")
    modal.resizable(False, False)
    canvas = tk.Canvas(modal)
    scrollbar = tk.Scrollbar(modal, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    notes: list = info["note"].split("\n")
    for note in notes:
        note = note.strip()
        note = note.replace("*", "")
        if note == "":
            continue
        if note.startswith("###"):
            note = note.replace("###", "")
            tk.Label(scrollable_frame, anchor=tk.W, width=50,text=note, font=("Helvetica", 9, "bold")).pack(expand=True, )
        elif note.startswith("##"):
            note = note.replace("##", "")
            tk.Label(scrollable_frame, anchor=tk.W, width=50,text=note, font=("Helvetica", 10, "bold")).pack(expand=True, )
        elif note[0].isdigit():
            note = note.replace("**", "")
            tk.Label(scrollable_frame, anchor=tk.W, width=50,text=note, font=("Helvetica", 8, "bold")).pack(expand=True, )
        else:
            note = note.replace("-", "")
            tk.Label(scrollable_frame, anchor=tk.W, width=50,text=note).pack(expand=True, )# images
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    with open("info.json", "r") as f:
        data = json.load(f)
        data["open"] = True
        with open("info.json", "w") as f:
            json.dump(data, f, indent=4)
delete_img = tk.PhotoImage(file=os.path.join(dirname, "assets/images/delete.png"))
add_img = tk.PhotoImage(file=os.path.join(dirname, "assets/images/add.png"))
export_img = tk.PhotoImage(file=os.path.join(dirname, "assets/images/excel.png"))
set_img = tk.PhotoImage(file=os.path.join(dirname, "assets/images/set.png"))
gh_image = tk.PhotoImage(file=os.path.join(dirname, "assets/images/github.png"))


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
    tk.Label(modal, text=f"Version {info['version']}").pack()
    tk.Label(modal, text=f"Author: {info['author']}").pack()
    tk.Label(modal, text=f"Email: {info['email']}").pack()
    tk.Label(modal, text="Github").pack()
    tk.Button(
        modal,
        image=gh_image,
        command=lambda: webbrowser.open(f"https://github.com/{info['url']}"),
    ).pack()
    tk.Button(
        modal,
        text="Protein icon by Icons8",
        command=lambda: webbrowser.open("https://icons8.com/icon/18334/protein"),
    ).pack()



def update():
    response = messagebox.askquestion(
        "Update",
        "A new version is available. The update requires a restart of the application. Do you want to continue?",
    )
    if response == "yes":
        threading.Thread(target=lambda: Popen(["updater.exe"], shell=True)).start()
        win.destroy()
        sys.exit()


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
    help.add_command(label="Update", command=update)
    menubar.add_cascade(label="File", menu=file)
    menubar.add_cascade(label="Edit", menu=edit)
    menubar.add_cascade(label="Help", menu=help)
    win.config(menu=menubar)
