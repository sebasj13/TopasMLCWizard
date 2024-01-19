import customtkinter as ctk
from leafpair import LeafPair

class MLCWizard(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("MLC Wizard")
        self.geometry("800x600")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.F = ctk.CTkFrame(self)
        self.F.pack(fill="both", expand=True)

        self.leafpair_0 = LeafPair(self.F)
        self.leafpair_0.pack(fill="x", expand=True)

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    MLCWizard().mainloop()