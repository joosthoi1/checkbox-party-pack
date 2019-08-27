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
                if x[3] == 0:
                    mycolor = "white"
                else:
                    mycolor = '#%02x%02x%02x' % (x[0], x[1], x[2])
                new_image[-1].append(mycolor)
        return new_image
