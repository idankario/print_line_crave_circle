#This program create line circle and cravew
""""**********************************************
    *  Student 1 :  Shani Levi     ID: 302853619  
    *  Student 2 :  Idan Kario     ID: 300853751  
    **********************************************
"""
#Import Libraries
from tkinter import *
from PIL import Image, ImageTk



HEIGHT = 600
WIDTH = 800

option_figure = ['Line','Circle','Cerve']
option_curve = [10,50,100,1000]

class DrowingApp:
    def __init__(self, master):
        self.master = master
        master.title("GUI HW1 By Shani & Idan")
        # Color of the shape
        self.my_color = "Black"
        self.my_figure = "Line"
        self.my_curve = 10
        self.my_point = 1
        # Holds the selected point
        self.x = [0,0,0,0]
        self.y = [0,0,0,0]

        # Canvas widget to display graphical elements like lines or text
        self.canvas = Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack(expand=YES, fill=BOTH)

        #Set img background
        bg = PhotoImage("bg.png")
   
        my_label = Label(self.master,image=bg)
        my_label.bg = render
        my_label.place(x=0, y=0,relwidth=1,relheight=1)

        # Uper section
        frame = Frame(self.master, bg='#80c1ff', bd=5)
        frame.place(relx=0.5, rely=0.1,relwidth=0.75, relheight=0.1, anchor='n')

        # lower section
        self.lower_frame = Canvas(self.master,bg='#80c1ff', bd=5)
        self.lower_frame.place(relx=0.5, rely=0.25,relwidth=0.75, relheight=0.6, anchor='n')
        self.lower_frame.bind("<ButtonPress-1>", self.click)

        # Set figures variable and trace changes
        self.figure_val = StringVar(frame)
        self.figure_val.set(option_figure[0])
        figure = OptionMenu(frame, self.figure_val, *option_figure)
        self.figure_val.trace("w", self.change_option)
        figure.place(relwidth=0.20, relheight=1)

        # Set curve variable and trace changes
        self.curve_val = IntVar(frame)
        self.curve_val.set(option_curve[0])
        curve = OptionMenu(frame, self.curve_val, *option_curve)
        self.curve_val.trace("w", self.change_option)
        curve.place(relx=0.25, relwidth=0.20, relheight=1)

        # Set color button
        color = Button(frame, text="Color",command=self.color_option)
        color.place(relx=0.50, relwidth=0.20, relheight=1)

        # Set clear button
        clear = Button(frame, text="Clear", command=lambda: self.lower_frame.delete("all"))
        clear.place(relx=0.80, relwidth=0.20, relheight=1)

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


# main
if __name__ == '__main__':
    """Toplevel widget of Tk which represents mostly the main window
    of an application. It has an associated Tcl interpreter."""
    root = Tk()
    my_gui = DrowingApp(root)
    root.mainloop()