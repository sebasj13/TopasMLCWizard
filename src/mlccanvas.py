from tkinter import Canvas, PhotoImage
from src.leafpair import LeafPair
from src.jaws import JawPair

class MLCCanvas(Canvas):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, width=1260, height=1000, bg="#2B2B2B", borderwidth=0, highlightthickness=0 )

        self.scale = PhotoImage(file="img/scale.png")
        self.create_image(0,0, image=self.scale, anchor="nw")
        
        self.jawpair = JawPair(self)

        self.num_of_leafpairs = 80
        self.leafpairs = [LeafPair(self, i) for i in range(self.num_of_leafpairs)]

