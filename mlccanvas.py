from tkinter import Canvas, PhotoImage
from PIL import Image
from leafpair import LeafPair
from jaws import JawPair

class MLCCanvas(Canvas):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, width=1260, height=1000, bg="#2B2B2B", borderwidth=0, highlightthickness=0 )

        self.scale = PhotoImage(file="scale.png")
        self.create_image(0,0, image=self.scale, anchor="nw")
        
        self.jawpair = JawPair(self)

        self.num_of_leafpairs = 80
        self.leafpairs = [LeafPair(self, i) for i in range(self.num_of_leafpairs)]

