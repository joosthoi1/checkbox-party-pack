import tkinter as tk
import tetris.tetris as tetris
import minesweeper.minesweeper as minesweeper
import imgtocheck.imgtocheck as imgtocheck
import snake.snake as snake
import displayboard.displayboard as DisplayBoard
import giftocheck.giftocheck as giftocheck
import rubiks_cube.cube as cube
from functools import partial
import pypresence
import threading
import json
import PIL.Image
import PIL.ImageTk
import time

class GameError(Exception):
    pass

class main:
    def __init__(self):
        with open("settings.json", 'r') as file:
            settings = json.loads(file.read())

        if settings['pypresence']:
            client_id = '605045493592227860'
            self.RPC = pypresence.Presence(client_id)
            self.RPC.connect()
            details = "In menu:"
            state = "Game launcher"
            self.RPC.update(details = details, state = state)

        self.main_loop()


    def main_loop(self):
        while True:
            self.root = tk.Tk()
            self.old_num = 0

            menubar = tk.Menu(self.root)

            self.presence_var = tk.BooleanVar()
            with open("settings.json", 'r') as file:
                settings = json.loads(file.read())
            self.presence_var.set(settings['pypresence'])
            self.presence = settings['pypresence']


            settingsmenu = tk.Menu(menubar, tearoff=0)
            settingsmenu.add_checkbutton(
                label="Discord rich presence",
                variable=self.presence_var,
                command = self.presence_menu
            )

            menubar.add_cascade(label="Settings", menu=settingsmenu)

            self.root.config(menu=menubar)

            self.add_scrollbar()

            self.framelist = []
            self.innerframelist = []
            self.imglist = []

            self.imagelabels = [
                ('Tetris', "tetris/Tetrislogo.png"),
                ('Minesweeper', "minesweeper/minewsweeperlogo.png"),
                ('Snake', "snake/snakelogo.png"),
                ('Imgtocheck', "tetris/Tetrislogo.png"),
                ('Display Board', "tetris/Tetrislogo.png"),
                ('Giftocheck', "tetris/Tetrislogo.png"),
                ("Rubik's Cube", "rubiks_cube/rubikslogo.png")
            ]

            self.setup_frames()
            self.on_resize(width = self.canvas.winfo_width())
            
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.canvas.bind("<Configure>", self.on_resize)
            self.root.mainloop()

    def on_resize(self, event=None, width=None):
        if event:
            canvas_width = event.width
            new_num = event.width // 319
            self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
        else:
            new_num = width // 319
        if new_num == 0:
                new_num = 1
        if new_num != self.old_num:  
            self.old_num = new_num
            self.position_frames(new_num)
            
            

    def position_frames(self, max_x):
        x, y = 0, 0
        for label in self.framelist:
            self.move_frame(label, y, x)
            x += 1
            if x == max_x:
                x = 0
                y += 1
            
            
    
    def on_close(self):
        exit(0)

    def presence_menu(self):
        with open("settings.json", 'r') as file:
            settings = json.loads(file.read())
        settings['pypresence'] = self.presence_var.get()
        self.presence = settings['pypresence']
        with open("settings.json", 'w+') as file:
            file.write(json.dumps(settings, indent = 4))
        if self.presence:
            if not hasattr(self, 'RPC'):
                client_id = '605045493592227860'
                self.RPC = pypresence.Presence(client_id)

            self.RPC.connect()

            details = "In menu:"
            state = "Game launcher"
            self.RPC.update(details = details, state = state)
        else:
            self.RPC.clear()

    def move_frame(self, frame, row, col):
        frame.grid(row=row, column=col)
    
    def setup_frames(self):
        for i in self.imagelabels:
            self.framelist.append(
                tk.Frame(self.frame)
            )
            im = PIL.Image.open(i[1])
            photo = PIL.ImageTk.PhotoImage(im)
            self.imglist.append(photo)
            cur_image = self.imglist[-1]
            cur_frame = self.framelist[-1]
            tk.Frame(cur_frame,width=10,).grid(row=0,column=0)
            tk.Frame(cur_frame,width=10,).grid(row=0,column=2)
            tk.Frame(cur_frame,height=10,).grid(row=0,column=0)
            tk.Frame(cur_frame,height=10,).grid(row=4,column=0)
            
            tk.Label(cur_frame, text = i[0], font = ("Helvetica", "16")).grid(row=1,column=1)
            
            tk.Label(cur_frame, image = cur_image).grid(row=2,column=1)

            innerframe = tk.Frame(cur_frame, width=200)
            innerframe.grid(row=3,column=1)
            tk.Button(
                innerframe,
                text='start',
                command = partial(self.load, i[0])
            ).pack(side='left')
            tk.Button(innerframe, text='⚙', command = partial(self.config, i[0])).pack(side='right')
        
    def add_scrollbar(self):
        self.canvas = tk.Canvas(self.root, borderwidth=0, width=1050,height=740)
        self.frame1 = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_frame = self.canvas.create_window(
            (4,4),
            window=self.frame1,
            anchor="n",
            tags="self.frame1",
        )
        self.frame = tk.Frame(self.frame1)
        self.frame.pack(side='top')
       

        self.frame.bind("<Configure>", self.onFrameConfigure)
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load(self, name):
        self.root.destroy()

        details = "In game:"
        state = name
        if self.presence:
            self.RPC.update(details = details, state = state)

        if name == 'Tetris':
            tetris.tetris()
        elif name == 'Minesweeper':
            minesweeper.minesweeper()
        elif name == 'Snake':
            snake.snake()
        elif name == 'Imgtocheck':
            imgtocheck.imgtocheck()
        elif name == 'Display Board':
            DisplayBoard.board()
        elif name == 'Giftocheck':
            giftocheck.giftocheck()
        elif name == "Rubik's Cube":
            cube.cube()
        else:
            raise GameError("Game was not found")

        details = "In menu:"
        state = "Game launcher"
        if self.presence:
            self.RPC.update(details = details, state = state)


    def config(self, name):
        details = "In menu:"
        state = f'{name} config'
        if self.presence:
            self.RPC.update(details = details, state = state)

        if name == 'Minesweeper':
            minesweeper.config()
        if name == 'Snake':
            snake.config()
        if name == 'Imgtocheck':
            imgtocheck.config()
        if name == 'Display Board':
            DisplayBoard.config()
        if name == 'Giftocheck':
            giftocheck.config()

        details = "In menu:"
        state = "Game launcher"
        if self.presence:
            self.RPC.update(details = details, state = state)





if __name__ == '__main__':
    main()
