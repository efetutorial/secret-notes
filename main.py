import base64
import sys
from cryptography.fernet import Fernet
import tkinter
from tkinter import messagebox

def generate_key(master_key):
    return base64.urlsafe_b64encode(master_key.ljust(32)[:32].encode())

def encrypt_message(message, master_key):
    key = generate_key(master_key)
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, master_key):
    key = generate_key(master_key)
    fernet = Fernet(key)
    try:
        decrypted_message = fernet.decrypt(encrypted_message).decode()
    except:
        decrypted_message = "Invalid Key"
    return decrypted_message

def save_note():
    try:
        title = title_entry.get()
        secret = text_entry.get("1.0", "end-1c")
        master_key = master_entry.get()

        # Boş alan kontrolü
        if not title or not secret or not master_key:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        encrypted_secret = encrypt_message(secret, master_key)
        with open("secrets.txt", "ab") as file:
            file.write(f"{title}\n".encode())
            file.write(encrypted_secret + b'\n')
        status_label.config(text=f"Note '{title}' has been saved and encrypted.")

        # Şifrelenmiş notu gösterme
        decrypted_secret = decrypt_message(encrypted_secret, master_key)
        if decrypted_secret != "Invalid Key":
            status_label.config(text="Note has been encrypted.")
        else:
            status_label.config(text="Invalid Key")
    except Exception as e:
        messagebox.showwarning("Warning", f"Error: {e}")

def decrypt_note():
    master_key = master_entry.get()
    try:
        with open("secrets.txt", "rb") as file:
            lines = file.readlines()
            if len(lines) % 2 != 0:
                status_label.config(text="Invalid secrets file format.")
                return
            for i in range(0, len(lines), 2):
                title = lines[i].strip().decode()
                encrypted_secret = lines[i+1].strip()
                decrypted_secret = decrypt_message(encrypted_secret, master_key)
                if decrypted_secret != "Invalid Key":
                    status_label.config(text=f"Decrypted note:  {decrypted_secret}")
                    return
            messagebox.showwarning("Warning", "No valid note found.")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "Secret file not found.")
    except Exception as e:
        messagebox.showwarning("Warning", f"Error: {e}")

# TK
window = tkinter.Tk()
window.geometry("300x300")
window.title("Secret Notes")

title_label = tkinter.Label(window, text="Title:")
title_label.pack()
title_entry = tkinter.Entry(window)
title_entry.pack()

text_label = tkinter.Label(window, text="Text:")
text_label.pack()
text_entry = tkinter.Text(window, height=4, width=30)
text_entry.pack()

master_label = tkinter.Label(window, text="Master Key:")
master_label.pack()
master_entry = tkinter.Entry(window)
master_entry.pack()

status_label = tkinter.Label(window)
status_label.pack()

encrypt_button = tkinter.Button(window, text="Encrypt", command=save_note)
encrypt_button.pack()

decrypt_button = tkinter.Button(window, text="Decrypt", command=decrypt_note)
decrypt_button.pack()

tkinter.mainloop()
