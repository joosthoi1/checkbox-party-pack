import gridcreation as grid
import tkinter as tk
from tkinter import messagebox as tkm
from random import randint
import keyboard
import json
class minesweeper:
    def __init__(self):
        with open('minesweeper\\config.json') as file:
            contents = json.loads(file.read())
        self.bombnumber = contents['bombs']
        self.dead = '0'
        x = contents['x']
        y = contents['y']
        self.grid2 = grid.grid(x, y, text = '  ', xoffset = 1, yoffset = 1, command=self.checkUncicked)
        self.flaglist = []
        for i in range(10000):
            self.flaglist.append(0)
        self.populate()


        self.var_states1()


    def populate(self):

        self.flagboxvar, self.label2text = tk.IntVar(), tk.StringVar()
        self.flagcheckbox = tk.Checkbutton(self.grid2.root, text = 'Flag', command=self.flagbox, var = self.flagboxvar)
        self.flagcheckbox.grid(row=0,column=0)
        label = tk.Label(self.grid2.root, text = '⚐')
        label.grid(row=0, column = int(self.grid2.numberx/2)-1)
        label2 = tk.Label(self.grid2.root, textvariable = self.label2text)
        self.label2text.set(self.bombnumber)
        label2.grid(row=0, column = int(self.grid2.numberx/2))

    def flagbox(self):
        if self.flagboxvar.get() == 1:
            self.flag = 'on'
        else:
            self.flag = 'off'

    def createfield(self):
        self.bomblist = []
        uncoordBomblist = []
        for i in range(self.bombnumber):
            while 1:
                x = randint(1, self.grid2.numberx)
                y = randint(1, self.grid2.numbery)
                if not self.grid2.coords([x, y]) in self.bomblist:
                    self.bomblist.append(self.grid2.coords([x, y]))
                    uncoordBomblist.append([x, y])
                    break
                else:
                    pass

    def numbergeneration(self):

        self.valuelist = []
        sample = self.sample
        for i in range(len(self.grid2.boxlist)):
#            print(self.bomblist)
            boxvalue = 0

            if not i in self.bomblist:
                for notI in range(8):
                    try:
                        if self.grid2.coords([self.grid2.uncoords(i)[0]+sample[notI][0], self.grid2.uncoords(i)[1]+sample[notI][1]]) in self.bomblist and self.grid2.uncoords(i)[1]+sample[notI][1] != self.grid2.numbery+1 and self.grid2.uncoords(i)[0]+sample[notI][0] != 0:
                                boxvalue += 1
                    except IndexError:
                        pass
                self.valuelist.append(boxvalue)
    #            boxlist[i].configure(boxvalue)
            else:
                self.valuelist.append(0)

    def checkUncicked(self):
        self.flagsplaced = 0

        colordict = {
        0 : 'white smoke',
        1 : 'royalblue1',
        2 : 'green4',
        3: 'red3',
        4:'dark orchid',
    	5:'hot pink',
    	6:'yellow',
    	7:'MediumPurple4',
    	8:'turquoise1'
        }
        again = False
        if self.flag == 'off':
            checkedlist = []
            for i in range(len(self.grid2.varlist)):
                if self.grid2.varlist[i].get() == 0:

                    self.flaglist[i] = 0
                    self.grid2.boxlist[i].configure(bg='light gray')

                if self.grid2.varlist[i].get() == 1 and self.flaglist[i] != 1:

                    checkedlist.append(0)
                    if i in self.bomblist:
                        self.grid2.boxlist[i].configure(state='disabled', disabledforeground='black')
                        self.dead = '1'
                    else:
                        self.grid2.boxlist[i].configure(text=self.valuelist[i], state='disabled', disabledforeground=colordict[self.valuelist[i]])
                        if self.valuelist[i] == 0:

                            for notI in range(8):
                                try:
#                                    print(self.grid2.coords([self.grid2.uncoords(i)[0]+self.sample[notI][0], self.grid2.uncoords(i)[1]+self.sample[notI][1]]))
                                    if self.grid2.varlist[self.grid2.coords([self.grid2.uncoords(i)[0]+self.sample[notI][0], self.grid2.uncoords(i)[1]+self.sample[notI][1]])].get() == 0 and self.grid2.uncoords(i)[1]+self.sample[notI][1] != self.grid2.numbery+1 and self.grid2.uncoords(i)[0]+self.sample[notI][0] != 0:
                                        self.grid2.varlist[self.grid2.coords([self.grid2.uncoords(i)[0]+self.sample[notI][0], self.grid2.uncoords(i)[1]+self.sample[notI][1]])].set(1)
                                        self.grid2.boxlist[self.grid2.coords([self.grid2.uncoords(i)[0]+self.sample[notI][0], self.grid2.uncoords(i)[1]+self.sample[notI][1]])].configure(state='disabled', disabledforeground=colordict[self.valuelist[self.grid2.coords([self.grid2.uncoords(i)[0]+self.sample[notI][0], self.grid2.uncoords(i)[1]+self.sample[notI][1]])]])
                                        again = True
                                except IndexError as e:

                                    pass
                if len(checkedlist) == self.grid2.numberx*self.grid2.numbery-len(self.bomblist) and self. dead != '1':
                    self.dead = '2'
        if again:
#            self.grid2.root.update()
            self.checkUncicked()
        if self.flag == 'on':
            for i in range(len(self.grid2.varlist)):
                if self.grid2.varlist[i].get() == 0:
                    self.flaglist[i] = 0
                    self.grid2.boxlist[i].configure(bg='light gray')

                    self.label2text.set(self.bombnumber-self.flagsplaced)
                if self.grid2.varlist[i].get() == 1 and self.grid2.boxlist[i]['state'] != 'disabled':
                    self.flaglist[i] = 1
                    self.grid2.boxlist[i].configure(bg='red')

                self.flagsplaced = 0
                for i in self.flaglist:
                    if i == 1:
                        self.flagsplaced += 1
                self.label2text.set(self.bombnumber-self.flagsplaced)

    def var_states1(self):

        self.sample = [
        [-1, 1], [0, 1], [1, 1],
        [-1, 0],         [1, 0],
        [-1, -1], [0, -1], [1, -1]
        ]
        self.createfield()
    #    for i in bomblist:
    #        boxlist[i].select()
        self.numbergeneration()
        self.flagbox()
        while 1:

            #self.checkUncicked()

            if self.dead == '1':
                self.dead = 0
                tkm.showinfo('Game Over', 'You exploded into a million pieces :(')
                self.recreate()
                break
            if self.dead == '2':
                self.dead = 0
                tkm.showinfo('Game Over', 'YOU WIN!!!!')
                self.recreate()
                break
            if (keyboard.is_pressed('space')):
                self.flagcheckbox.invoke()
                self.grid2.root.update()
                while 1:
                    if not (keyboard.is_pressed('space')):
                        break
            try:
                self.grid2.root.update()
            except:
                return

    def recreate(self):
        self.label2text.set(self.bombnumber)
        self.clearall()
        self.var_states1()

    def clearall(self):
        for i in self.grid2.boxlist:
            i.deselect()
            i.configure(state='normal', bg='light gray', fg = 'black', text="  ")

class config:

    def __init__(self):
        from functools import partial


        with open('minesweeper\\config.json') as file:
            self.contents = json.loads(file.read())
        self.root = tk.Toplevel()
        self.varx = tk.IntVar()
        self.vary = tk.IntVar()
        self.varbombs = tk.IntVar()
        tk.Label(self.root,text='x').grid(row = 0, column=0,sticky='w')
        tk.Label(self.root,text='y').grid(row = 1, column=0,sticky='w')
        tk.Label(self.root,text='bombs').grid(row = 2, column=0,sticky='w')
        tk.Entry(self.root,width=3,textvariable=self.varx).grid(row = 0, column=1,sticky='w')
        tk.Entry(self.root,width=3,textvariable=self.vary).grid(row = 1, column=1,sticky='w')
        tk.Entry(self.root,width=3,textvariable=self.varbombs).grid(row = 2, column=1,sticky='w')
        self.varx.set(self.contents['x'])
        self.vary.set(self.contents['y'])
        self.varbombs.set(self.contents['bombs'])
        tk.Button(self.root,text='randomize',command=partial(self.randomize, 'x'),padx=10).grid(row = 0, column=2,sticky='e')
        tk.Button(self.root,text='randomize',command=partial(self.randomize, 'y'),padx=10).grid(row = 1, column=2,sticky='e')
        tk.Button(self.root,text='randomize',command=partial(self.randomize, 'bombs'),padx=10).grid(row = 2, column=2,sticky='e')
        tk.Button(self.root,text='randomize all',command=partial(self.randomize, 'all')).grid(row = 3, column=0,sticky='e')
        tk.Button(self.root,text='done',command=self.done).grid(row = 3, column=2,sticky='e')
        self.root.mainloop()
    def randomize(self, button):
        import random
        if button == "x":
            self.varx.set(random.randint(1,100))
        if button == "y":
            self.vary.set(random.randint(1,100))
        if button == "bombs":
            self.varbombs.set(random.randint(1,100))
        if button == "all":
            self.varx.set(random.randint(1,100))
            self.vary.set(random.randint(1,100))
            self.varbombs.set(random.randint(1,100))
    def done(self):
        if not self.varx.get() or not self.vary.get() or not self.varbombs.get():
            tk.messagebox.showwarning(message="Please make sure no value is 0")

        elif self.varx.get() * self.vary.get() <= self.varbombs.get():
            tk.messagebox.showwarning(message="Please make sure there's enough room for the bombs")
        else:
            self.contents['x'] = self.varx.get()
            self.contents['y'] = self.vary.get()
            self.contents['bombs'] = self.varbombs.get()
            with open('minesweeper\\config.json', 'w') as file:
                file.write(json.dumps(self.contents))
            self.root.destroy()

if __name__ == "__main__":
#    minesweeper()
    config()
