import requests
from tkinter import messagebox
import os

path_to_file = "dist"
url_commits = "https://api.github.com/repos/JuanMolina2001/PIDFF/commits"
url_download = "https://github.com/JuanMolina2001/PIDFF/raw/master/dist/main"
last_version_file = "assets/last.txt"

os.makedirs("assets", exist_ok=True)

def download_update(last_version):
    response = requests.get(url_download)
    if response.status_code == 200:
        with open(path_to_file, "wb") as file:
            file.write(response.content)
        print(f"Se ha actualizado el archivo '{path_to_file}' a la última versión disponible.")
        with open(last_version_file, "w") as f:
            f.write(last_version)
        messagebox.showinfo("Actualización", "La aplicación ha sido actualizada a la última versión.")
    else:
        raise Exception(f"Error downloading file '{path_to_file}': {response.status_code}")
def update_alert():
    return messagebox.askquestion("Update", "A new version is available. The update requires a restart of the application. Do you want to continue?")
def check_update():
    try:    
        response = requests.get(url_commits)
        if response.status_code == 200:
            commits = response.json()
            if commits:
                if os.path.exists(last_version_file):
                    with open(last_version_file, "r") as f:
                        current_version = f.read().strip()
                else:
                    current_version = ""
                last_version = commits[0]["sha"]
                if current_version != last_version:
                    response = update_alert()
                    if response == "yes":
                        pass
                    
                else:
                    messagebox.showinfo("Information", "No new version available.")
            else:
                messagebox.showinfo("Information", "No new version available.")
        else:
            raise Exception(f"Error getting repository information: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
if __name__ == "__main__":
    check_update()
