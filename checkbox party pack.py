import tkinter as tk
import tetris.tetris as tetris
import minesweeper.minesweeper as minesweeper
import imgtocheck.imgtocheck as imgtocheck
import snake.snake as snake
import displayboard.displayboard as DisplayBoard
from functools import partial
import json


class main:
    def __init__(self):
        self.root = tk.Tk()
        self.framelist = []
        self.innerframelist = []
        self.imglist = []

        self.mainframe(0,0)
        self.verticalspacer(0,1)
        self.mainframe(0,2)
        self.verticalspacer(0,3)
        self.mainframe(0,4)
        self.horizontalspacer(1,0)
        self.mainframe(2,0)
        self.verticalspacer(2,1)
        self.mainframe(2,2)
        self.imagelabel(0, 'Tetris', "tetris\\Tetrislogo.png")
        self.imagelabel(1, 'Minesweeper', "tetris\\Tetrislogo.png")
        self.imagelabel(2, 'Snake', "tetris\\Tetrislogo.png")
        self.imagelabel(3, 'Imgtocheck', "tetris\\Tetrislogo.png")
        self.imagelabel(4, 'Display Board', "tetris\\Tetrislogo.png")


        self.root.mainloop()

    def mainframe(self, row1, col1):
        self.framelist.append(
        tk.Frame(self.root)
        )
        self.framelist[-1].grid(row=row1,column=col1)

    def verticalspacer(self,row1,col1):
        self.frame1 = tk.Frame(self.root, width = 20,height= 250)
        self.frame1.grid(row=row1,column=col1)

    def horizontalspacer(self,row1,col1):
        self.frame1 = tk.Frame(self.root, width = 400,height= 20)
        self.frame1.grid(row=row1,column=col1)

    #

    def imagelabel(self, index, name, image):
        tk.Label(self.framelist[index], text = name, font = ("Helvetica", "16")).pack()


        self.imglist.append(tk.PhotoImage(file=image))
        tk.Label(self.framelist[index], image = self.imglist[-1]).pack()

        innerframe = tk.Frame(self.framelist[index], width=200)
        innerframe.pack()
        tk.Button(
            innerframe,
            text='start',
            command = partial(self.load, name)
        ).pack(side='left')
        tk.Button(innerframe, text='⚙', command = partial(self.config, name)).pack(side='right')

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
    def config(self, name):
        if name == 'Minesweeper':
            minesweeper.config()
        if name == 'Snake':
            snake.config()
        if name == 'Imgtocheck':
            imgtocheck.config()
        if name == 'Display Board':
            DisplayBoard.config()


if __name__ == '__main__':
    main()
