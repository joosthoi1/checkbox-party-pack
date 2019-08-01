from gridcreation import grid_reverse as grid
import tkinter as tk
import tetris.holdcoords as holdcoords
import time
import random
from tkinter import messagebox

class tetris:
    def __init__(self):
        self.bgcolor = 'gainsboro'
        self.grid1 = grid(20,20)
        self.grid1.numberx = 10
        self.varnaming()
        self.nextlist = []
        self.holding = ''
        self.groundlist = []
        self.groundcolor = {}
        self.root.title('Tetris')
        for i in self.boxlist:
            i.configure(state="disabled")
        for i in self.boxlist:
            i.configure(bg=self.bgcolor)
        self.nextblocksetup()
        self.colordict = {
            'block_cube':'gold',
            'block_s':'chartreuse2',
            'block_s_2':'red2',
            'block_l':'SlateBlue1',
            'block_l_2':'dark orange',
            'block_i':'cyan',
            'block_t':'magenta2',
        }
        self.loaded = []

        self.root.focus_force()
        self.root.bind('<Left>', self.moveleft)
        self.root.bind('a', self.moveleft)
        self.root.bind('<Right>', self.moveright)
        self.root.bind('d', self.moveright)
        self.root.bind('<Down>', self.movedown)
        self.root.bind('s', self.movedown)
        self.root.bind('q', self.rotatel)
        self.root.bind('e', self.rotater)
        self.root.bind('<space>', self.holdblock)
        self.root.bind('<Up>', self.down_all)
        self.root.bind('w', self.down_all)


        self.createblock()
        self.load()
        self.frame = 0
        self.groundcount = 0
        self.main()

    def down_all(self, event=None):
        self.unload()
        for i in range(self.grid1.numbery):
            self.movedown()
        self.load()
        self.groundify()

    def holdblock(self, event=None):
        self.unload()
        if not self.holdlimit:
            if not self.holding:
                self.holding = self.blocktype
                self.createblock()

            else:
                self.customunload(holdcoords.holdcoords[self.holding])
                blockdict = {
                    'block_cube':[[5, 2], [5, 1], [6, 2], [6, 1]],
                    'block_s':[[6, 2], [5, 2], [4, 1], [5, 1]],
                    'block_s_2':[[4, 2], [5, 2],[6, 1],[5, 1]],
                    'block_l':[[4, 2], [4, 1],[6, 1],[5, 1]],
                    'block_l_2':[[6, 2], [4, 1], [6, 1], [5, 1]],
                    'block_i':[[4, 1], [7, 1], [6, 1], [5, 1]],
                    'block_t':[[4, 1], [6, 1],[5, 2], [5, 1]],
                }

                self.holding, self.blocktype = self.blocktype, self.holding
                self.loaded = blockdict[self.blocktype]
                self.curcolor = self.colordict[self.blocktype]
            self.customload(holdcoords.holdcoords[self.holding], self.colordict[self.holding])
            self.holdlimit += 1
        self.load()


    def nextblocksetup(self):
        x = 0
        y = 1
        for i in self.boxlist:
            if x == 10 or x == 15:
                i.configure(bg = 'black')
            if ((y == 5 or y == 20 or y == 15) and x >= 10) or (y == 10 and x>=15):
                i.configure(bg = 'black')
            x += 1
            if x == 20:
                x = 0
                y += 1
        for i in holdcoords.nextcoords:
            self.nextlist.append(random.choice(list(i)))

    def customload(self, loadlist, color):
        for i in loadlist:
            self.boxlist[self.coords(i)].configure(bg = color)

    def customunload(self, loadlist):
        for i in loadlist:
            self.boxlist[self.coords(i)].configure(bg = self.bgcolor)

    def varnaming(self):
        self.root = self.grid1.root
        self.boxlist = self.grid1.boxlist
        self.coords = self.grid1.coords
        self.uncoords = self.grid1.uncoords
        self.numbery = self.grid1.numbery
        self.numberx = self.grid1.numberx
        self.varlist = self.grid1.varlist

    def main(self):
        if self.frame == 10:
            self.unload()
            self.movedown()
            self.load()
            self.frame = 0
        self.frame += 1
        if self.groundcount >= 4:
            self.groundify()
        self.checkclearline()
        self.root.after(40, self.main)

    def loadgrd(self):
        for i in self.groundlist:
            coord = self.coords(i)
            color = self.groundcolor[coord]
            self.boxlist[coord].configure(bg=color)

    def unloadgrd(self):
        for i in self.groundlist:
            coord = self.coords(i)
            self.boxlist[coord].configure(bg=self.bgcolor)

    def groundify(self):
        self.groundcount = 0
        self.groundlist = self.groundlist + [(i) for i in self.loaded]
        for i in self.loaded:
            self.groundcolor[self.coords(i)] = self.curcolor
        self.createblock()
        self.load()

    def createblock(self):
        self.holdlimit = 0
        blockdict = {
            'block_cube':[[5, 2], [5, 1], [6, 2], [6, 1]],
            'block_s':[[6, 2], [5, 2], [4, 1], [5, 1]],
            'block_s_2':[[4, 2], [5, 2],[6, 1],[5, 1]],
            'block_l':[[4, 2], [4, 1],[6, 1],[5, 1]],
            'block_l_2':[[6, 2], [4, 1], [6, 1], [5, 1]],
            'block_i':[[4, 1], [7, 1], [6, 1], [5, 1]],
            'block_t':[[4, 1], [6, 1],[5, 2], [5, 1]],
        }

        self.loaded = []
        self.blocktype = self.nextlist[0]
        self.curcolor = self.colordict[self.blocktype]
        if not any(i in self.groundlist for i in blockdict[self.blocktype]):
            for i in blockdict[self.blocktype]:
                self.loaded.append(i)
        else:
            self.end()
            return

        nextcoords = holdcoords.nextcoords
        for counter, i in enumerate(self.nextlist):
            self.customunload(nextcoords[counter][i])
        self.nextlist.pop(0)
        self.nextlist.append(random.choice(list(nextcoords[-1])))
        for counter, i in enumerate(self.nextlist):
            self.customload(nextcoords[counter][i], self.colordict[i])

    def end(self):
        messagebox1 = tk.messagebox.askquestion('Game Over', f'Game Over\nWould you like to play again?')
        if messagebox1 == 'yes':
            self.root.destroy()
            tetris()
        else:
            self.root.destroy()

    def rotatel(self, event=None):
        self.unload()
        if not self.blocktype == 'block_cube':
            templist = []
            px = self.loaded[3][0]
            py = self.loaded[3][1]
            for i in self.loaded.copy():
                templist.append([i[1] + px - py, px + py - i[0]])
            boundingtestx = any(self.numberx < i[0] or i[0] < 1 for i in templist)
            boundingtesty = any(1 > i[1] or i[1] > self.numbery for i in templist)
            collision = any(i in self.groundlist for i in templist)
            if not boundingtestx and not boundingtesty and not collision:
                self.loaded = templist
        self.load()

    def rotater(self, event=None):
        self.unload()
        if not self.blocktype == 'block_cube':
            templist = []
            px = self.loaded[3][0]
            py = self.loaded[3][1]
            for i in self.loaded.copy():
                templist.append([px + py - i[1], i[0] + py - px])
            boundingtestx = any(self.numberx < i[0] or i[0] < 1 for i in templist)
            boundingtesty = any(1 > i[1] or i[1] > self.numbery for i in templist)
            collision = any(i in self.groundlist for i in templist)
            if not boundingtestx and not boundingtesty and not collision:
                self.loaded = templist
        self.load()

    def load(self):
        for i in self.loaded:
            coord = self.coords(i)
            self.boxlist[coord].configure(bg=self.curcolor)


    def unload(self):
        for i in self.loaded:
            coord = self.coords(i)
            self.boxlist[coord].configure(bg=self.bgcolor)

    def movedown(self, event=None):
        self.unload()
        ground1 = [list(i) for i in self.groundlist]
        for i in range(len(self.groundlist)):
            ground1[i][1] -= 1
        if not any(i[1] >= self.grid1.numbery for i in self.loaded) and not any(i in ground1 for i in self.loaded):
            for i in range(len(self.loaded)):
                self.loaded[i][1] += 1
                self.groundcount = 0
        else:
            self.groundcount += 1
        self.load()

    def mvground(self, linenmb):
        linelist = [[] for i in range(self.numbery)]
        for i in self.groundlist:
            linelist[i[1]-1].append(i)
        for y in linelist[:linenmb][::-1]:
            ground1 = [list(i) for i in self.groundlist]
            for i in range(len(self.groundlist)):
                ground1[i][1] -= 1
            if not any(i[1] == self.grid1.numbery for i in y) and not any(i in ground1 for i in y):
                for i in range(len(y)):
                    coord = self.coords(y[i])
                    tempcolor = self.groundcolor[coord]
                    self.groundcolor.pop(coord)
                    y[i][1] += 1
                    self.groundcolor[self.coords(y[i])] = tempcolor

    def moveup(self, event=None):  # dev
        self.unload()
        ground1 = [list(i) for i in self.groundlist]
        for i in range(len(self.groundlist)):
            ground1[i][1] += 1
        if not any(i[1] <= 1 for i in self.loaded) and not any(i in ground1 for i in self.loaded):

            for i in range(len(self.loaded)):

                self.loaded[i][1] -= 1
        self.load()

    def moveleft(self, event=None):
        self.unload()
        ground1 = [list(i) for i in self.groundlist]
        for i in range(len(self.groundlist)):
            ground1[i][0] += 1
        if not any(i[0] <= 1 for i in self.loaded) and not any(i in ground1 for i in self.loaded):
            for i in range(len(self.loaded)):
                self.loaded[i][0] -= 1
        self.load()


    def moveright(self, event=None):
        self.unload()
        ground1 = [list(i) for i in self.groundlist]
        for i in range(len(self.groundlist)):
            ground1[i][0] -= 1
        if not any(i[0] >= self.grid1.numberx for i in self.loaded) and not any(i in ground1 for i in self.loaded):
            for i in range(len(self.loaded)):
                self.loaded[i][0] += 1
        self.load()

    def checkclearline(self):
        templist = [[] for i in range(self.numbery)]
        for y in range(1, self.numbery+1):
            for i in self.groundlist:
                if i[1] == y:
                    templist[y-1].append(i)
            if len(templist[y-1]) == self.numberx:
                self.unloadgrd()
                for i2 in templist[y-1]:
                    self.groundlist.remove(i2)
                    self.groundcolor.pop(self.coords(i2))
                self.mvground(y)
                self.loadgrd()
if __name__ == "__main__":
    try:
        tetris()
    except TclError or KeyError:
        Quit()
