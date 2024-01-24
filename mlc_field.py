import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps
import numpy as np
from scipy.interpolate import interp1d

class MLCField():

    def __init__(self, parent, CF, leaf_positions, jaw_positions, index):
        self.parent = parent
        self.index = index
        self.select = False

        self.leaf_positions = leaf_positions
        self.jaw_positions = jaw_positions
        self.CF = CF

        self.image = self.create_bitmap(size=80)

        self.C = parent
        self.C.bind("<Enter>", lambda event: self.C.config(cursor="hand2"))
        self.C.bind("<Leave>", lambda event: self.C.config(cursor="arrow"))
        self.C.config(width=(max([index, len(self.CF.sequence)])+2)*100+20)
        self.image_id = self.C.create_image(index*110,5, image=self.image, anchor="nw")

    def scale(self, value, size):
        return int((interp1d([-200,200],[0,size])(value)))

    def create_bitmap(self, size=80, border=False):
        jawimage = np.zeros((size,size))
        mlcimage = np.zeros((size,size))
        bottomjawpixel = self.scale(self.jaw_positions[0], size)
        topjawpixel = self.scale(self.jaw_positions[1], size)
        for i in range(size):
            if i < topjawpixel or i > bottomjawpixel:
                for j in range(size):
                    jawimage[i][j] = 1

        for i in range(size):
            for j in range(0, self.scale(self.leaf_positions[i//(size//80)][0], size)):
                mlcimage[i][j] = 1
            for j in range(self.scale(self.leaf_positions[i//(size//80)][1], size), size):
                mlcimage[i][j] = 1

        jawimage = np.rot90(jawimage, k=2)
        image = np.add(mlcimage, jawimage)
        r = np.zeros((size,size))
        g = np.zeros((size,size))
        b = np.zeros((size,size))
        r = image.copy()
        g = image.copy()
        b = image.copy()
        r[image >= 1] = 102
        g[image >= 1] = 102 
        b[image >= 1] = 102
        r[image == 0] = 43
        g[image == 0] = 49
        b[image == 0] = 138
        rgbArray = np.zeros((size, size,3), 'uint8')
        rgbArray[..., 0] = r
        rgbArray[..., 1] = g
        rgbArray[..., 2] = b
        img = Image.fromarray(rgbArray)
        if border:
            img = ImageOps.expand(img, border=8, fill="black")
            img = ImageOps.expand(img, border=2, fill="white")
        else:
            img = ImageOps.expand(img, border=10, fill="black")
        return ImageTk.PhotoImage(img)
    
    def selected(self):
        if self.select: 
            self.unselected()
            self.select = False
            self.CF.selected_field = None
            return
        
        self.select = True
        try: self.CF.sequence[self.CF.selected_field].unselected()
        except: pass
        self.C.delete(self.image_id)
        self.image = self.create_bitmap(size=80, border=True)
        self.image_id = self.C.create_image(self.index*110,5, image=self.image, anchor="nw")

    def unselected(self):
        self.C.delete(self.image_id)
        self.image = self.create_bitmap(size=80, border=False)
        self.image_id = self.C.create_image(self.index*110,5, image=self.image, anchor="nw")