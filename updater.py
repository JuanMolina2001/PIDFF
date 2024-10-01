import requests
from tkinter import ttk, messagebox
import tkinter as tk
import json
win = tk.Tk()
win.geometry("300x100")
win.resizable(False, False)
win.title("Update")
info = json.load(open("info.json"))
path_to_file = 'main.exe'
url_commits = f"https://api.github.com/repos/{info['url']}/commits"
url_download = f"https://github.com/{info['url']}/raw/master/dist/main.exe"
current_version = info["version"]
current_commit = info["commit"]
status = tk.Label(win, text=f"Start Updating...\nCurrent version: {current_version}\nLast commit: {current_commit}")
def get_version():
    response = requests.get(f"https://api.github.com/repos/{info['url']}/releases/latest")
    if response.status_code == 200:
        try:
            release = response.json()
        except:
            raise Exception("Error getting file")
        if release:
            return release["tag_name"]
        else:
            raise Exception("Error getting repository information")
    else:
        raise Exception(f"Error getting repository information: {response.status_code}")
    
def download_update(last_commit:str):
    status["text"] = f"Downloading update...\nCurrent version: {current_version}\nLast commit: {current_commit}"
    response = requests.get(url_download)
    if response.status_code == 200:
        progress = ttk.Progressbar(win, orient="horizontal", length=300, mode="determinate")
        progress.pack()
        progress["maximum"] = response.headers["Content-Length"]
        progress["value"] = 0
        progress.start()
        with open(path_to_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                progress["value"] += len(chunk)
                progress.update()
                file.write(chunk)
        progress.stop()
        try:
            version = get_version()
        except Exception as e:
            print("Error getting version")
        with open("info.json", "w") as f:
            info["commit"] = last_commit
            info["version"] = version
            f.write(json.dumps(info,indent=4))
        messagebox.showinfo("Update", f"Update completed. Restart the application to apply the changes.")
    else:
        messagebox.showerror("Error", f"Error downloading file '{path_to_file}': {response.status_code}")

def check_update():
    try:    
        status["text"] = f"Checking for updates...\nCurrent version: {current_version}\nLast commit: {current_commit}"
        response = requests.get(url_commits)
        if response.status_code == 200:
            try:
                commits = response.json()
            except:
                raise Exception("Error getting file")
            if commits:
                last_commit = commits[0]["sha"]
                if current_commit!= last_commit:
                    download_update(last_commit)
                else:
                    messagebox.showinfo("Information", "No new version available.")
            else:
                messagebox.showinfo("Information", "No new version available.")
        else:
            raise Exception(f"Error getting repository information: {response.status_code}")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", str(e))
    finally:
        win.destroy()
status.pack()
win.after(1000, check_update)
win.mainloop()
