import customtkinter as ctk

from controlframe import CF
from mlccanvas import MLCCanvas


class MLCWizard(ctk.CTk):

    def __init__(self):
        super().__init__(fg_color="#2B2B2B")
        self.title("TOPAS MLC Wizard")
        self.pack_propagate(False)

        self.C = MLCCanvas(self)
        self.CF = CF(self)

        self.C.pack(fill="both", pady=(5,5), expand=True, side="left")
        self.CF.pack(fill="both", pady=(5,5), side="right")

        self.bind("<Configure>", self.stop_resize)

        self.after(1000, lambda: self.unbind("<Configure>"))
        self.mainloop()

    def stop_resize(self, event):
       if self.state() == "zoomed":
           pass
       else:
           self.state('zoomed')

if __name__ == "__main__":
    MLCWizard()