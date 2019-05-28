from tkinter import filedialog
import tkinter as tk
import cv2
import gridcreation as grid
import json

class imgtocheck:
    def __init__(self):

        with open('imgtocheck\\config.json') as file:
            self.contents = json.loads(file.read())

        tk.Tk().withdraw()
        self.filename =  filedialog.askopenfilename(
            initialdir = "/",title = "Select file",filetypes = (
                ("png files","*.png"), ("jpeg files", ("*.jpg","*.jpeg")),
                ("gif files","*.gif"), ("all files","*.*")
            )
        )
        path = self.filename  # path to image
        if not path:
            return

        if path.split('.')[1] == 'png':  # checks if its a png since png's need special treatment
            image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        else:
            image = cv2.imread(path)

        self.y = image.shape[0]  # gets images x and y values
        self.x = image.shape[1]
        self.maxx, self.maxy = self.contents['x'], self.contents['y']  # maximum amount of checkboxes on x and y axis numbers which I found to be the best fit for a 1080p monitor

        self.downscale()

        self.resized = cv2.resize(image, (self.newx, self.newy))  # resizes image to the dimensions formed in downscale
        cv2.imshow("preview", self.resized)  # shows preview of image

        self.grid1 = grid.grid(self.newx - 1, self.newy - 1)  # creates a checkboxgrid, read gridcreation.py for info
        self.grid1.root.title('art')
        self.colorin()
        self.grid1.root.mainloop()
    def downscale(self):
        self.newx, self.newy = self.x, self.y
        while 1:    # loops and changes the y value by 1 and the x value by the relative x/y until it fits in the pre astablished 69x41 area
            if (int(self.newx) <= self.maxx and self.newy <= self.maxy):
                self.newx = int(self.newx)
                break
            self.newy -= 1
            self.newx -= self.x/self.y

    def colorin(self):              # grabs the color of each pixel and modifies the checkboxes to be that color
        x, y = 1, 1
        for i in self.grid1.boxlist:
            mycolor = '#%02x%02x%02x' % (self.resized[y-1][x-1][2], self.resized[y-1][x-1][1], self.resized[y-1][x-1][0])  # converts rgb to hex
            if list(self.resized[y-1][x-1]) == [0, 0, 0, 0]:
                mycolor = 'white'
            self.grid1.boxlist[self.grid1.coords(x, self.grid1.numbery - (y - 1))].configure(bg=mycolor, fg=mycolor,disabledforeground=mycolor)
            if not self.contents['enabled']:
                self.grid1.boxlist[self.grid1.coords(x, self.grid1.numbery - (y - 1))].configure(state='disabled')  # disables checkboxes to get more color, remove/comment this line to make them checkable
            if self.contents['selected']:
                self.grid1.boxlist[self.grid1.coords(x, self.grid1.numbery - (y - 1))].select()
            if self.contents['color']:
                self.grid1.boxlist[self.grid1.coords(x, self.grid1.numbery - (y - 1))].configure(bg=mycolor, fg='black',disabledforeground='black')

#            self.grid1.boxlist[self.grid1.coords(x, self.grid1.numbery-(y-1))].select() #selects checkboxes to get more color, remove/comment this line to make them checkable
            x += 1
            if x == self.newx:
                y += 1
                x = 1
            if y == self.newy:
                break

class config:
    def __init__(self):
        from functools import partial

        with open('imgtocheck\\config.json') as file:
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

        tk.Button(self.root,text='done',command=self.done).grid(row = 4, column=2,sticky='e')
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
            with open('imgtocheck\\config.json', 'w') as file:
                file.write(json.dumps(self.contents))
            self.root.destroy()
if __name__ == '__main__':
    imgtocheck()
    #config()
