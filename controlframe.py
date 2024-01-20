import customtkinter as ctk

class CF(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, width=620, height=1000)
        self.pack_propagate(False)
        self.title = ctk.CTkLabel(self, text="TOPAS MLC Wizard", font=("Bahnschrift", 30, "bold"), fg_color="#2B2B2B")
        self.title.pack(pady=(5,5))

        self.entry = ctk.CTkEntry(self, width=100, font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.button = ctk.CTkButton(self, text="Square Field", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.square)
        self.entry.pack(pady=(5,5))
        self.button.pack(pady=(5,5))


    def square(self):
        field_size = 10*float(self.entry.get())
        if field_size > 400:
            field_size = 400
        if field_size < 0:
            field_size = 0

        x1, x2 = y1,y2 = -round(field_size/2,2), round(field_size/2,2)
        for i in range(len(self.parent.leafpairs)):
            if self.parent.leafpairs[i].y > y2 or self.parent.leafpairs[i].y < y1:
                self.parent.leafpairs[i].set_left_leaf(0)
                self.parent.leafpairs[i].set_right_leaf(0)
            else:
                self.parent.leafpairs[i].set_left_leaf(x1)
                self.parent.leafpairs[i].set_right_leaf(x2)
