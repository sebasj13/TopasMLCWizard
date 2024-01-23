from scipy.interpolate import interp1d
import ctypes

class LeafPair():
    def __init__(self, parent, number):
        self.C = parent
        self.number = str(number)
        if len(self.number) == 1:
            self.number = "0"+self.number

        self.w = 150
        self.h = 10

        self.pixelx = [0,1110]
        self.pixely = 20 + number*12 +2

        self.y = interp1d([0,79], [200,-195])(number) - 2.5

        self.left_selected = False
        self.right_selected = False

        self.leftleaf = self.C.create_rectangle(-1000+self.pixelx[0]+1,self.pixely,self.w+1,self.pixely+self.h, fill="grey40")
        self.C.tag_bind(self.leftleaf, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.leftleaf, "<Control-Button-1>", self.select_left_leaf)
        self.C.tag_bind(self.leftleaf, "<Enter>", self.hand_enter)
        self.C.tag_bind(self.leftleaf, "<Leave>", self.hand_leave)
        self.C.tag_bind(self.leftleaf, "<B1-Motion>", self.drag_motion)
        self.C.tag_bind(self.leftleaf, "<ButtonRelease-1>", self.drag_end)

        self.rightleaf = self.C.create_rectangle(self.pixelx[1]+1,self.pixely,self.pixelx[1]+self.w+1+1000,self.pixely+self.h,  fill="grey40")
        self.C.tag_bind(self.rightleaf, "<Enter>", self.hand_enter)
        self.C.tag_bind(self.rightleaf, "<Control-Button-1>", self.select_right_leaf)
        self.C.tag_bind(self.rightleaf, "<Leave>", self.hand_leave)
        self.C.tag_bind(self.rightleaf, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.rightleaf, "<B1-Motion>", self.drag_motion)
        self.C.tag_bind(self.rightleaf, "<ButtonRelease-1>", self.drag_end)

        self.leftleaftext = self.C.create_text(self.pixelx[0]+self.w//2,self.pixely + self.h//2, text=f"LL{self.number}: {self.xscale(0)}", fill="black", anchor="w", font=("Arial",9))
        self.C.tag_bind(self.leftleaftext, "<Enter>", self.hand_enter)
        self.C.tag_bind(self.leftleaftext, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.leftleaftext, "<B1-Motion>", self.drag_motion)
        self.C.tag_bind(self.leftleaftext, "<ButtonRelease-1>", self.drag_end)

        self.rightleaftext = self.C.create_text(self.pixelx[1]+self.w//2,self.pixely + self.h//2, text=f"RL{self.number}: {self.xscale(960)}", fill="black", anchor="e", font=("Arial",9))
        self.C.tag_bind(self.rightleaftext, "<Enter>", self.hand_enter)
        self.C.tag_bind(self.rightleaftext, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.rightleaftext, "<B1-Motion>", self.drag_motion)
        self.C.tag_bind(self.rightleaftext, "<ButtonRelease-1>", self.drag_end)

        self.set_left_leaf(-200.0)
        self.set_right_leaf(200.0)

    def hand_enter(self, event):
        self.C.config(cursor="hand2")

    def hand_leave(self, event):
        self.C.config(cursor="arrow")


    def GetTextDimensions(self, text):
        class SIZE(ctypes.Structure):
            _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

        hdc = ctypes.windll.user32.GetDC(0)
        hfont = ctypes.windll.gdi32.CreateFontA(9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Arial")
        hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

        size = SIZE(0, 0)
        ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

        ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
        ctypes.windll.gdi32.DeleteObject(hfont)

        return (size.cx, size.cy)

    def xscale(self, value):
        return round(float(interp1d([0,960],[-200,200])(value)),1)
    
    def inverse_xscale(self, value):
        return int(interp1d([-200,200],[0,960])(value))
    
    def set_left_leaf(self, x):
        self.C.moveto(self.leftleaf,x=-1000+self.inverse_xscale(x))
        self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {x}", anchor="w")
        self.C.moveto(self.leftleaftext,x=self.inverse_xscale(x)+74+(50-self.GetTextDimensions(f"LL{self.number}: {x}")[0]))
        self.pixelx[0] = self.inverse_xscale(x)

        x = self.inverse_xscale(x)
        if x+150 > self.pixelx[1]:
            rightleafpos = x + 150
            if rightleafpos > self.C.winfo_width()-self.w:
                rightleafpos = self.C.winfo_width()-self.w
                x = self.C.winfo_width()-2*self.w
            self.C.moveto(self.rightleaf,x=rightleafpos)
            self.C.itemconfigure(self.rightleaftext, text=f"RL{self.number}: {self.xscale(rightleafpos-150)}", anchor="e")
            self.C.moveto(self.rightleaftext,x=rightleafpos+16)
            self.pixelx[1] = rightleafpos


    def set_right_leaf(self, x):
        self.C.moveto(self.rightleaf,x=self.inverse_xscale(x)+150)
        self.C.itemconfigure(self.rightleaftext, text=f"RL{self.number}: {x}", anchor="e")
        self.C.moveto(self.rightleaftext,x=self.inverse_xscale(x)+150+16)
        self.pixelx[1] = self.inverse_xscale(x)+self.w

        x = self.inverse_xscale(x)+150
        if x <= self.pixelx[0]+150:
            leftleafpos = x-150
            if leftleafpos < 0:
                leftleafpos = 0
                x=150
            self.C.moveto(self.leftleaf,x=-1000+leftleafpos)
            self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {self.xscale(leftleafpos)}", anchor="w")
            self.C.moveto(self.leftleaftext,x=leftleafpos+74+(50-self.GetTextDimensions(f"LL{self.number}: {self.xscale(x)}")[0]))
            self.pixelx[0] = leftleafpos


    def drag_start(self, event):
        self._drag_start_x = event.x
        self.name = {1:"rightleaf", 0:"leftleaf"}[self.C.find_closest(event.x, event.y)[0]%2]

    def drag_motion(self, event, other = False):
        if self.name == "leftleaf":
            self.C.tag_unbind(self.leftleaf, "<Leave>")
            cur_x = self.pixelx[0]
        else:
            self.C.tag_unbind(self.rightleaf, "<Leave>")
            cur_x = self.pixelx[1]

        x = cur_x + event.x - self._drag_start_x

        if x < 0:
            x = 0
        elif x > self.C.winfo_width() - self.w:
            x = self.C.winfo_width() - self.w

        if self.name == "leftleaf":
            
            if x+150 > self.pixelx[1]:
                rightleafpos = x + 150
                if rightleafpos > self.C.winfo_width()-self.w:
                    rightleafpos = self.C.winfo_width()-self.w
                    x = self.C.winfo_width()-2*self.w
                self.C.moveto(self.rightleaf,x=rightleafpos)
                self.C.itemconfigure(self.rightleaftext, text=f"RL{self.number}: {self.xscale(rightleafpos-150)}", anchor="e")
                self.C.moveto(self.rightleaftext,x=rightleafpos+16)

                self.pixelx[1] = rightleafpos

            self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {self.xscale(x)}", anchor="w")
            self.C.moveto(self.leftleaf,x=-1000+x)
            self.C.moveto(self.leftleaftext,x=x+74+(50-self.GetTextDimensions(f"LL{self.number}: {self.xscale(x)}")[0]))
            self.pixelx[0] = x

            if self.left_selected and other == False:
                for i in range(len(self.C.leafpairs)):
                    if self.C.leafpairs[i].number != self.number and self.C.leafpairs[i].left_selected:
                        self.C.leafpairs[i].name = "leftleaf"
                        self.C.leafpairs[i]._drag_start_x = self._drag_start_x
                        self.C.leafpairs[i].drag_motion(event, other=True)

        else:
            if x <= self.pixelx[0]+150:
                leftleafpos = x-150
                if leftleafpos < 0:
                    leftleafpos = 0
                    x=150
                self.C.moveto(self.leftleaf,x=-1000+leftleafpos)
                self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {self.xscale(leftleafpos)}", anchor="w")
                self.C.moveto(self.leftleaftext,x=leftleafpos+74+(50-self.GetTextDimensions(f"LL{self.number}: {self.xscale(x)}")[0]))
                self.pixelx[0] = leftleafpos

            self.C.itemconfigure(self.rightleaftext, text=f"RL{self.number}: {self.xscale(x-150)}", anchor="e")
            self.C.moveto(self.rightleaf,x=x)
            self.C.moveto(self.rightleaftext,x=x+16)
            self.pixelx[1] = x

            if self.right_selected and other == False:
                for i in range(len(self.C.leafpairs)):
                    if self.C.leafpairs[i].number != self.number and self.C.leafpairs[i].right_selected:
                        self.C.leafpairs[i].name = "rightleaf"
                        self.C.leafpairs[i]._drag_start_x = self._drag_start_x
                        self.C.leafpairs[i].drag_motion(event, other=True)

        self._drag_start_x = event.x

    def drag_end(self, event):
        self.C.tag_bind(self.leftleaf, "<Leave>", self.hand_leave)
        self.C.tag_bind(self.rightleaf, "<Leave>", self.hand_leave)
        if self.left_selected:
            if self.name == "leftleaf":
                self.left_selected = False
                self.C.itemconfigure(self.leftleaf, fill="grey40")
                self.C.itemconfigure(self.leftleaftext, fill="black")
                for i in range(len(self.C.leafpairs)):
                    if self.C.leafpairs[i].number != self.number and self.C.leafpairs[i].left_selected:
                        self.C.leafpairs[i].name = "leftleaf"
                        self.C.leafpairs[i].drag_end(event)
        elif self.right_selected:
            if self.name == "rightleaf":
                self.right_selected = False
                self.C.itemconfigure(self.rightleaf, fill="grey40")
                self.C.itemconfigure(self.rightleaftext, fill="black")
                for i in range(len(self.C.leafpairs)):
                    if self.C.leafpairs[i].number != self.number and self.C.leafpairs[i].right_selected:
                        self.C.leafpairs[i].name = "rightleaf"
                        self.C.leafpairs[i].drag_end(event)

    def select_left_leaf(self, event):
        if self.left_selected:
            self.C.itemconfigure(self.leftleaf, fill="grey40")
            self.C.itemconfigure(self.leftleaftext, fill="black")
            self.left_selected = False
        else:
            self.C.itemconfigure(self.leftleaf, fill="green")
            self.C.itemconfigure(self.leftleaftext, fill="white")
            self.left_selected = True

    def select_right_leaf(self, event):
        if self.right_selected:
            self.C.itemconfigure(self.rightleaf, fill="grey40")
            self.C.itemconfigure(self.rightleaftext, fill="black")
            self.right_selected = False
        else:
            self.C.itemconfigure(self.rightleaf, fill="green")
            self.C.itemconfigure(self.rightleaftext, fill="white")
            self.right_selected = True