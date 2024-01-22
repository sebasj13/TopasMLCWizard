import customtkinter as ctk

class CF(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, width=660, height=1000)
        self.pack_propagate(False)
        self.title = ctk.CTkLabel(self, text="TOPAS MLC Wizard", font=("Bahnschrift", 30, "bold"), fg_color="#2B2B2B")
        self.title.pack(pady=(5,5))

        #SQUARE FIELD
        self.squareentry = ctk.CTkEntry(self, width=100, font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.squarebutton = ctk.CTkButton(self, text="Square Field", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.square)
        self.squareentry.pack(pady=(5,5))
        self.squarebutton.pack(pady=(5,5))

        #DRAW RECTANGLE
        self.drawrectbutton = ctk.CTkButton(self, text="Draw Rectangle", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.drawrect)
        self.drawrectbutton.pack(pady=(5,5))

    def square(self, value=None):
        if value == None:
            field_size = 10*float(self.squareentry.get())
        else:
            field_size = 10*value
        if field_size > 400:
            field_size = 400
        if field_size < 0:
            field_size = 0

        x1, x2 = y1,y2 = -round(field_size/2,2), round(field_size/2,2)
        for i in range(len(self.parent.C.leafpairs)):
            if self.parent.C.leafpairs[i].y > y2 + 2.5 or self.parent.C.leafpairs[i].y < y1 - 2.5:
                self.parent.C.leafpairs[i].set_left_leaf(0.0)
                self.parent.C.leafpairs[i].set_right_leaf(0.0)
            else:
                self.parent.C.leafpairs[i].set_left_leaf(x1)
                self.parent.C.leafpairs[i].set_right_leaf(x2)

        self.parent.C.jawpair.set_top_jaw(y2)
        self.parent.C.jawpair.set_bottom_jaw(y1)

    def drawrect(self):

        def drawrect_start(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y
            self.rect = self.parent.C.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)

        def drawrect_motion(event):
            self.parent.C.coords(self.rect, self._drag_start_x, self._drag_start_y, event.x, event.y)
            x1, y1, x2, y2 = self._drag_start_x, self._drag_start_y, event.x, event.y
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            x1, x2 = round(self.parent.C.leafpairs[0].xscale(x1-150)/10,2), round(self.parent.C.leafpairs[0].xscale(x2-150)/10,2)
            y1, y2 = round(self.parent.C.jawpair.yscale(y1)/10,2), round(self.parent.C.jawpair.yscale(y2)/10,2)

            self.parent.C.itemconfigure(self.tooltip, text=f"X1: {x1} cm, X2: {x2} cm, Y1: {y1} cm, Y2: {y2} cm")

        def drawrect_release(event):
            self.parent.C.delete(self.rect)
            x1, y1, x2, y2 = self._drag_start_x, self._drag_start_y, event.x, event.y

            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            x1, x2 = self.parent.C.leafpairs[0].xscale(x1-150), self.parent.C.leafpairs[0].xscale(x2-150)
            y1, y2 = self.parent.C.jawpair.yscale(y1), self.parent.C.jawpair.yscale(y2)

            for i in range(len(self.parent.C.leafpairs)):
                if self.parent.C.leafpairs[i].y < y1 + 5 and self.parent.C.leafpairs[i].y > y2 - 5:
                    self.parent.C.leafpairs[i].set_left_leaf(x1)
                    self.parent.C.leafpairs[i].set_right_leaf(x2)
                else:
                    self.parent.C.leafpairs[i].set_left_leaf(0.0)
                    self.parent.C.leafpairs[i].set_right_leaf(0.0)

            self.parent.C.jawpair.set_top_jaw(y1)
            self.parent.C.jawpair.set_bottom_jaw(y2)
                        

            self.parent.C.unbind("<Button-1>")
            self.parent.C.unbind("<B1-Motion>")
            self.parent.C.unbind("<ButtonRelease-1>")
            self.parent.C.delete(self.tooltip)

        self.tooltip = self.parent.C.create_text(900,745, text="", fill="yellow", anchor="center", font=("Arial", 9))

        self.parent.C.bind("<Button-1>", drawrect_start)
        self.parent.C.bind("<B1-Motion>", drawrect_motion)
        self.parent.C.bind("<ButtonRelease-1>", drawrect_release)
        self.square(value=40)