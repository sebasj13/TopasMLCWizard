import customtkinter as ctk
from .mlc_field import MLCField
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
from .rtplan_loadin import load_fields_from_rtplan
from .topas_loadin import load_fields_from_topas
from .field_def import *
from threading import Thread
import tkdial as tkd

class CF(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, width=660, height=1000)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0, minsize=250)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=0, minsize=300)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=0, minsize=150)
        self.rowconfigure(8, weight=0)
        self.columnconfigure(0, weight=1, minsize=330)
        self.columnconfigure(1, weight=1, minsize=330)   
        self.titleframe = ctk.CTkFrame(self, fg_color="#2B2B2B", border_color="white", border_width=2)
        self.title = ctk.CTkLabel(self.titleframe, text="ESMOCA FieldForge", font=("Bahnschrift", 30, "bold"), fg_color="#2B2B2B")
        self.titleframe.grid_propagate(False)
        self.title.pack(fill="both", pady=(10,10), expand=True, padx=(5,5), side="left")
        self.titleframe.grid(row=0, column=0, columnspan=2, pady=(5,5), sticky="nsew", padx=(5,5))

        self.sequence = []
        self.selected_field = None

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
        self.sq_field.grid(row=5, column=0, pady=(5,5), sticky="nsew", padx=(5,5))

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

        self.rec_field.grid(row=5, column=1, pady=(5,5), sticky="nsew", padx=(5,5))

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
        self.drawrectbutton.grid(row=4, column=0, pady=(5,5), sticky="sew")

        #SAVE/LOAD MLC FIELD
        self.savemlcbutton = ctk.CTkButton(self, text="Save MLC Field", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.save_mlc_field)
        self.savemlcbutton.grid(row=6, column=0, columnspan=2,  pady=(5,5), sticky="n")

        #SHOW/LOAD/SAVE MLC SEQUENCE

        self.saveframe = ctk.CTkFrame(self, fg_color="#2B2B2B", height=35)
        self.saveframe.grid_propagate(False)
        self.saveframe.rowconfigure(0)
        self.saveframe.columnconfigure(0, weight=1)
        self.saveframe.columnconfigure(1, weight=1)
        self.saveframe.columnconfigure(2, weight=1)
        self.showsequencebutton = ctk.CTkButton(self.saveframe, text="Show MLC Sequence", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.show_mlc_sequence)
        self.showsequencebutton.grid(row=0, column=0, pady=(5,5), sticky="nsew")
        self.loadsequencebutton = ctk.CTkButton(self.saveframe, text="Load MLC Sequence", font=("Bahnschrift", 15), fg_color="#2B2B2B", command= lambda: Thread(target=self.load_mlc_sequence).start())
        self.loadsequencebutton.grid(row=0, column=1, pady=(5,5), sticky="nsew")
        self.savesequencebutton = ctk.CTkButton(self.saveframe, text="Save MLC Sequence", font=("Bahnschrift", 15), fg_color="#2B2B2B", command=self.save_mlc_sequence)
        self.savesequencebutton.grid(row=0, column=2, pady=(5,5), sticky="nsew")
        self.saveframe.grid(row=8, column=0, columnspan=2, pady=(5,5), sticky="nsew", padx=(5,5))

        #FIELD SEQUENCE BROWSER
        self.fieldseqframe = ctk.CTkFrame(self, fg_color="#2B2B2B", border_color="white", border_width=2)
        self.fieldseqframe.grid_propagate(False)
        self.fieldseqframe.rowconfigure(0, weight=0)
        self.fieldseqframe.rowconfigure(1, weight=1)
        self.fieldseqframe.columnconfigure(0, weight=1)
        self.fieldseqtitle = ctk.CTkLabel(self.fieldseqframe, text="Field Sequence", font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.fieldseqscrollframe = ctk.CTkScrollableFrame(self.fieldseqframe, orientation="horizontal")
        self.fieldseqscrollcanvas = ctk.CTkCanvas(self.fieldseqscrollframe, width=100, height=110, bg="#2B2B2B", borderwidth=0, highlightthickness=0)
        self.fieldseqscrollcanvas.bind("<Double-Button-1>", self.load_mlc_field)
        self.fieldseqtitle.grid(row=0, column=0, pady=(5,5), sticky="nsew", padx=(5,5))
        self.fieldseqscrollframe.grid(row=1, column=0, pady=(5,5), sticky="nsew", padx=(5,5))
        self.fieldseqscrollcanvas.pack(fill="both", expand=True)
        self.fieldseqframe.grid(row=7, column=0, columnspan=2, pady=(5,5), sticky="sew", padx=(5,5))


        self.dialframe = ctk.CTkFrame(self, fg_color="#2B2B2B", border_color="white", border_width=2)
        self.dialframe.grid_propagate(False)    
        self.dialframe.rowconfigure(0, weight=1)
        self.dialframe.rowconfigure(1, weight=0)
        self.dialframe.columnconfigure(0, weight=1)
        self.dialframe.columnconfigure(1, weight=1)
        self.dialframe.columnconfigure(2, weight=1)

        self.gantrydial = tkd.Jogwheel(self.dialframe, text="Gantry: ", start=360, end=00, start_angle=90, divisions=22.5, scroll_steps=1, end_angle=360,button_radius=10, fg="#2B2B2B", bg="#2B2B2B", text_color="white", text_font=("Bahnschrift", 10), radius=180, integer=True)
        self.gantrydial.grid(row=0, column=0, pady=(10,5), sticky="nsew", padx=(25,5))
        self.gantrydial.set(0)
        self.collimatordial = tkd.Jogwheel(self.dialframe, text="Collimator: ", start=360, end=0, divisions=22.5, start_angle=90, end_angle=360,scroll_steps=1, button_radius=10, fg="#2B2B2B", bg="#2B2B2B", text_color="white", text_font=("Bahnschrift", 10), radius=180, integer=True)
        self.collimatordial.grid(row=0, column=1, pady=(10,5), sticky="nsew", padx=(5,5))    
        self.collimatordial.set(0)
        self.couchdial = tkd.Jogwheel(self.dialframe,text="Couch: ", start=360, end=0, divisions=22.5, start_angle=90, end_angle=360, scroll_steps=1, button_radius=10, fg="#2B2B2B", bg="#2B2B2B", text_color="white", text_font=("Bahnschrift", 10), radius=180, integer=True)
        self.couchdial.grid(row=0, column=2, pady=(10,5), sticky="nsew", padx=(5,5))
        self.couchdial.set(0)
        self.SSDandDepth = ctk.CTkFrame(self.dialframe, fg_color="#2B2B2B")
        self.SSDandDepth.columnconfigure(0, weight=1)
        self.SSDandDepth.columnconfigure(1, weight=1)
        self.SSDandDepth.columnconfigure(2, weight=1)
        self.SSDandDepth.columnconfigure(3, weight=1)

        self.SSD = ctk.StringVar(value="90")
        self.Depth = ctk.StringVar(value="10")
        self.SSDLabel = ctk.CTkLabel(self.SSDandDepth, text="Source-Surface-Distance:", font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.SSDEntry = ctk.CTkEntry(self.SSDandDepth, width=60, font=("Bahnschrift", 15), fg_color="#2B2B2B", textvariable=self.SSD)
        self.DepthLabel = ctk.CTkLabel(self.SSDandDepth, text="Depth:", font=("Bahnschrift", 15), fg_color="#2B2B2B")
        self.DepthEntry = ctk.CTkEntry(self.SSDandDepth, width=60, font=("Bahnschrift", 15), fg_color="#2B2B2B", textvariable=self.Depth)
        self.SSDLabel.grid(row=0, column=0, pady=(5,5), sticky="nse", padx=(5,5))
        self.SSDEntry.grid(row=0, column=1, pady=(5,5), sticky="nsw", padx=(5,5))
        self.DepthLabel.grid(row=0, column=2, pady=(5,5), sticky="nse", padx=(5,5))
        self.DepthEntry.grid(row=0, column=3, pady=(5,5), sticky="nsw", padx=(5,5))
        self.SSDandDepth.grid(row=1, column=0, columnspan=3, pady=(5,5), sticky="sew", padx=(5,5))
        self.dialframe.grid(row=1, column=0, columnspan=2, pady=(5,5), sticky="nsew", padx=(5,5))



    def save_mlc_field(self):
        leaf_positions = []
        for leafpair in self.parent.C.leafpairs:
            leaf_positions.append(leafpair.get_leaf_positions())
        jaw_positions = self.parent.C.jawpair.get_jaw_positions() 
        if self.selected_field == None:
            self.sequence.append(MLCField(self.fieldseqscrollcanvas, self, leaf_positions, jaw_positions, self.gantrydial.get(), self.collimatordial.get(), self.couchdial.get(), self.SSD.get(), self.Depth.get(), len(self.sequence)))
        else:
            self.sequence[self.selected_field].delete()
            self.sequence[self.selected_field] = MLCField(self.fieldseqscrollcanvas, self, leaf_positions, jaw_positions, self.gantrydial.get(), self.collimatordial.get(), self.couchdial.get(), self.SSD.get(), self.Depth.get(), self.selected_field)

        self.selected_field = None

    def load_mlc_sequence(self):
        file = askopenfilename(filetypes=[("RTPLAN", "*.dcm"), ("TOPAS Sequence", "*.txt")])
        if file == "": return

        if file.endswith(".txt"):
            load_fields_from_topas(file, self.fieldseqscrollcanvas, self)
        elif file.endswith(".dcm"):
            load_fields_from_rtplan(file, self.fieldseqscrollcanvas, self)

    def show_mlc_sequence(self, iteration=0):
        time = 200
        if len(self.sequence) > 10: time = 50
        if iteration == len(self.sequence):
            try: self.sequence[-1].unselected()
            except Exception: pass
            [field.unselected() for field in self.sequence]
            self.selected_field = None
            return
        if iteration == 0:
            if self.sequence[0].select == True: self.sequence[0].unselected()
        self.fieldseqscrollframe._parent_canvas.xview("moveto", max([0,iteration-2])/len(self.sequence))
        self.load_mlc_field(index=self.sequence[iteration].index, show=True)
        self.after(time, lambda: self.show_mlc_sequence(iteration+1))

    def save_mlc_sequence(self):
        if len(self.sequence) == 0: return
        planname = asksaveasfilename(filetypes=[("TOPAS Sequence", "*.txt")])
        cluster = askyesno("Cluster", "Define field for the IANVS cluster environment?")
        if planname == "": return
        gantry_angles, collimator_angles, couch_angles, left_jaw_positions, right_jaw_positions, ssd, depth = [], [], [], [], [], [], []
        left_leaf_positions, right_leaf_positions, = [[] for i in range(len(self.sequence))], [[] for i in range(len(self.sequence))]
        for i, field in enumerate(self.sequence):
            gantry_angles += [field.gantry_angle]
            collimator_angles += [field.collimator_angle]
            couch_angles += [field.couch_angle]
            ssd += [float(field.ssd)]
            depth += [float(field.depth)]
            field.leaf_positions.reverse()
            for j in range(80):
                left_leaf_positions[i] += [field.leaf_positions[j][0]]
                right_leaf_positions[i] += [field.leaf_positions[j][1]]
                if left_leaf_positions[i][-1] == right_leaf_positions[i][-1]:
                    left_leaf_positions[i][-1] -= 1
                    right_leaf_positions[i][-1] += 1
            field.leaf_positions.reverse()
            left_jaw_positions += [field.jaw_positions[1]]
            right_jaw_positions += [field.jaw_positions[0]]

        CreateTopasArcSequence(planname, gantry_angles, collimator_angles, couch_angles, left_leaf_positions, right_leaf_positions, left_jaw_positions, right_jaw_positions, ssd, depth, cluster)

    def load_mlc_field(self, event=None, index=None, show=False):

        if index == None:
            index = self.fieldseqscrollcanvas.find_closest(event.x, event.y)[0]
            for i in range(len(self.sequence)):
                if self.sequence[i].image_id == index:
                    index = i
                    break
        if not show: self.sequence[index].selected()
        for i, leafpair in enumerate(self.parent.C.leafpairs):

            leafpair.set_left_leaf(self.sequence[index].leaf_positions[i][0], checks=False)
            leafpair.set_right_leaf(self.sequence[index].leaf_positions[i][1], checks=False)
        
        self.gantrydial.set(self.sequence[index].gantry_angle)
        self.collimatordial.set(self.sequence[index].collimator_angle)
        self.couchdial.set(self.sequence[index].couch_angle)
        self.SSD.set(self.sequence[index].ssd)
        self.Depth.set(self.sequence[index].depth)
        self.parent.C.jawpair.set_top_jaw(self.sequence[index].jaw_positions[0])
        self.parent.C.jawpair.set_bottom_jaw(self.sequence[index].jaw_positions[1])

        self.selected_field = index


    def drag_field(self, event):

        index = self.fieldseqscrollcanvas.find_closest(event.x, event.y)[0]
        for i in range(len(self.sequence)):
            if self.sequence[i].image_id == index:
                index = i
                break

        self.sequence[index].drag_start_x = event.x
           
        def drag_motion(event, mlc_field=self.sequence[index], old_index = index, sequence = self.sequence):
            index = mlc_field.index
            new_loc = event.x - mlc_field.drag_start_x + old_index*110


            locations_left = [i*110 for i in range(len(self.sequence))]
            locations_right = [i+100 for i in locations_left]

            if index == 0:
                left, right = 0, 60
                leftindex, rightindex = 0, 1
            elif index == len(self.sequence)-1:
                left, right = locations_left[-1]-60, locations_right[-1]
                leftindex, rightindex = len(self.sequence)-2, len(self.sequence)-1
            else:
                left = locations_right[index-1]-60
                right = locations_left[index]+50
                leftindex, rightindex = index-1, index+1

            if new_loc < left:
                mlc_field.C.moveto(sequence[leftindex].image_id, mlc_field.index*110, 5)
                mlc_field.C.moveto(sequence[leftindex].close_image_id, mlc_field.index*110+40, 105)
                sequence[leftindex].index, sequence[index].index = sequence[index].index, sequence[leftindex].index
                sequence[leftindex], sequence[index] = sequence[index], sequence[leftindex]

            elif new_loc > right:
                mlc_field.C.moveto(sequence[rightindex].image_id, mlc_field.index*110, 5)
                mlc_field.C.moveto(sequence[rightindex].close_image_id, mlc_field.index*110+40, 105)
                sequence[rightindex].index, sequence[index].index = sequence[index].index, sequence[rightindex].index
                sequence[rightindex], sequence[index] = sequence[index], sequence[rightindex]

            mlc_field.C.moveto(mlc_field.image_id, new_loc, 5)
            mlc_field.C.moveto(mlc_field.close_image_id, new_loc+40, 105)


        def drag_release(event, mlc_field =self.sequence[index], index=index):
            new_loc = event.x - mlc_field.drag_start_x + index*110
            locations = [i*110 for i in range(len(self.sequence))]
            new_loc = min(locations, key=lambda x:abs(x-new_loc))
            mlc_field.C.moveto(mlc_field.image_id, new_loc, 5)
            mlc_field.C.moveto(mlc_field.close_image_id, new_loc+40, 105)
            self.fieldseqscrollcanvas.unbind("<B1-Motion>")
            self.fieldseqscrollcanvas.unbind("<ButtonRelease-1>")
            if self.selected_field != None:
                self.selected_field = mlc_field.index


        self.fieldseqscrollcanvas.bind("<B1-Motion>", drag_motion)
        self.fieldseqscrollcanvas.bind("<ButtonRelease-1>", drag_release)

    def square(self, value=None):
        if value == None:
            try: field_size = 10*float(self.squareentry.get())
            except ValueError: return
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
            self.parent.C.unbind("<Enter>")

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

            if x1 < 150:
                x1 = 150
            if x2 > 150 + 960:
                x2 = 150 + 960
            if y1 < 0:
                y1 = 20
            if y2 > 1000:
                y2 = 980

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
                        
            self.parent.C.unbind("<Enter>")
            self.parent.C.unbind("<Motion>")
            self.parent.C.unbind("<Button-1>")
            self.parent.C.unbind("<B1-Motion>")
            self.parent.C.unbind("<ButtonRelease-1>")
            self.parent.C.delete(self.tooltip)

        self.parent.C.bind("<Enter>", on_enter)
        self.parent.C.bind("<Button-1>", drawrect_start)
        self.parent.C.bind("<Motion>", mouse_motion)
        self.parent.C.bind("<B1-Motion>", drawrect_motion)
        self.parent.C.bind("<ButtonRelease-1>", drawrect_release)
        self.square(value=40)

    def offaxis(self):
        try: x1, y1, x2, y2 = float(self.x1entry.get())*10, float(self.y1entry.get())*10, float(self.x2entry.get())*10, float(self.y2entry.get())*10
        except ValueError: return
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