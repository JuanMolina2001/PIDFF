from Bio import Entrez
from Bio import SeqIO
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import os
from PIL import Image, ImageTk
import terminal
print(terminal.DNA)
dirname = os.path.dirname(__file__)
win = tk.Tk()
win.title("PIDFF")
win.geometry("800x600")
# form 
tk.Label(win, text="Enter your email:").pack()
email = tk.Entry(win)
email.pack()
tk.Label(win, text="Enter the IDs of the proteins:").pack()
codes = tk.Text(win, height=10, width=50)
codes.pack()
# images
delete_img = ImageTk.PhotoImage(Image.open(os.path.join(dirname, "assets/images/delete.png")).resize((30, 30)))
add_img = ImageTk.PhotoImage(Image.open(os.path.join(dirname, "assets/images/add.png")).resize((30, 30)))
export_img = ImageTk.PhotoImage(Image.open(os.path.join(dirname, "assets/images/excel.png")).resize((30, 30)))
set_img = ImageTk.PhotoImage(Image.open(os.path.join(dirname, "assets/images/set.png")).resize((30, 30)))
# If you want more information about proteins, add the field names here 
# Si quieres más información sobre las proteínas, agrega los nombres de los campos aquí
columns = ("ID", "organism", "DBSOURCE", "sequence")
# table
table = ttk.Treeview(win, columns=columns, show="headings")
index = 0
for col in columns:
    table.heading(str(index), text=col.title(), anchor="center")
    index += 1

# commands for buttons
def submit(add:bool):
    all_codes = codes.get("1.0", tk.END).split("\n")
    codes.delete("1.0", tk.END)
    if add is False:
        delete()
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
        table.insert("", "end", values=(id_search,  name_organism, db_source, sequence))

def delete():
    for row in table.get_children():
        table.delete(row)
def export():
    filename = filedialog.asksaveasfilename( title="Select a folder to save the excel", filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")), defaultextension=".xlsx")
    if filename == "":
        return
    print(filename)
    data = []
    for row in table.get_children():
        data.append(table.item(row)['values'])
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(filename, index=False)
def set_table():
    submit(False)
def add_table():
    submit(True)
# submit button
frame_form = tk.Frame(win)
set_btn = tk.Button(frame_form, image=set_img, command=set_table)
add_btn =tk.Button(frame_form, image=add_img, command=add_table)
set_btn.pack( side="left")
add_btn.pack(side="right")
frame_form.pack()
# buttons for the table
frame_table = tk.Frame(win)
delete_btn = tk.Button(frame_table, image = delete_img, command=delete)
export_btn = tk.Button(frame_table, image = export_img, command=export)
table.pack(expand=True, fill="both")
delete_btn.pack(side="right")
export_btn.pack(side="left")
frame_table.pack()
win.mainloop()
