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

        self.y = interp1d([0,79], [-200,195])(number) + 2.5

        self.leftleaf = self.C.create_rectangle(self.pixelx[0]+1,self.pixely,self.w+1,self.pixely+self.h, fill="grey80")
        self.C.tag_bind(self.leftleaf, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.leftleaf, "<B1-Motion>", self.drag_motion)

        self.rightleaf = self.C.create_rectangle(self.pixelx[1]+1,self.pixely,self.pixelx[1]+self.w+1,self.pixely+self.h,  fill="grey80")
        self.C.tag_bind(self.rightleaf, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.rightleaf, "<B1-Motion>", self.drag_motion)


        self.leftleaftext = self.C.create_text(self.pixelx[0]+self.w//2,self.pixely + self.h//2, text=f"LL{self.number}: {self.xscale(0)}", fill="black", anchor="w", font=("Arial",9))
        self.C.tag_bind(self.leftleaftext, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.leftleaftext, "<B1-Motion>", self.drag_motion)

        self.rightleaftext = self.C.create_text(self.pixelx[1]+self.w//2,self.pixely + self.h//2, text=f"RL{self.number}: {self.xscale(960)}", fill="black", anchor="e", font=("Arial",9))
        self.C.tag_bind(self.rightleaftext, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.rightleaftext, "<B1-Motion>", self.drag_motion)


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
    
    def set_left_leaf(self, value):
        self.C.moveto(self.leftleaf,x=self.inverse_xscale(value))
        self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {value}", anchor="w")
        self.C.moveto(self.leftleaftext,x=self.inverse_xscale(value)+74+(50-self.GetTextDimensions(f"LL{self.number}: {value}")[0]))
        self.pixelx[0] = self.inverse_xscale(value)
        print(self.pixelx)

    def set_right_leaf(self, value):
        self.C.moveto(self.rightleaf,x=self.inverse_xscale(value)+150)
        self.C.itemconfigure(self.rightleaftext, text=f"RL{self.number}: {value}", anchor="e")
        self.C.moveto(self.rightleaftext,x=self.inverse_xscale(value)+150+16)
        self.pixelx[1] = self.inverse_xscale(value)+self.w

    def drag_start(self, event):
        self._drag_start_x = event.x
        self.name = {1:"rightleaf", 0:"leftleaf"}[self.C.find_closest(event.x, event.y)[0]%2]

    def drag_motion(self, event):

        if self.name == "leftleaf":
            cur_x = self.pixelx[0]
        else:
            cur_x = self.pixelx[1]

        x = cur_x + event.x - self._drag_start_x
        self._drag_start_x = event.x

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
            self.C.moveto(self.leftleaf,x=x)
            self.C.moveto(self.leftleaftext,x=x+74+(50-self.GetTextDimensions(f"LL{self.number}: {self.xscale(x)}")[0]))
            self.pixelx[0] = x

        else:
            if x <= self.pixelx[0]+150:
                leftleafpos = x-150
                if leftleafpos < 0:
                    leftleafpos = 0
                    x=150
                self.C.moveto(self.leftleaf,x=leftleafpos)
                self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {self.xscale(leftleafpos)}", anchor="w")
                self.C.moveto(self.leftleaftext,x=leftleafpos+74+(50-self.GetTextDimensions(f"LL{self.number}: {self.xscale(x)}")[0]))
                self.pixelx[0] = leftleafpos

            self.C.itemconfigure(self.rightleaftext, text=f"RL{self.number}: {self.xscale(x-150)}", anchor="e")
            self.C.moveto(self.rightleaf,x=x)
            self.C.moveto(self.rightleaftext,x=x+16)
            self.pixelx[1] = x
