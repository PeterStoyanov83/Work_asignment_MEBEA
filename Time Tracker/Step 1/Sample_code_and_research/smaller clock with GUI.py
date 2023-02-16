# importing the entire tkinter module
from tkinter import *
from tkinter.ttk import *

# to retrieve the system's time, you need to import the strftime function
from time import strftime

# creation of the tkinter window
main = Tk()
main.title('time')


# This function displays the current time on the label defined herein
def display_time():
    string = strftime('%H:%M:%S %p')
    clock_label.config(text=string)
    clock_label.after(1000, display_time)


# creating an attractive look:  needs styling the label widget
clock_label = Label(main, font=('calibri', 50, 'bold'),
                    background='white',
                    foreground='gray')

# defining how to place the digital clock at the centre tkinter's window
clock_label.pack(anchor='center')
display_time()

mainloop()
