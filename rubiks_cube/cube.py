import tkinter as tk
import gridcreation as gc
import rubiks_cube.lists as lists
from functools import partial

class cube:
    def __init__(self):
        self.root = tk.Tk()

        self.cube_frame = tk.Frame(self.root)
        self.grid = gc.grid_reverse(12,9, root=self.cube_frame, do_title=False)
        self.cube_frame.grid(row=0,column=0)

        self.button_frame = tk.Frame(self.root)

        self.button_frame.grid(row=1,column=0,sticky='w')

        self.cube_buttons_frame = tk.Frame(self.root)
        self.cube2_frame = tk.Frame(self.cube_buttons_frame)
        self.grid2 = gc.grid_reverse(9,9, root=self.cube2_frame, do_title=False)

        self.cube_buttons_frame.grid(row=2,column=0)
        self.cube2_frame.grid(row=1, column=1)
        self.selected = 'F'

        self.create_buttons()

        self.lists = lists.list()
        self.list_to_checks()

        self.root.mainloop()

    def create_buttons(self):
        tk.Button(
            self.button_frame,
            text= "F",
            command = partial(self.button, "F"),
            width=6
        ).grid(row=0,column=0)
        tk.Button(
            self.button_frame,
            text= "F'",
            command = partial(self.button, "F'"),
            width=6
        ).grid(row=1,column=0)
        tk.Button(
            self.button_frame,
            text= "R",
            command = partial(self.button, "R"),
            width=6
        ).grid(row=0,column=1)
        tk.Button(
            self.button_frame,
            text= "R'",
            command = partial(self.button, "R'"),
            width=6
        ).grid(row=1,column=1)
        tk.Button(
            self.button_frame,
            text= "U",
            command = partial(self.button, "U"),
            width=6
        ).grid(row=0,column=2)
        tk.Button(
            self.button_frame,
            text= "U'",
            command = partial(self.button, "U'"),
            width=6
        ).grid(row=1,column=2)
        tk.Button(
            self.button_frame,
            text= "B",
            command = partial(self.button, "B"),
            width=6
        ).grid(row=0,column=3)
        tk.Button(
            self.button_frame,
            text= "B'",
            command = partial(self.button, "B'"),
            width=6
        ).grid(row=1,column=3)
        tk.Button(
            self.button_frame,
            text= "L",
            command = partial(self.button, "L"),
            width=6
        ).grid(row=0,column=4)
        tk.Button(
            self.button_frame,
            text= "L'",
            command = partial(self.button, "L'"),
            width=6
        ).grid(row=1,column=4)
        tk.Button(
            self.button_frame,
            text= "D",
            command = partial(self.button, "D"),
            width=6
        ).grid(row=0,column=5)
        tk.Button(
            self.button_frame,
            text= "D'",
            command = partial(self.button, "D'"),
            width=6
        ).grid(row=1,column=5)

        self.side_layout = {
            "F":[['U',[6,7,8]],['R',[0,3,6]],['D',[2,1,0]],['L',[8,5,2]]],
            "R":[['U',[8,5,2]],['B',[0,3,6]],['D',[8,5,2]],['F',[8,5,2]]],
            "U":[['B',[2,1,0]],['R',[2,1,0]],['F',[2,1,0]],['L',[2,1,0]]],
            "B":[['R',[8,5,2]],['U',[2,1,0]],['L',[0,3,6]],['D',[6,7,8]]],
            "L":[['U',[0,3,6]],['F',[0,3,6]],['D',[0,3,6]],['B',[8,5,2]]],
            "D":[['L',[6,7,8]],['F',[6,7,8]],['R',[6,7,8]],['B',[6,7,8]]],
        }

        tk.Button(
            self.cube_buttons_frame,
            text = '→',
            command = partial(self.change_size, "right"),
            height=13
        ).grid(row=1,column=2)
        tk.Button(
        self.cube_buttons_frame,
        text = '←',
        command = partial(self.change_size, "left"),
        height=13
        ).grid(row=1,column=0)
        tk.Button(
            self.cube_buttons_frame,
            text = '↓',
            command = partial(self.change_size, "down"),
            width=32
        ).grid(row=2,column=1)
        tk.Button(
            self.cube_buttons_frame,
            text = '↑',
            command = partial(self.change_size, "up"),
            width=32
        ).grid(row=0,column=1)

    def change_size(self, direction):

        if self.selected == 'F':
            side_dict = {
                "right":"R",
                "left":"L",
                "up":"U",
                "down":"D"
            }
            self.selected = side_dict[direction]

        elif self.selected == 'R':
            side_dict = {
                "right":"B",
                "left":"F",
                "up":"U",
                "down":"D"
            }
            self.selected = side_dict[direction]

        elif self.selected == 'B':
            side_dict = {
                "right":"L",
                "left":"R",
                "up":"U",
                "down":"D"
            }
            self.selected = side_dict[direction]

        elif self.selected == 'L':
            side_dict = {
                "right":"F",
                "left":"B",
                "up":"U",
                "down":"D"
            }
            self.selected = side_dict[direction]

        elif self.selected == 'U':
            side_dict = {
                "right":"R",
                "left":"L",
                "up":"B",
                "down":"F"
            }
            self.selected = side_dict[direction]

        elif self.selected == 'D':
            side_dict = {
                "right":"L",
                "left":"R",
                "up":"F",
                "down":"B"
            }
            self.selected = side_dict[direction]

        self.list_to_checks()

    def sides(self, layout, reverse):
#        layout = [('U',[6,7,8]),('R',[0,3,6]),('D',[2,1,0]),('L',[2,5,8])
        if reverse:
            for i in layout:
                i[1] = i[1][::-1]
            layout = layout[::-1]
        for i in range(3):
            colors = []
            for i in layout:
                for x in i[1]:
                    colors.append(self.lists.sides[i[0]][x])

            colors.insert(0, colors.pop(-1))

            for c, i in enumerate(layout):
                for c2, x in enumerate(i[1]):
                    self.lists.sides[i[0]][x] = colors[c2 + c*3]

        self.list_to_checks()

    def button(self, button):
        if button[-1] == "'":
            button = button[0]
            reverse = True
        else:
            reverse = False

        current = self.lists.sides[button]
        copy_current = current.copy()

        if not reverse:
            layout = [[0,1,2],[2,5,8],[8,7,6],[6,3,0]]
        else:
            layout = [[0,3,6],[6,7,8],[8,5,2],[2,1,0]]

        new_layout = layout.copy()
        new_layout.insert(0, new_layout.pop(-1))

        for i in zip(layout, new_layout):
            for x in zip(i[0], i[1]):
                current[x[0]] = copy_current[x[1]]


        self.sides(self.side_layout[button], reverse)
        self.list_to_checks()

    def list_to_checks(self):
        for side in self.lists.side_names:
            if side == "F":
                y = 4
                x = 4
            elif side == "R":
                y = 4
                x = 7
            elif side == "U":
                x = 4
                y = 1
            elif side == "B":
                x = 10
                y = 4
            elif side == "L":
                x = 1
                y = 4
            elif side == "D":
                x = 4
                y = 7
            count_x = 0
            count_y = 0
            for i in self.lists.sides[side]:
                self.grid.boxlist[
                    self.grid.coords(x + count_x, y + count_y)
                ].configure(
                    bg = i,
                    fg = i
                )
                count_x += 1
                if count_x == 3:
                    count_y += 1
                    count_x = 0

            count_x = 0
            count_y = 0

            for color in self.lists.sides[self.selected]:
                x = 0
                y = 0
                for i in range(9):
                    self.grid2.boxlist[
                        self.grid2.coords((x+ 1) + count_x*3, (y+1) + count_y*3)
                    ].configure(
                        bg = color,
                        fg = color
                    )
                    x += 1
                    if x == 3:
                        y += 1
                        x = 0

                count_x += 1
                if count_x == 3:
                    count_y += 1
                    count_x = 0





if __name__ == "__main__":
    cube()
