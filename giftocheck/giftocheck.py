import giftocheck.imgtocheck as imgtocheck
from PIL import Image
import numpy as np
import gridcreation as gc
import tkinter as tk
import json


class giftocheck:
    def __init__(self):
        with open('giftocheck/config.json') as file:
            self.contents = json.loads(file.read())

        q = tk.Tk()
        q.withdraw()
        path =  tk.filedialog.askopenfilename(
                title = "Select file",filetypes = (
                ("gif files","*.gif"), ("all files","*.*")
            )
        )

        if not path:
            return

        self.image = Image.open(path)

        self.frames = []
        f = imgtocheck.imgtocheck()
        for i in range(self.image.n_frames):
            x = self.contents['x']
            y = self.contents['y']
            self.frames.append(f.init(self.image.convert('RGBA'), x, y))
            self.image.seek(i)


        self.grid = gc.grid_reverse(
            len(self.frames[0][0]),
            len(self.frames[0]),
            root = q
        )
        q.wm_deiconify()
        #for i in grid.boxlist:
        #    i.configure(state='disabled')
        self.animate_loop()


    def animate_loop(self):
        i = 0
        while True:
            try:
                for pos_y, y in enumerate(self.frames[i]):
                    for pos_x, x in enumerate(y):
                        box = self.grid.boxlist[
                            self.grid.coords(
                                pos_x+1, pos_y+1
                            )
                        ]
                        box.configure(bg=x, fg= x, disabledforeground=x)
                        if self.contents['selected']:
                            box.select()
                        if not self.contents['enabled']:
                            box.configure(state='disabled')
                        if not self.contents['color']:
                            box.configure(
                                fg = 'black',
                                disabledforeground='black'
                            )
                self.grid.root.update()
#                self.grid.root.update()
            except tk.TclError:
                break
            i += 1
            if i == self.image.n_frames:
                i = 0
class config:
    def __init__(self):
        from functools import partial

        with open('giftocheck/config.json') as file:
            self.contents = json.loads(file.read())

        self.root = tk.Toplevel()

        self.varx = tk.IntVar()
        self.vary = tk.IntVar()
        self.varstate = tk.BooleanVar()
        self.varselected = tk.BooleanVar()
        self.varcolor = tk.BooleanVar()

        tk.Label(self.root,text='x for 1080p 16/9, 69 is recommended').grid(row = 0, column=0,sticky='w')
        tk.Label(self.root,text='y for 1080p 16/9, 41 is recommended').grid(row = 1, column=0,sticky='w')
        tk.Label(self.root,text='Boxes are checkable').grid(row = 2, column=0,sticky='w')
        tk.Label(self.root,text='All boxes selected').grid(row = 3, column=0,sticky='w')
        tk.Label(self.root,text='Check color is black').grid(row = 4, column=0,sticky='w')

        tk.Entry(self.root,width=5,textvariable=self.varx).grid(row = 0, column=1,sticky='w')
        tk.Entry(self.root,width=5,textvariable=self.vary).grid(row = 1, column=1,sticky='w')
        tk.Checkbutton(self.root, variable=self.varstate).grid(row = 2, column=1,sticky='w')
        tk.Checkbutton(self.root, variable=self.varselected).grid(row = 3, column=1,sticky='w')
        tk.Checkbutton(self.root, variable=self.varcolor).grid(row = 4, column=1,sticky='w')

        self.varx.set(self.contents['x'])
        self.vary.set(self.contents['y'])
        self.varstate.set(self.contents['enabled'])
        self.varselected.set(self.contents['selected'])
        self.varcolor.set(self.contents['color'])

        tk.Button(self.root,text='randomize',command=partial(self.randomize, 'x'),padx=10).grid(row = 0, column=2,sticky='e')
        tk.Button(self.root,text='randomize',command=partial(self.randomize, 'y'),padx=10).grid(row = 1, column=2,sticky='e')
        tk.Button(self.root,text='randomize all',command=partial(self.randomize, 'all')).grid(row = 5, column=0,sticky='w')

        tk.Button(self.root,text='done',command=self.done).grid(row = 5, column=2,sticky='e')
        self.root.wait_window()

    def randomize(self, button):
        import random
        if button == "x":
            self.varx.set(random.randint(1,100))
        if button == "y":
            self.vary.set(random.randint(1,100))
        if button == "all":
            self.varx.set(random.randint(1,100))
            self.vary.set(random.randint(1,100))
    def done(self):
        if not self.varx.get() or not self.vary.get():
            tk.messagebox.showwarning(message="Please make sure no value is 0")

        else:
            self.contents['x'] = self.varx.get()
            self.contents['y'] = self.vary.get()
            self.contents['enabled'] = self.varstate.get()
            self.contents['selected'] = self.varselected.get()
            self.contents['color'] = self.varcolor.get()
            with open('giftocheck/config.json', 'w') as file:
                file.write(json.dumps(self.contents))
            self.root.destroy()

if __name__ == "__main__":
    giftocheck()
