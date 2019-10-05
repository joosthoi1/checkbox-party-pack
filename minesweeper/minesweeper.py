import gridcreation as gc
import tkinter as tk
from tkinter import messagebox
import random
import json
import time
from functools import partial

class minesweeper:
    def __init__(self):
        with open('minesweeper/config.json') as file:
            contents = json.loads(file.read())
        self.root = tk.Tk()
        self.flag_frame = tk.Frame(self.root)
        self.mine_frame = tk.Frame(self.root)
        self.flag_frame.pack()
        self.mine_frame.pack()
        self.bomb_number = contents['bombs']
        x = contents['x']
        y = contents['y']
        self.grid = gc.grid_reverse(x,y, root=self.mine_frame, text = '  ', do_title=False)
        tk.Label(self.flag_frame,text='⚐').pack(side='left')
        self.flag_num = tk.IntVar()
        self.flag_num.set(self.bomb_number)
        tk.Label(self.flag_frame,text='',textvariable = self.flag_num).pack(side='left')
        self.flags = set()
        self.colors = {
            0:"white smoke",
            1:"royalblue1",
            2:"green4",
            3:"red3",
            4:"dark orchid",
            5:"hot pink",
            6:"yellow",
            7:"MediumPurple4",
            8:"turquoise1"
        }
        #self.place_bombs()
        self.bomb_list = set()
        self.bind()
        #self.generate_numbers()
        self.root.mainloop()

    def reload(self):
        self.flag_num.set(self.bomb_number)
        self.flags = set()
        self.bomb_list = set()
        self.bind()
        for i in self.grid.boxlist:
            i.deselect()
            i.config(state='normal', text= '  ', bg= 'light gray', activebackground= 'light gray')
            self.root.update()


    def reveal_board(self):
        for c, i in enumerate(self.grid.boxlist):
            text = self.value_list[c]
            color = self.colors[text]
            i.select()
            i.config(bg='light gray', text = text, disabledforeground = color, state='disabled')
            if c in self.bomb_list:
                i.config(bg='black', disabledforeground = 'light gray')
            if c in self.flags:
                if c in self.bomb_list:
                    i.config(bg='dark red')
                else:
                    i.config(bg='dim gray', disabledforeground = 'light gray')

    def place_bombs(self, boxes, c):
        boxes.add(c)
        random_range = list(range(self.grid.numberx*self.grid.numbery))
        self.unopened = set(random_range)
        for i in boxes:
            random_range.remove(i)
        for i in range(self.bomb_number):
            rand_num = random.choice(random_range)
            self.bomb_list.add(rand_num)
            random_range.remove(rand_num)

    def generate_numbers(self):
        y = self.grid.numbery
        x = self.grid.numberx
        self.value_list = []
        for c, i in enumerate(self.grid.boxlist):
            box_value = 0
            ignore_top = (True if c - x < 0 else False)
            ignore_bottom = (True if c + x >= x*y else False)
            ignore_left = (True if c % x is 0 else False)
            ignore_right = (True if (c+1) % x is 0 else False)
            ignore_topright = ignore_top or ignore_right
            ignore_topleft = ignore_top or ignore_left
            ignore_bottomright = ignore_bottom or ignore_right
            ignore_bottomleft = ignore_bottom or ignore_left
            if not c in self.bomb_list:
                if not ignore_top:
                    if c - x in self.bomb_list:
                        box_value += 1
                if not ignore_left:
                    if c - 1 in self.bomb_list:
                        box_value += 1
                if not ignore_right:
                    if c + 1 in self.bomb_list:
                        box_value += 1
                if not ignore_bottom:
                    if c + x in self.bomb_list:
                        box_value += 1
                if not ignore_topright:
                    if (c+1) - x in self.bomb_list:
                        box_value += 1
                if not ignore_topleft:
                    if (c-1) - x in self.bomb_list:
                        box_value += 1
                if not ignore_bottomright:
                    if (c+1) + x in self.bomb_list:
                        box_value += 1
                if not ignore_bottomleft:
                    if (c-1) + x in self.bomb_list:
                        box_value += 1
            self.value_list.append(box_value)

    def right(self, box, event=None):
        checkbox = self.grid.boxlist[box]
        if not checkbox['state'] == 'disabled':
            checkbox.toggle()
            if box in self.flags:
                self.flags.remove(box)
                checkbox.config(bg = 'light gray')
                self.flag_num.set(self.flag_num.get() + 1)
            else:
                self.flags.add(box)
                checkbox.config(bg = 'red')
                self.flag_num.set(self.flag_num.get() - 1)

    def left(self, box, event=None):
        checkbox = self.grid.boxlist[box]
        if not self.bomb_list:
            self.open(box)
        if not checkbox['state'] == 'disabled':
            if not box in self.flags:
                if box in self.bomb_list:
                    self.dead()
                else:
                    self.unopened.remove(box)
                    text = self.value_list[box]
                    color = self.colors[text]
                    checkbox.config(text=text, state='disabled',disabledforeground=color)
                    checkbox.select()
                    if text == 0:
                        self.open(box)
                    if self.unopened == self.bomb_list:
                        self.win()
            else:
                checkbox.deselect()

    def dead(self):
        self.reveal_board()
        messagebox1 = messagebox.askquestion(
            'Game Over', f'You exploded into a million pieces :(\nWould you like to play again?'
        )
        if messagebox1 == 'yes':
            self.reload()
        else:
            self.root.destroy()

    def win(self):
        messagebox1 = messagebox.askquestion(
            'Game Over', f'You won!\nWould you like to play again?'
        )
        if messagebox1 == 'yes':
            self.reload()
        else:
            self.root.destroy()

    def open(self, c):
        y = self.grid.numbery
        x = self.grid.numberx
        ignore_top = (True if c - x < 0 else False)
        ignore_bottom = (True if c + x >= x*y else False)
        ignore_left = (True if c % x is 0 else False)
        ignore_right = (True if (c+1) % x is 0 else False)
        ignore_topright = ignore_top or ignore_right
        ignore_topleft = ignore_top or ignore_left
        ignore_bottomright = ignore_bottom or ignore_right
        ignore_bottomleft = ignore_bottom or ignore_left

        boxes = set()
        if not ignore_top:
            boxes.add(c - x)
        if not ignore_left:
            boxes.add(c - 1)
        if not ignore_right:
            boxes.add(c + 1)
        if not ignore_bottom:
            boxes.add(c + x)
        if not ignore_topright:
            boxes.add((c+1) - x)
        if not ignore_topleft:
            boxes.add((c-1) - x)
        if not ignore_bottomright:
            boxes.add((c+1) + x)
        if not ignore_bottomleft:
            boxes.add((c-1) + x)

        if not self.bomb_list:
            self.place_bombs(boxes, c)
            self.generate_numbers()

        for i in boxes:
            box = self.grid.boxlist[i]
            if not box['state'] == 'disabled':
                self.unopened.remove(i)
                text = self.value_list[i]
                color = self.colors[text]
                box.config(text=text, state='disabled',bg='light gray',disabledforeground=color)
                box.select()
                if text == 0:
                    self.open(i)
        if self.unopened == self.bomb_list:
            self.win()

    def bind(self):
        for c, i in enumerate(self.grid.boxlist):
            i.bind("<Button-1>", partial(self.left, c))
            i.bind("<Button-3>", partial(self.right, c))

class config:

    def __init__(self):
        with open('minesweeper/config.json') as file:
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
        self.root.wait_window()

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

        elif self.varx.get() * self.vary.get() - 8 <= self.varbombs.get():
            tk.messagebox.showwarning(message="Please make sure there's enough room for the bombs")
        else:
            self.contents['x'] = self.varx.get()
            self.contents['y'] = self.vary.get()
            self.contents['bombs'] = self.varbombs.get()
            with open('minesweeper/config.json', 'w') as file:
                file.write(json.dumps(self.contents))
            self.root.destroy()

if __name__ == "__main__":
    minesweeper()
#    config()
