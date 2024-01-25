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

        self.name = []

        self.y = interp1d([0,79], [200,-195])(number) - 2.5

        self.dragging = False
        self.left_selected = False
        self.right_selected = False

        self.leftleaf = self.C.create_rectangle(-960+self.pixelx[0]+1,self.pixely,self.w+1,self.pixely+self.h, fill="grey40")
        self.C.tag_bind(self.leftleaf, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.leftleaf, "<Control-Button-1>", self.select_left_leaf)
        self.C.tag_bind(self.leftleaf, "<Enter>", self.hand_enter)
        self.C.tag_bind(self.leftleaf, "<Leave>", self.hand_leave)
        self.C.tag_bind(self.leftleaf, "<B1-Motion>", self.drag_motion)

        self.rightleaf = self.C.create_rectangle(self.pixelx[1]+1,self.pixely,self.pixelx[1]+self.w+1+1000,self.pixely+self.h,  fill="grey40")
        self.C.tag_bind(self.rightleaf, "<Enter>", self.hand_enter)
        self.C.tag_bind(self.rightleaf, "<Control-Button-1>", self.select_right_leaf)
        self.C.tag_bind(self.rightleaf, "<Leave>", self.hand_leave)
        self.C.tag_bind(self.rightleaf, "<Button-1>", self.drag_start)
        self.C.tag_bind(self.rightleaf, "<B1-Motion>", self.drag_motion)

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


    def get_leaf_positions(self):
        return [float(self.C.itemcget(self.leftleaftext, "text").split(":")[1].strip()), float(self.C.itemcget(self.rightleaftext, "text").split(":")[1].strip())]

    def hand_enter(self, event):
        self.C.config(cursor="hand2")

    def hand_leave(self, event):
        self.C.config(cursor="arrow")

    def get_text_dimensions(self, text):
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
        if value < 0:
            value = 0
        if value > 960:
            value = 960
        return round(float(interp1d([0,960],[-200,200])(value)),1)
    
    def inverse_xscale(self, value):
        return int(interp1d([-200,200],[0,960])(value))
    
    def set_left_leaf(self, x, checks=True):
        self.C.moveto(self.leftleaf,x=-960+self.inverse_xscale(x))
        self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {x}", anchor="w")
        self.C.moveto(self.leftleaftext,x=self.inverse_xscale(x)+74+(50-self.get_text_dimensions(f"LL{self.number}: {x}")[0]))
        self.pixelx[0] = self.inverse_xscale(x)

        if checks:
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

    def set_right_leaf(self, x, checks=True):
        self.C.moveto(self.rightleaf,x=self.inverse_xscale(x)+150)
        self.C.itemconfigure(self.rightleaftext, text=f"RL{self.number}: {x}", anchor="e")
        self.C.moveto(self.rightleaftext,x=self.inverse_xscale(x)+150+16)
        self.pixelx[1] = self.inverse_xscale(x)+self.w

        if checks:
            x = self.inverse_xscale(x)+150
            if x <= self.pixelx[0]+150:
                leftleafpos = x-150
                if leftleafpos < 0:
                    leftleafpos = 0
                    x=150
                self.C.moveto(self.leftleaf,x=-960+leftleafpos)
                self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {self.xscale(leftleafpos)}", anchor="w")
                self.C.moveto(self.leftleaftext,x=leftleafpos+74+(50-self.get_text_dimensions(f"LL{self.number}: {self.xscale(x)}")[0]))
                self.pixelx[0] = leftleafpos

    def drag_start(self, event):
        self._drag_start_x = event.x
        self.name.append({1:"rightleaf", 0:"leftleaf"}[self.C.find_closest(event.x, event.y)[0]%2])
        self.name = list(set(self.name))

    def drag_motion(self, event, other = False):
        self.C.tag_bind(self.leftleaf, "<ButtonRelease-1>", self.drag_end)
        self.C.tag_bind(self.rightleaf, "<ButtonRelease-1>", self.drag_end)
        if "leftleaf" in self.name and "rightleaf" in self.name:
            x1 = min([960,max([0,self.pixelx[0] + event.x - self._drag_start_x])])
            x2 = min([self.pixelx[1] + event.x - self._drag_start_x,1110])

        elif "leftleaf" in self.name:
            self.C.tag_unbind(self.leftleaf, "<Leave>")
            cur_x = self.pixelx[0]
            x = cur_x + event.x - self._drag_start_x
            if x < 0: x = 0
            elif x > self.C.winfo_width() - self.w: x = self.C.winfo_width() - self.w

        elif "rightleaf" in self.name:
            self.C.tag_unbind(self.rightleaf, "<Leave>")
            cur_x = self.pixelx[1]
            x = cur_x + event.x - self._drag_start_x
            if x < 0: x = 0
            elif x > self.C.winfo_width() - self.w: x = self.C.winfo_width() - self.w

        if "leftleaf" in self.name and "rightleaf" in self.name:
            self.set_left_leaf(self.xscale(x1))
            self.set_right_leaf(self.xscale(x2-150))

            for i in range(len(self.C.leafpairs)):
                if self.C.leafpairs[i].number != self.number:
                    self.C.leafpairs[i].name = list(set(self.C.leafpairs[i].name))
                    self.C.leafpairs[i]._drag_start_x = self._drag_start_x
                    if self.C.leafpairs[i].right_selected:
                        self.C.leafpairs[i].name.append("rightleaf")
                        self.C.leafpairs[i].set_right_leaf(self.C.leafpairs[i].xscale(x2-150))
                    if self.C.leafpairs[i].left_selected:
                        self.C.leafpairs[i].name.append("leftleaf")
                        self.C.leafpairs[i].set_left_leaf(self.C.leafpairs[i].xscale(x1))

        elif "leftleaf" in self.name:
            
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
            self.C.moveto(self.leftleaf,x=-960+x)
            self.C.moveto(self.leftleaftext,x=x+74+(50-self.get_text_dimensions(f"LL{self.number}: {self.xscale(x)}")[0]))
            self.pixelx[0] = x

            if self.left_selected and other == False:
                for i in range(len(self.C.leafpairs)):
                    if self.C.leafpairs[i].number != self.number and self.C.leafpairs[i].left_selected:
                        self.C.leafpairs[i].name.append("leftleaf")
                        self.C.leafpairs[i].name = list(set(self.C.leafpairs[i].name))
                        self.C.leafpairs[i]._drag_start_x = self._drag_start_x
                        self.C.leafpairs[i].drag_motion(event, other=True)
                        self.C.leafpairs[i].other = True

        elif "rightleaf" in self.name:
            if x <= self.pixelx[0]+150:
                leftleafpos = x-150
                if leftleafpos < 0:
                    leftleafpos = 0
                    x=150
                self.C.moveto(self.leftleaf,x=-960+leftleafpos)
                self.C.itemconfigure(self.leftleaftext, text=f"LL{self.number}: {self.xscale(leftleafpos)}", anchor="w")
                self.C.moveto(self.leftleaftext,x=leftleafpos+74+(50-self.get_text_dimensions(f"LL{self.number}: {self.xscale(x)}")[0]))
                self.pixelx[0] = leftleafpos

            self.C.itemconfigure(self.rightleaftext, text=f"RL{self.number}: {self.xscale(x-150)}", anchor="e")
            self.C.moveto(self.rightleaf,x=x)
            self.C.moveto(self.rightleaftext,x=x+16)
            self.pixelx[1] = x

            if self.right_selected and other == False:
                for i in range(len(self.C.leafpairs)):
                    if self.C.leafpairs[i].number != self.number and self.C.leafpairs[i].right_selected:
                        self.C.leafpairs[i].name.append("rightleaf")
                        self.C.leafpairs[i].name = list(set(self.C.leafpairs[i].name))
                        self.C.leafpairs[i]._drag_start_x = self._drag_start_x
                        self.C.leafpairs[i].drag_motion(event, other=True)

        self._drag_start_x = event.x

    def drag_end(self, event):

        for i in range(len(self.C.leafpairs)):

            self.C.leafpairs[i].left_selected = False
            self.C.itemconfigure(self.C.leafpairs[i].leftleaf, fill="grey40")
            self.C.itemconfigure(self.C.leafpairs[i].leftleaftext, fill="black")
            self.C.leafpairs[i].right_selected = False
            self.C.itemconfigure(self.C.leafpairs[i].rightleaf, fill="grey40")
            self.C.itemconfigure(self.C.leafpairs[i].rightleaftext, fill="black")
            self.C.tag_bind(self.C.leafpairs[i].leftleaf, "<Leave>",  self.C.leafpairs[i].hand_leave)
            self.C.tag_bind(self.C.leafpairs[i].rightleaf, "<Leave>", self.C.leafpairs[i].hand_leave)
            self.C.tag_unbind(self.C.leafpairs[i].leftleaf, "<ButtonRelease-1>")
            self.C.tag_unbind(self.C.leafpairs[i].rightleaf, "<ButtonRelease-1>")
            self.C.leafpairs[i].name = []

    def select_left_leaf(self, event, other=False):
        if other:
            self.name.append("leftleaf")
            self.name = list(set(self.name))
            self.C.itemconfigure(self.leftleaf, fill="green")
            self.C.itemconfigure(self.leftleaftext, fill="white")
            self.left_selected = True
            self.dragging = False
            return

        if self.left_selected == True:
            self.C.itemconfigure(self.leftleaf, fill="grey40")
            self.C.itemconfigure(self.leftleaftext, fill="black")
            self.left_selected = False
            self.name.pop(self.name.index("leftleaf"))

        else:
            self.name.append("leftleaf")
            self.name = list(set(self.name))
            self.C.itemconfigure(self.leftleaf, fill="green")
            self.C.itemconfigure(self.leftleaftext, fill="white")
            self.left_selected = True
            self.dragging = False

        if not other:
            self.dragging = True
            self._select_drag_start_x = event.x
            self._select_drag_start_y = event.y
            self.C.tag_bind(self.leftleaf, "<B1-Motion>", self.select_multiple_leaf)
            self.C.tag_bind(self.leftleaf, "<ButtonRelease-1>", self.stop_select_multiple_leaf)

    def select_multiple_leaf(self, event):
        leaves_to_move = self.C.find_overlapping(self._select_drag_start_x, self._select_drag_start_y, event.x, event.y)
        left_leaf_ids = [[i,self.C.leafpairs[i].leftleaf] for i in range(len(self.C.leafpairs))]
        right_leaf_ids = [[i,self.C.leafpairs[i].rightleaf] for i in range(len(self.C.leafpairs))]
        left_leaves = []
        right_leaves = []
        for i in range(len(left_leaf_ids)):
            if left_leaf_ids[i][1] in leaves_to_move and left_leaf_ids[i][1] != self.leftleaf:
                left_leaves += [i]
        for i in range(len(right_leaf_ids)):
            if right_leaf_ids[i][1] in leaves_to_move and right_leaf_ids[i][1] != self.rightleaf:
                right_leaves += [i]

        for i in left_leaves:
            self.C.leafpairs[i].select_left_leaf(event, other=True)
        for i in right_leaves:
            self.C.leafpairs[i].select_right_leaf(event, other=True)

        


    def stop_select_multiple_leaf(self, event):

        leaves_to_move = self.C.find_overlapping(self._select_drag_start_x, self._select_drag_start_y, event.x, event.y)
        left_leaf_ids = [[i,self.C.leafpairs[i].leftleaf] for i in range(len(self.C.leafpairs))]
        right_leaf_ids = [[i,self.C.leafpairs[i].rightleaf] for i in range(len(self.C.leafpairs))]
        left_leaves = []
        right_leaves = []
        for i in range(len(left_leaf_ids)):
            if left_leaf_ids[i][1] in leaves_to_move and left_leaf_ids[i][1] != self.leftleaf:
                left_leaves += [i]
        for i in range(len(right_leaf_ids)):
            if right_leaf_ids[i][1] in leaves_to_move and right_leaf_ids[i][1] != self.rightleaf:
                right_leaves += [i]

        for i in left_leaves:
            self.C.leafpairs[i].select_left_leaf(event, other=True)
        for i in right_leaves:
            self.C.leafpairs[i].select_right_leaf(event, other=True)

        self.dragging = False
        self.C.tag_bind(self.leftleaf, "<B1-Motion>", self.drag_motion)
        self.C.tag_bind(self.rightleaf, "<B1-Motion>", self.drag_motion)
        self.C.tag_unbind(self.leftleaf, "<ButtonRelease-1>")
        self.C.tag_unbind(self.rightleaf, "<ButtonRelease-1")

    def select_right_leaf(self, event, other=False):
        if other:
            self.name.append("rightleaf")
            self.name = list(set(self.name))
            self.C.itemconfigure(self.rightleaf, fill="green")
            self.C.itemconfigure(self.rightleaftext, fill="white")
            self.right_selected = True
            self.dragging = False
            return
        
        if self.right_selected == True:
            self.C.itemconfigure(self.rightleaf, fill="grey40")
            self.C.itemconfigure(self.rightleaftext, fill="black")
            self.right_selected = False
            self.name.pop(self.name.index("rightleaf"))

        else:
            self.name.append("rightleaf")
            self.name = list(set(self.name))
            self.C.itemconfigure(self.rightleaf, fill="green")
            self.C.itemconfigure(self.rightleaftext, fill="white")
            self.right_selected = True
            self.dragging = False

        if not other:
            self.dragging = True
            self._select_drag_start_x = event.x
            self._select_drag_start_y = event.y
            self.C.tag_bind(self.rightleaf, "<B1-Motion>", self.select_multiple_leaf)
            self.C.tag_bind(self.rightleaf, "<ButtonRelease-1>", self.stop_select_multiple_leaf)