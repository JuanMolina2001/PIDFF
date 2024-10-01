
from utils import *

win.title("PIDFF")
win.geometry("800x600")
# form
tk.Label(win, text="Enter your email:").pack()
email = tk.Entry(win)
email.pack()
tk.Label(win, text="Enter the IDs of the proteins:").pack()
codes = tk.Text(win, height=10, width=50)
codes.pack()
# If you want more information about proteins, add the field names here
# Si quieres más información sobre las proteínas, agrega los nombres de los campos aquí
columns = ("ID", "organism", "DBSOURCE", "sequence")
# table
table.config(columns=columns)
index = 0
for col in columns:
    table.heading(str(index), text=col.title(), anchor="center")
    index += 1

# buttons for the form
frame_form = tk.Frame(win)
set_btn = tk.Button(frame_form, image=set_img, command=lambda: set_table((codes,email)))
add_btn = tk.Button(frame_form, image=add_img, command=lambda: add_table((codes,email)))
set_btn.pack(side="left")
add_btn.pack(side="right")
frame_form.pack()
# buttons for the table
frame_table = tk.Frame(win)
delete_btn = tk.Button(frame_table, image=delete_img, command=delete)
export_btn = tk.Button(frame_table, image=export_img, command=export)
table.pack(expand=True, fill="both")
delete_btn.pack(side="right")
export_btn.pack(side="left")
frame_table.pack()
set_menu()

win.mainloop()
