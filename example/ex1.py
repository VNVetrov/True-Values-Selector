import tkinter as tk

def close_this(w: tk.Toplevel):
    w.destroy()
    w.update()
    ws.destroy()

def New_Window():
    Window = tk.Toplevel()
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
    canvas.pack()
    button2 = tk.Button(Window, text="close", command=lambda: close_this(Window))
    button2.pack()


HEIGHT = 300
WIDTH = 500

ws = tk.Tk()
ws.title("Python Guides")
canvas = tk.Canvas(ws, height=HEIGHT, width=WIDTH)
canvas.pack()


button = tk.Button(ws, text="Click ME", bg='White', fg='Black',
                   command=lambda: New_Window())

button.pack()
ws.mainloop()