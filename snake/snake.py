from gridcreation import grid
from random import randint
from tkinter import messagebox as tkm
import keyboard,time
import tkinter as tk
import json

class snake:

    def __init__(self):
        with open('snake/config.json') as file:
            contents = json.loads(file.read())
        x = contents['x']
        y = contents['y']
        self.tickspeed = contents['tickspeed']
        self.deathonwall = contents['deathonwall']
        self.grid1 = grid(x,y)
        self.grid1.root.title('Snake')
        self.main()

    def main(self):
        y, x = int(self.grid1.numbery/2), 1
        bodylength = 3
        dir = 'Right'
        dirrn = 'Right'
        fruitneeded = False
        snake_body = []
        tick = 0
        needfruit = True
        while 1:

            if (keyboard.is_pressed('w') or keyboard.is_pressed('up')) and dirrn != 'Down':  # if key 'q' is pressed
                dir = 'Up'
            elif (keyboard.is_pressed('s') or keyboard.is_pressed('down')) and dirrn != 'Up':  # if key 'q' is pressed
                dir = 'Down'
            elif (keyboard.is_pressed('a') or keyboard.is_pressed('left')) and dirrn != 'Right':  # if key 'q' is pressed
                dir = 'Left'
            elif (keyboard.is_pressed('d') or keyboard.is_pressed('right')) and dirrn != 'Left':  # if key 'q' is pressed
                dir = 'Right'
            if tick == 3:
                dirrn = dir

                if needfruit:
                    while 1:
                        randcoordsx, randcoordsy = randint(1, self.grid1.numberx), randint(1, self.grid1.numbery)
                        if self.grid1.coords(randcoordsx,randcoordsy) in snake_body:
                            pass
                        else:
                            fruitplace = self.grid1.coords(randcoordsx,randcoordsy)
                            try:
                                self.grid1.boxlist[self.grid1.coords(randcoordsx,randcoordsy)].select()
                                self.grid1.boxlist[self.grid1.coords(randcoordsx,randcoordsy)].configure(bg='red', fg='red')
                            except:
                                return
                            needfruit = False
                            break
                tick = 0
                try:
                    self.grid1.boxlist[self.grid1.coords(x, y)].select()
                    self.grid1.boxlist[self.grid1.coords(x, y)].configure(foreground='green',bg='light gray')
                except:
                    return
                if len(snake_body) >= bodylength:
                    snake_body.insert(0, self.grid1.coords(x, y))
                    self.grid1.boxlist[snake_body[-1]].deselect()
                    self.grid1.boxlist[snake_body[-1]].configure(foreground='black')
                    snake_body.pop(-1)
                else:
                    snake_body.insert(0, self.grid1.coords(x, y))
                if snake_body[0] == fruitplace:
                    bodylength += 1
                    needfruit = True
                if dir == 'Right':
                    x+=1
                if dir == 'Left':
                    x-=1
                if dir == 'Up':
                    y+=1
                if dir == 'Down':
                    y-=1
                try:
                    self.grid1.root.update()
                except Exception:
                    pass
                if x == self.grid1.numberx+1 and dir == 'Right':
                    if self.deathonwall:
                        self.dead(bodylength)
                    else:
                        x= 1
                if x == 0 and dir == 'Left':
                    if self.deathonwall:
                        self.dead(bodylength)
                    else:
                        x= self.grid1.numberx
                if y == self.grid1.numbery+1 and dir == 'Up':
                    if self.deathonwall:
                        self.dead(bodylength)
                    else:
                        y = 1
                if y == 0 and dir == 'Down':
                    if self.deathonwall:
                        self.dead(bodylength)
                    else:
                        y =self.grid1.numbery
                if snake_body[0] in snake_body[1:]:
                    if snake_body[1] in snake_body[1:]:
                        self.dead(bodylength)
                        return

            tick += 1

            time.sleep(self.tickspeed)
    def reload(self):
        for i in self.grid1.boxlist:
            i.deselect()
            i.configure(bg='light gray')

        self.main()
    def dead(self,bodylength):
        messagebox1 = tk.messagebox.askquestion('Game Over', f'You died with a length of {bodylength}\nWould you like to play again?')
        if messagebox1 == 'yes':
            self.reload()
        else:
            self.grid1.root.destroy()

class config:

    def __init__(self):
        from functools import partial


        with open('snake/config.json') as file:
            self.contents = json.loads(file.read())
        self.root = tk.Toplevel()
        self.varx = tk.IntVar()
        self.vary = tk.IntVar()
        self.varticks = tk.DoubleVar()
        self.varwall = tk.BooleanVar()
        tk.Label(self.root,text='x').grid(row = 0, column=0,sticky='w')
        tk.Label(self.root,text='y').grid(row = 1, column=0,sticky='w')
        tk.Label(self.root,text='tickspeed (s)').grid(row = 2, column=0,sticky='w')
        tk.Label(self.root,text='Death on wall').grid(row = 3, column=0,sticky='w')
        tk.Entry(self.root,width=5,textvariable=self.varx).grid(row = 0, column=1,sticky='w')
        tk.Entry(self.root,width=5,textvariable=self.vary).grid(row = 1, column=1,sticky='w')
        tk.Entry(self.root,width=5,textvariable=self.varticks).grid(row = 2, column=1,sticky='w')
        tk.Checkbutton(self.root, variable=self.varwall).grid(row = 3, column=1,sticky='w')
        self.varx.set(self.contents['x'])
        self.vary.set(self.contents['y'])
        self.varticks.set(self.contents['tickspeed'])
        self.varwall.set(self.contents['deathonwall'])
        tk.Button(self.root,text='randomize',command=partial(self.randomize, 'x'),padx=10).grid(row = 0, column=2,sticky='e')
        tk.Button(self.root,text='randomize',command=partial(self.randomize, 'y'),padx=10).grid(row = 1, column=2,sticky='e')
        tk.Button(self.root,text='randomize',command=partial(self.randomize, 'ticks'),padx=10).grid(row = 2, column=2,sticky='e')
        tk.Button(self.root,text='randomize all',command=partial(self.randomize, 'all')).grid(row = 4, column=0,sticky='e')
        tk.Button(self.root,text='done',command=self.done).grid(row = 4, column=2,sticky='e')
        self.root.wait_window()

    def randomize(self, button):
        import random
        if button == "x":
            self.varx.set(random.randint(1,100))
        if button == "y":
            self.vary.set(random.randint(1,100))
        if button == "ticks":
            self.varticks.set(random.randint(1,100)/1000)
        if button == "all":
            self.varx.set(random.randint(1,100))
            self.vary.set(random.randint(1,100))
            self.varticks.set(random.randint(1,100)/1000)
    def done(self):
        if not self.varx.get() or not self.vary.get() or not self.varticks.get():
            tk.messagebox.showwarning(message="Please make sure no value is 0")

        else:
            self.contents['x'] = self.varx.get()
            self.contents['y'] = self.vary.get()
            self.contents['tickspeed'] = self.varticks.get()
            self.contents['deathonwall'] = self.varwall.get()
            with open('snake/config.json', 'w') as file:
                file.write(json.dumps(self.contents))
            self.root.destroy()

if __name__ == "__main__":
    snake()
#    config()
