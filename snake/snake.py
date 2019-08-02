import gridcreation as gc
from tkinter import messagebox
import random
import json
import tkinter as tk

class snake:
    def __init__(self):
        with open('snake/config.json') as file:
            settings = json.loads(file.read())

        self.death_on_wall = settings['deathonwall']
        self.tick_speed = int(settings['tickspeed'])
        self.grid = gc.grid_reverse(settings['x'], settings['y'])
        self.root = self.grid.root


        self.root.focus_force()
        self.setup()

        self.root.bind("<Right>", self.right)
        self.root.bind("d", self.right)
        self.root.bind("<Left>", self.left)
        self.root.bind("a", self.left)
        self.root.bind("<Up>", self.up)
        self.root.bind("w", self.up)
        self.root.bind("<Down>", self.down)
        self.root.bind("s", self.down)

        self.loop()
        self.root.mainloop()

    def setup(self):
        self.x = 0
        self.y = self.grid.numbery//2
        self.dir = "Right"
        self.length = 3
        self.body = []
        self.need_fruit = True

    def loop(self):
        self.previous_dir = self.dir

        if self.need_fruit:
            while self.need_fruit:
                randcoordsx = random.randint(1, self.grid.numberx)
                randcoordsy = random.randint(1, self.grid.numbery)
                if not self.grid.coords(randcoordsx,randcoordsy) in self.body:
                    self.fruit_place = self.grid.coords(randcoordsx,randcoordsy)
                    box = self.grid.boxlist[
                        self.grid.coords(randcoordsx,randcoordsy)
                    ]
                    box.select()
                    box.configure(bg='red', fg='red')

                    self.need_fruit = False

        if self.dir == 'Right':
            self.x+=1
            if self.x == self.grid.numberx+1:
                if self.death_on_wall:
                    self.dead(self.length)
                    return
                else:
                    self.x = 1
        if self.dir == 'Left':
            self.x-=1
            if self.x == 0:
                if self.death_on_wall:
                    self.dead(self.length)
                    return
                else:
                    self.x = self.grid.numberx
        if self.dir == 'Up':
            self.y-=1
            if self.y == 0:
                if self.death_on_wall:
                    self.dead(self.length)
                    return
                else:
                    self.y = self.grid.numbery
        if self.dir == 'Down':
            self.y+=1
            if self.y == self.grid.numbery+1:
                if self.death_on_wall:
                    self.dead(self.length)
                    return
                else:
                    self.y = 1


        self.grid.boxlist[self.grid.coords(self.x, self.y)].select()
        self.grid.boxlist[self.grid.coords(self.x, self.y)].configure(foreground='green',bg='light gray')

        if len(self.body) >= self.length:
            self.body.insert(0, self.grid.coords(self.x, self.y))
            if not self.body[0] == self.body[-1]:
                body = self.grid.boxlist[self.body[-1]]
                body.deselect()
                body.configure(foreground='black')
            self.body.pop(-1)
        else:
            self.body.insert(0, self.grid.coords(self.x, self.y))

        if len(self.body) >= 1:
            if self.body[0] in self.body[1:]:
                self.dead(self.length)
                return

        if self.body[0] == self.fruit_place:
            self.length += 1
            self.need_fruit = True

        self.root.after(100, self.loop)

    def right(self, event=None):
        if not self.previous_dir == "Left":
            self.dir = "Right"
    def left(self, event=None):
        if not self.previous_dir == "Right":
            self.dir = "Left"
    def up(self, event=None):
        if not self.previous_dir == "Down":
            self.dir = "Up"
    def down(self, event=None):
        if not self.previous_dir == "Up":
            self.dir = "Down"

    def dead(self, length):
        messagebox1 = messagebox.askquestion('Game Over', f'You died with a length of {length}\nWould you like to play again?')
        if messagebox1 == 'yes':
            self.reload()
        else:
            self.grid.root.destroy()

    def reload(self):
        for i in self.grid.boxlist:
            i.deselect()
            i.configure(bg='light gray')

        self.setup()
        self.loop()

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
        tk.Label(self.root,text='tickspeed (ms)').grid(row = 2, column=0,sticky='w')
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
            messagebox.showwarning(message="Please make sure no value is 0")

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
