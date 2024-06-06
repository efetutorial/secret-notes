import base64
import sys
from cryptography.fernet import Fernet

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
    title = input("Enter your title: ")
    secret = input("Enter your secret: ")
    master_key = input("Enter master key: ")
    encrypted_secret = encrypt_message(secret, master_key)
    with open(f"{title}.txt", "wb") as file:
        file.write(encrypted_secret)
    print(f"Note '{title}' has been saved and encrypted.")

def decrypt_note():
    title = input("Enter your title: ")
    master_key = input("Enter master key: ")
    try:
        with open(f"{title}.txt", "rb") as file:
            encrypted_secret = file.read()
        decrypted_secret = decrypt_message(encrypted_secret, master_key)
        print(f"Decrypted note: {decrypted_secret}")
    except FileNotFoundError:
        print(f"No note found with title '{title}'.")

def main():
    while True:
        print("1. Save & Encrypt Note")
        print("2. Decrypt Note")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            save_note()
        elif choice == '2':
            decrypt_note()
        elif choice == '3':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()