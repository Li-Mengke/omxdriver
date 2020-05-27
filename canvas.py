import tkinter
import subprocess

root = tkinter.Tk()
root.config(bg = 'black')
root.attributes('-fullscreen', True)
canvas1 = tkinter.Canvas(root, width = 200, height = 200, background = 'black')
canvas2 = tkinter.Canvas(root, width = 200, height = 200)
canvas1.place(x=0, y = 0)
canvas2.place(x=200, y = 0)
tkinter.mainloop()





