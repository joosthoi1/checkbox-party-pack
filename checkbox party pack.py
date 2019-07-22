import tkinter as tk
import tetris.tetris as tetris
import minesweeper.minesweeper as minesweeper
import imgtocheck.imgtocheck as imgtocheck
import snake.snake as snake
import displayboard.displayboard as DisplayBoard
import giftocheck.giftocheck as giftocheck
from functools import partial
import json
import PIL.Image
import PIL.ImageTk


class main:
    def __init__(self):
        self.root = tk.Tk()
        self.add_scrollbar()

        self.framelist = []
        self.innerframelist = []
        self.imglist = []

        self.mainframe(0,0)
        self.mainframe(1,0)
        self.mainframe(2,0)
        self.mainframe(0,1)
        self.mainframe(1,1)
        self.mainframe(2,1)

        self.imagelabel(0, 'Tetris', "tetris/Tetrislogo.png")
        self.imagelabel(1, 'Minesweeper', "tetris/Tetrislogo.png")
        self.imagelabel(2, 'Snake', "tetris/Tetrislogo.png")
        self.imagelabel(3, 'Imgtocheck', "tetris/Tetrislogo.png")
        self.imagelabel(4, 'Display Board', "tetris/Tetrislogo.png")
        self.imagelabel(5, 'Giftocheck', "tetris/Tetrislogo.png")

        self.root.mainloop()




    def mainframe(self, col, row):
        col *= 2
        row *= 2
        if col and not row:
            self.verticalspacer(col - 1, row)
        if row and not col:
            self.horizontalspacer(col, row - 1)
        self.framelist.append(
        tk.Frame(self.frame)
        )
        self.framelist[-1].grid(row=row,column=col)

    def verticalspacer(self,col1,row1):
        self.frame1 = tk.Frame(self.frame, width = 20,height= 250)
        self.frame1.grid(row=row1,column=col1)

    def horizontalspacer(self,col1,row1):
        self.frame1 = tk.Frame(self.frame, width = 400,height= 20)
        self.frame1.grid(row=row1,column=col1)

    #

    def imagelabel(self, index, name, image):
        tk.Label(self.framelist[index], text = name, font = ("Helvetica", "16")).pack()
        im = PIL.Image.open(image)
        photo = PIL.ImageTk.PhotoImage(im)

        self.imglist.append(photo)
        tk.Label(self.framelist[index], image = self.imglist[-1]).pack()

        innerframe = tk.Frame(self.framelist[index], width=200)
        innerframe.pack()
        tk.Button(
            innerframe,
            text='start',
            command = partial(self.load, name)
        ).pack(side='left')
        tk.Button(innerframe, text='⚙', command = partial(self.config, name)).pack(side='right')

    def add_scrollbar(self):
        self.canvas = tk.Canvas(self.root, borderwidth=0, width=1050,height=740)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(
            (4,4),
            window=self.frame,
            anchor="nw",
            tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load(self, name):
        if name == 'Tetris':
            self.root.destroy()
            tetris.tetris()
            main()
        if name == 'Minesweeper':
            self.root.destroy()
            minesweeper.minesweeper()
            main()
        if name == 'Snake':
            self.root.destroy()
            snake.snake()
            main()
        if name == 'Imgtocheck':
            self.root.destroy()
            imgtocheck.imgtocheck()
            main()
        if name == 'Display Board':
            self.root.destroy()
            DisplayBoard.board()
            main()
        if name == 'Giftocheck':
            self.root.destroy()
            giftocheck.giftocheck()
            main()
    def config(self, name):
        if name == 'Minesweeper':
            minesweeper.config()
        if name == 'Snake':
            snake.config()
        if name == 'Imgtocheck':
            imgtocheck.config()
        if name == 'Display Board':
            DisplayBoard.config()
        if name == 'Giftocheck':
            giftocheck.config()


if __name__ == '__main__':
    main()
