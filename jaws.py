from scipy.interpolate import interp1d

class JawPair:
    def __init__(self, parent):
        self.C = parent

        self.pixely = [0, 980]

        self.w = 1260
        self.h = 1000

        self.topjaw = self.C.create_rectangle(0,-980,1260,20, fill="grey40")
        self.bottomjaw = self.C.create_rectangle(0,980,1260,1980, fill="grey40")
        self.topjawtext = self.C.create_text(630,10, text=f"Top Jaw: {self.yscale(20)}", fill="black", anchor="center", font=("Arial", 9))
        self.bottomjawtext = self.C.create_text(630,990, text=f"Bottom Jaw: {self.yscale(980)}", fill="black", anchor="center", font=("Arial", 9))
        self.C.moveto(self.topjawtext,y=6)
        self.C.moveto(self.bottomjawtext,y=980+0)

        self.C.tag_bind(self.topjaw, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.topjaw, "<B1-Motion>", self.drag_motion)
        self.C.tag_bind(self.topjawtext, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.topjawtext, "<B1-Motion>", self.drag_motion)
        self.C.tag_bind(self.bottomjaw, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.bottomjaw, "<B1-Motion>", self.drag_motion)
        self.C.tag_bind(self.bottomjawtext, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.bottomjawtext, "<B1-Motion>", self.drag_motion)

    def yscale(self, value):
        return round(float(interp1d([980,20],[-200,200])(value)),1)
    
    def inverse_yscale(self, value):
        return int(interp1d([-200,200],[980,20])(value))
    
    def set_top_jaw(self, value):
        self.C.moveto(self.topjaw,y=self.inverse_yscale(value)-self.h)
        self.C.moveto(self.topjawtext,y=self.inverse_yscale(value)-14)
        self.C.itemconfigure(self.topjawtext, text=f"Top Jaw: {value}", anchor="center")
        self.pixely[0] = self.inverse_yscale(value)

    def set_bottom_jaw(self, value):
        self.C.moveto(self.bottomjaw,y=self.inverse_yscale(value))
        self.C.moveto(self.bottomjawtext,y=self.inverse_yscale(value)+0)
        self.C.itemconfigure(self.bottomjawtext, text=f"Bottom Jaw: {value}", anchor="center")
        self.pixely[1] = self.inverse_yscale(value)

    def drag_start(self, event):
        self._drag_start_y = event.y
        self.name = {1:"topjaw", 0:"bottomjaw"}[self.C.find_closest(event.x, event.y)[0]%2]

    def drag_motion(self, event):

        if self.name == "topjaw":
            cur_y = self.pixely[0]
        else:
            cur_y = self.pixely[1]

        y = cur_y + event.y - self._drag_start_y
        self._drag_start_y = event.y

        if y < 20:
            y = 20

        if y > 980:
            y = 980

        if self.name == "topjaw":

            if y >= self.pixely[1]:    
                self.C.itemconfigure(self.bottomjawtext, text=f"Bottom Jaw: {self.yscale(y)}", anchor="center")
                self.C.moveto(self.bottomjaw,y=y)
                self.C.moveto(self.bottomjawtext,y=y+0)
                self.pixely[1] = y

            self.C.itemconfigure(self.topjawtext, text=f"Top Jaw: {self.yscale(y)}", anchor="center")
            self.C.moveto(self.topjaw,y=y-self.h)
            self.C.moveto(self.topjawtext,y=y-14)
            self.pixely[0] = y

        else:
            if y <= self.pixely[0]:
                
                self.C.itemconfigure(self.topjawtext, text=f"Top Jaw: {self.yscale(y)}", anchor="center")
                self.C.moveto(self.topjaw,y=y-self.h)
                self.C.moveto(self.topjawtext,y=y-14)
                self.pixely[0] = y
                    
            self.C.itemconfigure(self.bottomjawtext, text=f"Bottom Jaw: {self.yscale(y)}", anchor="center")
            self.C.moveto(self.bottomjaw,y=y)
            self.C.moveto(self.bottomjawtext,y=y+0)
            self.pixely[1] = y
