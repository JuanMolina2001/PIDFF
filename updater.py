import requests
from tkinter import messagebox
import json
info = json.load(open("info.json"))
path_to_file = info["path_to_file"]
url_commits = f"{info['url']}/commits"
url_download = f"{info['url']}/raw/master/{path_to_file}"
current_version = info["version"]
current_hash = info["hash"]
def download_update(last_hash):
    response = requests.get(url_download)
    if response.status_code == 200:
        with open(path_to_file, "wb") as file:
            file.write(response.content)
        print(f"Se ha actualizado el archivo '{path_to_file}' a la última versión disponible.")
        with open("info.json", "w") as f:
            f.write(json.dumps({"hash": last_hash}))
        messagebox.showinfo("Actualización", "La aplicación ha sido actualizada a la última versión.")
    else:
        messagebox.showerror("Error", f"Error downloading file '{path_to_file}': {response.status_code}")

def check_update():
    try:    
        response = requests.get(url_commits)
        if response.status_code == 200:
            commits = response.json()
            if commits:
                last_hash = commits[0]["sha"]
                if current_hash != last_hash:
                    response = messagebox.askquestion("Update", "A new version is available. The update requires a restart of the application. Do you want to continue?")
                    if response == "yes":
                        download_update(last_hash)
                else:
                    messagebox.showinfo("Information", "No new version available.")
            else:
                messagebox.showinfo("Information", "No new version available.")
        else:
            raise Exception(f"Error getting repository information: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
