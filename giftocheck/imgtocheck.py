from tkinter import filedialog
import tkinter as tk
from PIL import Image
import gridcreation as grid
import json
import numpy as np
#57, self.grid1.numbery - (8 - 1)
class imgtocheck:
    def init(self, image, maxx, maxy):
        self.x = image.size[0]
        self.y = image.size[1]  # gets images x and y values

        self.maxx, self.maxy = maxx, maxy  # maximum amount of checkboxes on x and y axis numbers which I found to be the best fit for a 1080p monitor

        self.downscale()

        self.resized = np.array(image.resize((self.newx, self.newy)))  # resizes image to the dimensions formed in downscale
        return self.hexify()


    def downscale(self, image=None, max = None):
        if image:
            self.x = image.size[0]
            self.y = image.size[1]

        self.newx, self.newy = self.x, self.y

        if max:
            self.maxx = max[0]
            self.maxy = max[1]
        while 1:    # loops and changes the y value by 1 and the x value by the relative x/y until it fits in the pre astablished 69x41 area
            if (int(self.newx) <= self.maxx and self.newy <= self.maxy):
                self.newx = int(self.newx)
                break
            self.newy -= 1
            self.newx -= self.x/self.y
        return self.newx, self.newx

    def hexify(self):
        new_image = []
        for y in self.resized:
            new_image.append([])
            for x in y:
                mycolor = '#%02x%02x%02x' % (x[0], x[1], x[2])
                new_image[-1].append(mycolor)
        return new_image

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
        self.root.mainloop()
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
