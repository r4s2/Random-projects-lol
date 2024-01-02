import os 
import customtkinter as ctk
from tkinter import filedialog 

window = ctk.CTk()
window.title("Minecraft Commits")
window.geometry("400x150")
window.resizable(width=False, height=False)
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("Dark")
commit_list = []
user = ""
initial_directory = f"/Users/{user}/Library/Application Support/minecraft"

def open_file_dialog():
    global user
    global initial_directory
    file_paths = filedialog.askdirectory(initialdir=initial_directory)
    temp_path_list = []
    print("Selected files:", file_paths)
    #for file_path in file_paths:
        #commit_list.append(''.join(file_path))
    commit_list.append(file_paths)
    print(commit_list)
        
def run_commits(commit_list = commit_list):
    global initial_directory 
    if len(commit_list) >= 1:
        for index, item in enumerate(commit_list):
            os.system(f"git -C '{item}' add .")
            os.system(f"git -C '{item}' commit -am 'routine save'")
            os.system(f"git -C '{item}' push")
            os.system("echo 'commits made!'")
            
def pull_new_info(): 
    global initial_directory 
    if len(commit_list) >= 1:
        for index, item in enumerate(commit_list):
            os.system(f"git -C '{item}' reset --hard")
            os.system(f"git -C '{item}' pull")
            os.system("echo 'commits saved!'")

def insert_username():
    global user
    global initial_directory
    if str(text_entry.get()) != "":
        user = text_entry.get() 
        initial_directory = f"/Users/{user}/Library/Application Support/minecraft"
    else: 
        user = "sdjgfh;sd"
    print(initial_directory)
    

text_entry = ctk.CTkEntry(window, width=150, placeholder_text="Computer Username")
submit_user = ctk.CTkButton(window, text="Enter Username", command=insert_username)
select_files = ctk.CTkButton(window, text="add Minecraft files to commit", command=open_file_dialog)
commit_button = ctk.CTkButton(window, text="commit Minecraft files", command=run_commits)
pull_button = ctk.CTkButton(window, text="pull Minecraft files", command=pull_new_info)

text_entry.grid(row=0,column=0,padx=10)
submit_user.grid(row=0,column=1,padx=10)
select_files.grid(row=3,column=0,padx=10)
commit_button.grid(row=3,column=1,padx=10)
pull_button.grid(row=4,column=1,padx=10)

window.mainloop()