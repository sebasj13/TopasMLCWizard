import customtkinter as ctk

class CF(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, width=660, height=1000)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0, minsize=300)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1, minsize=300)
        self.columnconfigure(0, weight=1, minsize=330)
        self.columnconfigure(1, weight=1, minsize=330)   
        self.titleframe = ctk.CTkFrame(self, fg_color="#2B2B2B", border_color="white", border_width=2)
        self.title = ctk.CTkLabel(self.titleframe, text="TOPAS MLC Wizard", font=("Bahnschrift", 30, "bold"), fg_color="#2B2B2B")
        self.titleframe.grid_propagate(False)
        self.title.pack(fill="both", pady=(10,10), expand=True, padx=(5,5), side="left")
        self.titleframe.grid(row=0, column=0, columnspan=2, pady=(5,5), sticky="nsew", padx=(5,5))

        #SQUARE FIELD
        self.sq_field = ctk.CTkFrame(self, fg_color="#2B2B2B", border_color="white", border_width=2)
        self.sq_field.grid_propagate(False)
        self.sq_field.columnconfigure(0, weight=1)
        self.sq_field.rowconfigure(0, weight=1, minsize=56)
        self.sq_field.rowconfigure(1, weight=1)

        self.squareentry = ctk.CTkEntry(self.sq_field, width=100, font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.squarebutton = ctk.CTkButton(self.sq_field, text="Square Field", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.square)
        self.squareentry.grid(row=0, column=0, pady=(5,5), sticky="s")
        self.squarebutton.grid(row=1, column=0, pady=(5,5), sticky="n")
        self.sq_field.grid(row=1, column=0, pady=(5,5), sticky="nsew", padx=(5,5))

        #OFFAXIS FIELD
        self.rec_field = ctk.CTkFrame(self, fg_color="#2B2B2B", border_color="white", border_width=2)
        self.rec_field.grid_propagate(False)
        self.rec_field.rowconfigure(0)
        self.rec_field.rowconfigure(1)
        self.rec_field.rowconfigure(2)
        self.rec_field.rowconfigure(3)
        self.rec_field.rowconfigure(4)
        self.rec_field.rowconfigure(5)
        self.rec_field.columnconfigure(0, weight=1, minsize = 105)
        self.rec_field.columnconfigure(1, weight=1, minsize = 105)
        self.rec_field.columnconfigure(2, weight=1, minsize = 105)
        self.y2entry = ctk.CTkEntry(self.rec_field, width=100, font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.x1entry = ctk.CTkEntry(self.rec_field, width=100, font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.x2entry = ctk.CTkEntry(self.rec_field, width=100, font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.y1entry = ctk.CTkEntry(self.rec_field, width=100, font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.x1label = ctk.CTkLabel(self.rec_field, text="X1", font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.x2label = ctk.CTkLabel(self.rec_field, text="X2", font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.y1label = ctk.CTkLabel(self.rec_field, text="Y1", font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.y2label = ctk.CTkLabel(self.rec_field, text="Y2", font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.offaxisbutton = ctk.CTkButton(self.rec_field, text="Rectangular Field", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.offaxis, width=100)

        self.rec_field.grid(row=1, column=1, pady=(5,5), sticky="nsew", padx=(5,5))

        #grid in a 1 - 2 - 1 shape, with y2 on top, then x1 and x2, then y1 on bottom
        self.y2label.grid(row=0, column=1, pady=(5,5), sticky="nsew")
        self.y2entry.grid(row=1, column=1, pady=(5,5), sticky="nsew")
        self.x1label.grid(row=2, column=0, pady=(5,5), sticky="nsew", padx=(5,0))
        self.x1entry.grid(row=3, column=0, pady=(5,5), sticky="nsew", padx=(5,0))
        self.x2label.grid(row=2, column=2, pady=(5,5), sticky="nsew", padx=5)
        self.x2entry.grid(row=3, column=2, pady=(5,5), sticky="nsew", padx=5)
        self.y1label.grid(row=4, column=1, pady=(5,5), sticky="nsew")
        self.y1entry.grid(row=5, column=1, pady=(5,5), sticky="nsew")
        self.offaxisbutton.grid(row=6, column=0, columnspan=3, pady=(5,5), sticky="ns")

        #DRAW RECTANGLE
        self.drawrectbutton = ctk.CTkButton(self, text="Draw Rectangle", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.drawrect)
        self.drawrectbutton.grid(row=2, column=0, columnspan=2, pady=(5,5), sticky="nsew")

        #FIELD SEQUENCE BROWSER
        self.fieldseqframe = ctk.CTkFrame(self, fg_color="#2B2B2B", border_color="white", border_width=2)
        self.fieldseqframe.grid_propagate(False)
        self.fieldseqframe.rowconfigure(0, weight=0)
        self.fieldseqframe.rowconfigure(1, weight=1)
        self.fieldseqframe.columnconfigure(0, weight=1)
        self.fieldseqtitle = ctk.CTkLabel(self.fieldseqframe, text="Field Sequence", font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.fieldseqtitle.grid(row=0, column=0, pady=(5,5), sticky="nsew", padx=(5,5))
        self.fieldseqframe.grid(row=3, column=0, columnspan=2, pady=(5,5), sticky="nsew", padx=(5,5))




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
            self.parent.C.unbind("Motion>")
            self.parent.C.config(cursor="crosshair")

        def drawrect_motion(event):
            try:
                self.parent.C.coords(self.rect, self._drag_start_x, self._drag_start_y, event.x, event.y)
                x1, y1, x2, y2 = self._drag_start_x, self._drag_start_y, event.x, event.y
                if x1 > x2:
                    x1, x2 = x2, x1
                if y1 > y2:
                    y1, y2 = y2, y1
                x1, x2 = round(self.parent.C.leafpairs[0].xscale(x1-150)/10,2), round(self.parent.C.leafpairs[0].xscale(x2-150)/10,2)
                y1, y2 = round(self.parent.C.jawpair.yscale(y1)/10,2), round(self.parent.C.jawpair.yscale(y2)/10,2)

                self.parent.C.itemconfigure(self.tooltip, text=f"X1: {x1} cm, X2: {x2} cm, Y1: {y1} cm, Y2: {y2} cm")
            except ValueError: pass

        def on_enter(event):
            self.tooltip = self.parent.C.create_text(900,745, text="", fill="yellow", anchor="center", font=("Arial", 9))

        def mouse_motion(event):
            if self.parent.C.cget("cursor") != "crosshair":
                self.parent.C.config(cursor="crosshair")
            try:
                x1, y1 = event.x, event.y
                x1 = round(self.parent.C.leafpairs[0].xscale(x1-150)/10,2)
                y1 = round(self.parent.C.jawpair.yscale(y1)/10,2)
                self.parent.C.itemconfigure(self.tooltip, text=f"X1: {x1} cm, Y1: {y1} cm")
            except ValueError: pass

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
                        
            self.parent.C.unbind("<Enter>")#
            self.parent.C.unbind("<Motion>")
            self.parent.C.unbind("<Button-1>")
            self.parent.C.unbind("<B1-Motion>")
            self.parent.C.unbind("<ButtonRelease-1>")
            self.parent.C.delete(self.tooltip)
            self.parent.C.config(cursor="arrow")

        self.parent.C.bind("<Enter>", on_enter)
        self.parent.C.bind("<Button-1>", drawrect_start)
        self.parent.C.bind("<Motion>", mouse_motion)
        self.parent.C.bind("<B1-Motion>", drawrect_motion)
        self.parent.C.bind("<ButtonRelease-1>", drawrect_release)
        self.square(value=40)

    def offaxis(self):
        x1, y1, x2, y2 = float(self.x1entry.get())*10, float(self.y1entry.get())*10, float(self.x2entry.get())*10, float(self.y2entry.get())*10
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        for i in range(len(self.parent.C.leafpairs)):
            if self.parent.C.leafpairs[i].y > y2 + 2.5 or self.parent.C.leafpairs[i].y < y1 - 2.5:
                self.parent.C.leafpairs[i].set_left_leaf(0.0)
                self.parent.C.leafpairs[i].set_right_leaf(0.0)
            else:
                self.parent.C.leafpairs[i].set_left_leaf(x1)
                self.parent.C.leafpairs[i].set_right_leaf(x2)

        self.parent.C.jawpair.set_top_jaw(y2)
        self.parent.C.jawpair.set_bottom_jaw(y1)