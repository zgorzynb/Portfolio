from future.moves.tkinter import *
from word import Word

root = Tk()
root.geometry("1400x800")
app = Word(master=root)
app.mainloop()
root.destroy()
