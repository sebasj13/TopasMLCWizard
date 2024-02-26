import customtkinter as ctk
import os
import sys

from .src.controlframe import CF
from .src.mlccanvas import MLCCanvas

#TODO: Add a feature to import the field sequence from a TOPAS Sequence file
#TODO: Add a feature to export the field sequence

class MLCWizard(ctk.CTk):

    def __init__(self):
        super().__init__(fg_color="#2B2B2B")
        self.title("ESMOCA FieldForge")
        self.geometry("1920x1080")
        self.pack_propagate(False)

        self.C = MLCCanvas(self)
        self.CF = CF(self)

        self.C.pack(fill="both", pady=(5,5), expand=True, side="left")
        self.CF.pack(fill="both", pady=(5,5), side="right")

        self.bind("<Configure>", self.stop_resize)

        self.after(1000, lambda: self.unbind("<Configure>"))

        self.iconpath = self.resource_path(os.path.join("img", "logo.ico"))
        self.iconbitmap(self.iconpath)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.mainloop()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, "TopasMLCWizard", "topasmlcwizard", relative_path)
        
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

    def stop_resize(self, event):
       if self.state() == "zoomed":
           pass
       else:
           self.state('zoomed')

if __name__ == "__main__":
    MLCWizard()