import tkinter
from PIL import ImageTk, Image

# Window
window = tkinter.Tk()
window.geometry("350x500")
window.title("Secret Notes")

# Image
img = Image.open("img.png")
img = img.resize((120, 120))
photo = ImageTk.PhotoImage(img)

# Label
# Label
label = tkinter.Label(window, image=photo)
label.place(x=66,y=77)
label.pack()


tkinter.mainloop()
