import gridcreation as gc
import tkinter as tk
import time
import json
try:
    import displayboard.ascii as ascii
except:
    import ascii

#'a!"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
#test sentence ^^

class board:
    def __init__(self):
        self.grid = gc.grid_reverse(40,8)
        self.root = self.grid.root
        with open('displayboard\\config.json') as file:
            self.contents = json.loads(file.read())

        self.string = self.contents['text']
        self.string += ' '
        self.nextLetter = True
        self.letter = 0
        self.letterIndex = 0
        self.blank = False
        while True:
            try:
                self.nextFrame()
                self.root.update()
                time.sleep(0.1)
                self.moveLeft()
            except:
                break



    def nextFrame(self):
        if self.nextLetter and not self.blank:
            self.loaded = ascii.letters[self.string[self.letter]]
            self.letter += 1
            self.nextLetter = False
            if self.letter == len(self.string):
                self.letter = 0


        for i in range(self.grid.numbery):
            if self.loaded[self.letterIndex][i]:
                box = self.grid.boxlist[
                    self.grid.coords(self.grid.numberx, i+1)
                ]
                box.select()
                box.configure(bg='black')

        self.letterIndex += 1
        if self.letterIndex == len(self.loaded):
            self.letterIndex = 0
            self.nextLetter = True
            if not self.blank:
                self.loaded = ascii.letters['blank']
                self.blank = True
            else:
                self.blank = False



    def mainloop(self):
        while 1:
            self.nextFrame()
            self.moveLeft()

    def moveLeft(self):
        to_clear = []
        moved = []
        for c, i in enumerate(self.grid.varlist):
            if i.get():
                to_clear.append(c)
                uncoords = self.grid.uncoords(c)
                if not uncoords[0] == 1:
                    moved.append(
                        (self.grid.uncoords(c)[0]-1, self.grid.uncoords(c)[1])
                    )
        for i in to_clear:
            box = self.grid.boxlist[i]
            box.deselect()
            box.configure(bg='light grey')
        for i in moved:
            box = self.grid.boxlist[self.grid.coords(i)]
            box.select()
            box.configure(bg='black')

class config:
    def __init__(self):
        from functools import partial

        with open('displayboard\\config.json') as file:
            self.contents = json.loads(file.read())
        self.root = tk.Tk()
        self.textvar = tk.StringVar

        tk.Label(self.root,text='text: ').grid(row = 0, column=0,sticky='nw')
        textbox = tk.Text(self.root,height=3,width=30)
        textbox.grid(row=0,column=1,sticky='w')

        textbox.insert(tk.END, self.contents['text'])

        self.root.mainloop()



if __name__ == "__main__":
    board()
#    config()
