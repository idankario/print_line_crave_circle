
#This program create line circle and cravew
""""**********************************************
    *  Student 1 :  Shani Levi     ID: 302853619  
    *  Student 2 :  Idan Kario     ID: 300853751  
    **********************************************
"""
#Import Libraries
from tkinter import Tk,Canvas,Frame, Label, OptionMenu, Button, StringVar,IntVar
from tkinter_custom_button import TkinterCustomButton
from tkinter import colorchooser
from PIL import Image, ImageTk
option_figure = ['Line','Circle','Cerve']
option_curve = [10,50,100,1000]
class DrowingApp:
    def __init__(self,master,WIDTH=1100,HEIGHT=600):
        master.title("GUI HW1 By Shani & Idan")
        self.init_Val()
        self.create_canvas(master,WIDTH,HEIGHT)
        master.attributes("-transparentcolor", "red") 
        self.create_upper_menu()
        # lower section
        self.lower_frame = Canvas(self.master,bg='#c9daf8', bd=5)
        self.lower_frame.place(relx=0.5, rely=0.25,relwidth=0.75, relheight=0.6, anchor='n')
        self.lower_frame.bind("<ButtonPress-1>", self.click)
    def create_upper_menu(self):
        # Uper section
        frame = Frame(self.master, bg='#a0dbd1', bd=4)
        frame.place(relx=0.5, rely=0.1,relwidth=0.75, relheight=0.1, anchor='n')
        # Set curve and figure variable and trace changes
        self.figure_val=StringVar(frame)
        self.create_OptionMenu(self.figure_val,frame,option_figure[0],0.05,option_figure)
        self.curve_val = IntVar(frame)
        self.create_OptionMenu(self.curve_val,frame,option_curve[0],0.30,option_curve)
        # Set color button
        color = TkinterCustomButton(master=frame,height=52, text="Color",command=self.color_option)
        color.place(relx=0.55)
        # Set clear button
        clear = TkinterCustomButton(master=frame,height=52, text="Clear", command=lambda: self.lower_frame.delete("all"))
        clear.place(relx=0.80)
    def create_OptionMenu(self,s,frame,val,loc,func):
        # Set figures variable and trace changes
        s.set(val)
        s.trace("w", self.change_option)
        om = OptionMenu(frame, s, *func)
        om.place(relx=loc, relwidth=0.15, relheight=1)
        om.config(bg = "#2874A6") 
        om ["menu"] ["bg"] = "#2874A6"
        om ["activebackground"] = "#5499C7"
    def init_Val(self):
        self.my_color = "Black"
        self.my_figure = "Line"
        self.my_curve = 10
        self.my_point = 1
        # Holds the selected point
        self.x = [0,0,0,0]
        self.y = [0,0,0,0]
    def create_canvas(self,master,WIDTH,HEIGHT):
        self.master = master
        self.rootgeometry(WIDTH,HEIGHT)
        self.canvas = Canvas(self.master)
        self.canvas.pack()
        self.background_image = Image.open('bg.PNG') 
        self.image_copy = self.background_image.copy()
        self.background = ImageTk.PhotoImage(self.background_image)
        self.loadbackground()
    def change_option(self, *args):
        # Set my_point to first click
        self.my_point == 1
        # Set values
        self.my_figure = self.figure_val.get()
        self.my_curve = self.curve_val.get()

    def click(self, event):
        # Get (x,y)
        if self.my_point == 1:
            # Get first x,y
            self.x[0] = event.x
            self.y[0] = event.y
            self.my_point = 2
            return
        if self.my_point == 2:
            # Get sec x,y
            self.x[1] = event.x
            self.y[1] = event.y
            self.my_point = 3

            # check if line or circle
            # if its cerve get 2 more (x,y)
            if self.my_figure == 'Line':
                self.myLine(self.x[0], self.y[0],self.x[1],self.y[1])
                self.my_point = 1
                return
            elif self.my_figure == 'Circle':
                r = self.getR(self.x[0], self.y[0], self.x[1], self.y[1])
                self.myCircle(self.x[0], self.y[0],r)
                self.my_point = 1
                return
            elif self.my_figure == 'Cerve':
                return

        if self.my_point == 3:
            # Get third x,y
            self.x[2] = event.x
            self.y[2] = event.y
            self.my_point = 4
            return

        if self.my_point == 4:
            # Get fourth x,y
            self.x[3] = event.x
            self.y[3] = event.y
            self.my_point = 1

            self.myCurve(self.x[0], self.y[0], self.x[1], self.y[1], self.x[2], self.y[2], self.x[3], self.y[3])
            return

    def color_option(self):
        # variable to store hexadecimal code of color
        color = colorchooser.askcolor()[1]
        if color!=None:
            self.my_color = color
            print(self.my_color)

    def putPixel(self,x_, y_):
        self.lower_frame.create_line(x_, y_, x_ + 1, y_ + 1, fill=self.my_color)

    # Bersenheim
    def myLine(self,x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y_ = y1
        points = []
        for x_ in range(x1, x2 + 1):
            coord = (y_, x_) if is_steep else (x_, y_)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y_ += ystep
                error += dx
        if swapped:
            points.reverse()
        for point in points:
            self.putPixel(point[0], point[1])

    def circle_lines(self, xc, yc, x_, y_):
        self.putPixel(xc + x_, yc + y_)
        self.putPixel(xc - x_, yc + y_)
        self.putPixel(xc + x_, yc - y_)
        self.putPixel(xc - x_, yc - y_)
        self.putPixel(xc + y_, yc + x_)
        self.putPixel(xc - y_, yc + x_)
        self.putPixel(xc + y_, yc - x_)
        self.putPixel(xc - y_, yc - x_)
        return

    def myCircle(self, xc, yc, r):
        x_, y_ = 0, r
        d = 3 - 2 * r
        self.circle_lines(xc, yc, x_, y_)
        while y_ >= x_:
            x_ += 1

            #  check for decision parameter
            #  update d, x, y
            if d > 0:
                y_ -= 1
                d = d + 4 * (x_ - y_) + 10

            else:
                d = d + 4 * x_ + 6
            self.circle_lines(xc, yc, x_, y_)
        return

    def getR(self, x1, y1, x2, y2):
        r = (x2 - x1) ** 2 + (y2 - y1) ** 2
        r = (r ** 0.5)
        return round(r)

    def getVal(self, x1, x2, x3, x4, t):
        ax = -x1 + 3 * x2 - 3 * x3 + x4
        bx = 3 * x1 - 6 * x2 + 3 * x3
        cx = -3 * x1 + 3 * x2
        dx = x1
        res = ax * t ** 3 + bx * t ** 2 + cx * t + dx
        return round(res)

    def myCurve(self, x1, x2, x3, x4, y1, y2, y3, y4):
        xt1 = x1
        yt1 = y1

        for t in range(0, self.my_curve + 1):
            pointx = self.getVal(x1, x2, x3, x4, t / self.my_curve)
            pointy = self.getVal(y1, y2, y3, y4, t / self.my_curve)
            self.myLine(xt1, yt1, pointx, pointy)
            xt1 = pointx
            yt1 = pointy
        return

    def loadbackground(self):
        self.label = Label(self.canvas, image = self.background)
        self.label.bind('<Configure>',self.resizeimage)
        self.label.pack(fill='both', expand='yes')

    def rootgeometry(self,WIDTH,HEIGHT):
   
        self.master.geometry(str(WIDTH) +'x'+str(HEIGHT))

    def resizeimage(self,event):
        image = self.image_copy.resize((self.master.winfo_width(),self.master.winfo_height()))
        self.image1 = ImageTk.PhotoImage(image)
        self.label.config(image = self.image1)
if __name__ == '__main__':
    root = Tk()
    my_gui = DrowingApp(root)
    root.mainloop()