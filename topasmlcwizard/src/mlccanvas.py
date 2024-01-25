from tkinter import Canvas, PhotoImage
import os
import sys

from .leafpair import LeafPair
from .jaws import JawPair


class MLCCanvas(Canvas):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, width=1260, height=1000, bg="#2B2B2B", borderwidth=0, highlightthickness=0 )

        self.scale = PhotoImage(file=self.resource_path(os.path.join("topasmlcwizard","img","scale.png")))
        self.create_image(0,0, image=self.scale, anchor="nw")
        
        self.jawpair = JawPair(self)

        self.num_of_leafpairs = 80
        self.leafpairs = [LeafPair(self, i) for i in range(self.num_of_leafpairs)]

    def resource_path(self, relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, "TopasMLCWizard", relative_path)
            else:
                 return os.path.join(os.path.abspath("."), relative_path)

