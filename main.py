import customtkinter as ctk
from leafpair import LeafPair
from controlframe import CF

class MLCWizard(ctk.CTk):

    def __init__(self):
        super().__init__(fg_color="#2B2B2B")
        self.title("TOPAS MLC Wizard")
        self.pack_propagate(False)

        self.F = ctk.CTkCanvas(self, width=1300, height=1000, bg="#2B2B2B", borderwidth=0, highlightthickness=0 )
        self.topjaw = self.F.create_rectangle(0,0,1300,200, fill="red")
        self.bottomjaw = self.F.create_rectangle(0,800,1300,1000, fill="red")
        self.CF = CF(self)

        self.F.pack(fill="both", pady=(5,5), expand=True, side="left")
        self.CF.pack(fill="both", pady=(5,5), side="right")
        self.num_of_leafpairs = 80
        self.leafpairs = [LeafPair(self.F, i) for i in range(self.num_of_leafpairs)]
        [self.leafpairs[i].pack(fill="x", expand=True) for i in range(self.num_of_leafpairs)]
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