import gridcreation as gc
import tkinter as tk
from tkinter import messagebox
import time
import json
import random
import displayboard.ascii as ascii
#import ascii


#'a!"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
#test sentence ^^

class board:
    def __init__(self):
        with open('displayboard/config.json') as file:
            self.contents = json.loads(file.read())
        x = self.contents['length']
        self.grid = gc.grid_reverse(x,8)
        self.root = self.grid.root


        self.string = self.contents['text']
        self.color = self.contents['color']
        self.use_random = self.contents['random_color']
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
                if self.use_random:
                    r = random.randint(0, 255)
                    b = random.randint(0, 255)
                    g = random.randint(0, 255)
                    hex = '#%02x%02x%02x' % (r, g, b)
                    box.configure(bg=hex)

                else:
                    box.configure(bg=self.color)

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
                        (uncoords[0]-1, uncoords[1], self.grid.boxlist[c]['bg'])
                    )
        for i in to_clear:
            box = self.grid.boxlist[i]
            box.deselect()
            box.configure(bg='light grey')
        for i in moved:
            box = self.grid.boxlist[self.grid.coords(i)]
            box.select()
            box.configure(bg=i[-1])

class config:
    def __init__(self):
        from functools import partial

        path = 'displayboard/config.json'
        with open(path) as file:
            self.contents = json.loads(file.read())
        print(self.contents)
        self.root = tk.Toplevel()
        self.radiovar = tk.IntVar()
        self.redvar = tk.StringVar()
        self.greenvar = tk.StringVar()
        self.bluevar = tk.StringVar()
        self.lengthvar = tk.StringVar()

        tk.Label(self.root,text='Text: ').grid(row = 0, column=0,sticky='nw')
        self.textbox = tk.Text(self.root,height=3,width=30)
        self.textbox.grid(row=0,column=1,sticky='w')

        self.textbox.insert(tk.END, self.contents['text'])

        tk.Label(self.root, text='length: ').grid(row=1,column=0,sticky='w')
        tk.Entry(
            self.root,
            textvariable = self.lengthvar,
            width=3
        ).grid(row=1,column=1,sticky='w')
        self.lengthvar.set(self.contents['length'])

        tk.Radiobutton(
            self.root, text = 'Color: ',variable = self.radiovar,value=1,
            command=self.rainbow_off
        ).grid(row=2,column=0,sticky='w')



        self.rgb_frame = tk.Frame(self.root)
        self.rgb_frame.grid(row=2,column=1,sticky='w')
        tk.Label(self.rgb_frame,text='R:').pack(side="left")
        tk.Entry(self.rgb_frame,width=3,textvariable=self.redvar).pack(side="left")
        tk.Label(self.rgb_frame,text='G:').pack(side="left")
        tk.Entry(self.rgb_frame,width=3,textvariable=self.greenvar).pack(side="left")
        tk.Label(self.rgb_frame,text='B:').pack(side="left")
        tk.Entry(self.rgb_frame,width=3,textvariable=self.bluevar).pack(side="left")
        color_button = tk.Checkbutton(self.rgb_frame)
        color_button.pack(side='left')
        hex = self.contents['color'][1:]
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        self.redvar.set(rgb[0])
        self.greenvar.set(rgb[1])
        self.bluevar.set(rgb[2])

        tk.Radiobutton(
            self.root, text = 'Rainbow',variable = self.radiovar,value=2,
            command=self.rainbow_on
        ).grid(row=3,column=0,sticky='w')

        if self.contents['random_color']:
            self.radiovar.set(2)
            self.rainbow_on()
        else:
            self.radiovar.set(1)

        tk.Button(
            self.root,
            command=self.done,
            text='done'
        ).grid(row=4,column=1,sticky='e')


        while True:
            try:
                self.root.update()
                rgb = (
                    self.redvar.get(),
                    self.greenvar.get(),
                    self.bluevar.get()
                )
                if all(i.isdigit() for i in rgb):
                    rgb = tuple(map(int, rgb))
                    if all(0 <= i <= 255 for i in rgb):
                        self.hex = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
                        color_button.configure(bg=self.hex)
            except tk.TclError:
                break


    def rainbow_on(self):
        for i in self.rgb_frame.winfo_children():
            i.configure(state='disabled')

    def rainbow_off(self):
        for i in self.rgb_frame.winfo_children():
            i.configure(state='normal')

    def done(self):
        contents = {}
        contents['text'] = self.textbox.get('1.0', 'end-1c')
        if self.lengthvar.get().isdigit():
            contents['length'] = int(self.lengthvar.get())
        else:
            tk.messagebox.showwarning(message="Please make sure length is a number")
            return
        if self.radiovar.get() == 1:
            rgb = (
                self.redvar.get(),
                self.greenvar.get(),
                self.bluevar.get()
            )
            if not all(i.isdigit() for i in rgb):
                tk.messagebox.showwarning(message="Please make sure the rgb values follow rgb rules")
                return
            rgb = tuple(map(int, rgb))
            if not all(0 <= i <= 255 for i in rgb):
                tk.messagebox.showwarning(message="Please make sure the rgb values follow rgb rules")
                return
            contents['color'] = self.hex
            contents['random_color'] = False
        else:
            contents['color'] = self.hex
            contents['random_color'] = True
        path = 'displayboard/config.json'
        with open(path, 'w') as file:
            file.write(json.dumps(contents, indent = 4))

        self.root.destroy()



if __name__ == "__main__":
    board()
#    config()
