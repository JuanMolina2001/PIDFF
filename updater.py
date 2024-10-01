import requests
from tkinter import ttk, messagebox
import tkinter as tk
import json
import threading
events = threading.Event()
win = tk.Tk()
win.geometry("400x100")
win.resizable(False, False)
win.title("Update")

# Cargar la información del archivo JSON
info = json.load(open("info.json"))
path_to_file = 'main.exe'
url_release = f"https://api.github.com/repos/{info['url']}/releases/latest"
current_version = info["version"]
status = tk.Label(win, text=f"Start Updating...\nCurrent version: {current_version}")

def download_update():
    try:    
        response = requests.get(url_release)
        status.config(text=f"Checking...\nCurrent version: {current_version}")
        if response.status_code == 200:
            try:
                release = response.json()
            except json.JSONDecodeError:
                raise Exception("Error getting file")
            
            if release:
                last_release = release["tag_name"]
                if last_release != current_version:
                    binaries = release["assets"]
                    note_version = release["body"]
                    for binary in binaries:
                        if binary["name"] == path_to_file:
                            download_url = binary["browser_download_url"]
                            break
                    # Iniciar la descarga
                    response = requests.get(download_url, stream=True)
                    total_size = int(response.headers.get('content-length', 0))
                    progress = ttk.Progressbar(win, orient="horizontal", length=300, mode="determinate")
                    progress.pack()
                    progress["maximum"] = total_size
                    status.config(text=f"Downloading...\nVersion: {last_release}")

                    # Descargar el archivo en chunks
                    with open(path_to_file, "wb") as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            file.write(chunk)
                            progress["value"] += len(chunk)

                    # Actualizar la versión en el archivo info.json
                    with open('info.json', 'r') as f:
                        data = json.load(f)
                        data["version"] = last_release
                        data["note"] = note_version
                        data["open"] = False
                        with open('info.json', 'w') as f:
                            json.dump(data, f, indent=4)

                    messagebox.showinfo("Update", "Update completed successfully.")
                else:
                    messagebox.showinfo("Info", "You are already using the latest version.")
            else:
                raise Exception("Error getting repository information")
        else:
            raise Exception(f"Error getting repository information: {response.status_code}")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", str(e))
    finally:
        events.set()
        win.quit()
status.pack()
threading.Thread(target=download_update).start()
def close():
    events.wait()
    win.destroy()
win.protocol("WM_DELETE_WINDOW", close) 
win.mainloop()
