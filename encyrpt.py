import base64
import sys
from cryptography.fernet import Fernet
import tkinter


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
    title = title_entry.get()
    secret = text_entry.get()
    master_key = master_entry.get()
    encrypted_secret = encrypt_message(secret, master_key)
    with open("secrets.txt", "ab") as file:
        file.write(f"{title}\n".encode())
        file.write(encrypted_secret + b'\n')
    durum_label.config(text=f"Note '{title}' has been saved and encrypted.")

    # Text ve master doğru girilmişse şifrelenmiş notu göster
    decrypted_secret = decrypt_message(encrypted_secret, master_key)
    if decrypted_secret != "Invalid Key":
        durum_label.config(text=f"Encrypted note")
    else:
        durum_label.config(text="Invalid Key")

def decrypt_note():
    master_key = master_entry.get()
    try:
        with open("secrets.txt", "rb") as file:
            lines = file.readlines()
            if len(lines) % 2 != 0:
                durum_label.config(text="Invalid secrets file format.")
                return
            for i in range(0, len(lines), 2):
                title = lines[i].strip().decode()
                encrypted_secret = lines[i+1].strip()
                decrypted_secret = decrypt_message(encrypted_secret, master_key)
                if decrypted_secret != "Invalid Key":
                    durum_label.config(text=f"Decrypted note:  {decrypted_secret}")
                    return
            durum_label.config(text="No valid note found.")
    except FileNotFoundError:
        durum_label.config(text="No secrets file found.")




#TK
window = tkinter.Tk()
window.geometry("300x300")
window.title("Secret Notes")

title_label = tkinter.Label(window, text="Title:")
title_label.pack()
title_entry = tkinter.Entry(window)
title_entry.pack()

text_label = tkinter.Label(window, text="Text:")
text_label.pack()
text_entry = tkinter.Entry(window)
text_entry.pack()

master_label = tkinter.Label(window, text="Master:")
master_label.pack()
master_entry = tkinter.Entry(window)
master_entry.pack()

durum_label = tkinter.Label(window)
durum_label.pack()



button = tkinter.Button(window, text="Encyrpt", command=save_note)
button.pack()

button_de = tkinter.Button(window, text="Decyrpt", command=decrypt_note)
button_de.pack()

tkinter.mainloop()
