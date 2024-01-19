import customtkinter as ctk
import numpy as np
from leafpair import LeafPair

class MLCWizard(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("MLC Wizard")
        self.geometry("1300x1000")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.F = ctk.CTkFrame(self)
        self.F.pack(fill="both", expand=True)

        self.num_of_leafpairs = 80
        self.leafpairs = [LeafPair(self.F, i) for i in range(self.num_of_leafpairs)]
        [self.leafpairs[i].pack(fill="x", expand=True) for i in range(self.num_of_leafpairs)]

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    MLCWizard().mainloop()