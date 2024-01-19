import customtkinter as ctk

class LeafPair(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        self.CL = ctk.CTkCanvas(self, width=150, height=20, highlightthickness=0, borderwidth=0, name="leftleaf")
        self.CL.config(cursor="hand2")
        self.CL.pack(side="left")
        self.CR = ctk.CTkCanvas(self, width=150, height=20, highlightthickness=0, borderwidth=0, name="rightleaf")
        self.CR.config(cursor="hand2")  
        self.CR.pack(side="right")

        self.leftleaf = self.CL.create_rectangle(0,0,149,19, fill="blue")
        self.leftleaftext = self.CL.create_text(75,10, text="LL: 150", fill="black")
        self.CL.tag_bind(self.leftleaf, "<Button-1>", self.drag_start)
        self.CL.tag_bind(self.leftleaf, "<B1-Motion>", self.drag_motion)
        self.CL.tag_bind(self.leftleaftext, "<Button-1>", self.drag_start)
        self.CL.tag_bind(self.leftleaftext, "<B1-Motion>", self.drag_motion)
        self.rightleaf = self.CR.create_rectangle(0,0,149,19,  fill="red")
        self.rightleaftext = self.CR.create_text(75,10, text="RL: 650", fill="black")
        self.CR.tag_bind(self.rightleaf, "<Button-1>", self.drag_start)
        self.CR.tag_bind(self.rightleaf, "<B1-Motion>", self.drag_motion)
        self.CR.tag_bind(self.rightleaftext, "<Button-1>", self.drag_start)
        self.CR.tag_bind(self.rightleaftext, "<B1-Motion>", self.drag_motion)

    def drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x

    def drag_motion(self, event):
        widget = event.widget
        name = str(widget).split(".")[-1]
        x = widget.winfo_x() - widget._drag_start_x + event.x

        if x < 0:
            x = 0
        elif x > self.parent.winfo_width()-widget.winfo_width():
            x = self.parent.winfo_width() - widget.winfo_width()

        if name == "leftleaf":

            if x+150 > (a:=self.nametowidget("rightleaf").winfo_x()):
                rightleafpos = a+(x-widget.winfo_x())
                if rightleafpos > self.parent.winfo_width()-widget.winfo_width():
                    rightleafpos = self.parent.winfo_width()-widget.winfo_width()
                    x = self.parent.winfo_width()-2*widget.winfo_width()
                self.nametowidget("rightleaf").place(x=rightleafpos)
                self.CR.itemconfigure(self.rightleaftext, text=f"RL: {rightleafpos}")
            self.CL.itemconfigure(self.leftleaftext, text=f"LL: {x+150}")

        else:

            if x < (a:=self.nametowidget("leftleaf").winfo_x())+150:
                leftleafpos = a-(widget.winfo_x()-x)
                if leftleafpos < 0:
                    leftleafpos = 0
                    x = widget.winfo_width()
                self.nametowidget("leftleaf").place(x=leftleafpos)
                self.CL.itemconfigure(self.leftleaftext, text=f"LL: {leftleafpos+150}")
            self.CR.itemconfigure(self.rightleaftext, text=f"RL: {x}")

        widget.place(x=x, y=widget.winfo_y())