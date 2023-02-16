from tkinter import *
from tkinter.ttk import *
import datetime
import platform
import winsound

type = "windows"
import os

window = Tk()
window.title("MEBEA CLOCK-IN/OUT SYSTEM")
window.geometry('500x250')
work_time_counter_num = 66600
work_time_counter_running = False
timer_counter_num = 66600
timer_counter_num_running = False
stopwatch_counter_num = 66600
stopwatch_running = False

# generating a general real time clock to show time at the moment
def general_clock():
    date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S/%p")
    date, time1 = date_time.strip()
    time2, time3 = time1.split("/")
    hour, minutes, seconds = time2.split(':')

    if int(hour) > 11 and int(hour) < 24:
        time = str(int(hour) - 12) + ":" + minutes + ":" + seconds + " " + time3

    else:
        time = time2 + " " + time3
    time_label.config(text=time)  # look for the variables ...
    date_label.config(text=date)
    time_label.after(1000, general_clock)


# creating a break reminder
def break_reminder():
    main_time = datetime.datetime.now().strftime("%H:%M %p")
    alarm_time = get_alarm_time_entry.get()
    alarm_time1, alarm_time2 = alarm_time.split(' ')
    alarm_hour, alarm_minutes = alarm_time1.split(':')
    main_time1, main_time2 = main_time.split(' ')
    main_hour1, main_minutes = main_time1.split(':')
    if int(main_hour1) > 12 and int(main_hour1) < 24:
        main_hour = str(int(main_hour1) - 12)
    else:
        main_hour = main_hour1
    if int(alarm_hour) == int(main_hour) and int(alarm_minutes) == int(main_minutes) and main_time2 == alarm_time2:
        for i in range(3):
            alarm_status_label.config(text='Time Is Up')
            if platform.system() == 'Windows':
                winsound.Beep(5000, 1000)
            elif platform.system() == 'Darwin':
                os.system('say Time is Up')
            elif platform.system() == 'Linux':
                os.system('beep -f 5000')
        get_alarm_time_entry.config(state='enabled')
        set_alarm_button.config(state='enabled')
        get_alarm_time_entry.delete(0, END)
        alarm_status_label.config(text='')
    else:
        alarm_status_label.config(text='Alarm Has Started')
        get_alarm_time_entry.config(state='disabled')
        set_alarm_button.config(state='disabled')
    alarm_status_label.after(1000, break_reminder)


# time worked. it will start with clock-in system
def stopwatch_counter(label):
    pass


tabs_control = Notebook(window)
clock_tab = Frame(tabs_control)
alarm_tab = Frame(tabs_control)
stopwatch_tab = Frame(tabs_control)
timer_tab = Frame(tabs_control)
tabs_control.add(clock_tab, text="Clock")
tabs_control.add(alarm_tab, text="break reminder")
tabs_control.add(stopwatch_tab, text='time worked')
# tabs_control.add(timer_tab, text='Timer')
tabs_control.pack(expand=1, fill="both")
time_label = Label(clock_tab, font='calibri 40 bold', foreground='black')
time_label.pack(anchor='center')
date_label = Label(clock_tab, font='calibri 40 bold', foreground='black')
date_label.pack(anchor='s')

# adding alarm to the system
get_alarm_time_entry = Entry(alarm_tab, font='calibri 15 bold')
get_alarm_time_entry.pack(anchor='center')
alarm_instructions_label = Label(alarm_tab, font='calibri 10 bold',
                                 text="Enter Alarm Time. Eg -> 01:30 PM, 01 -> Hour, 30 -> Minutes")
alarm_instructions_label.pack(anchor='s')
set_alarm_button = Button(alarm_tab, text="Set Alarm", command=break_reminder)
set_alarm_button.pack(anchor='s')
alarm_status_label = Label(alarm_tab, font='calibri 15 bold')
alarm_status_label.pack(anchor='s')

# adding stopwatch counter to the system
stopwatch_label = Label(stopwatch_tab, font='calibri 40 bold', text='Stopwatch')
stopwatch_label.pack(anchor='center')
stopwatch_start = Button(stopwatch_tab, text='Start', command=lambda: stopwatch_counter('start'))
stopwatch_start.pack(anchor='center')
stopwatch_stop = Button(stopwatch_tab, text='Stop', state='disabled', command=lambda: stopwatch_counter('stop'))
stopwatch_stop.pack(anchor='center')
stopwatch_reset = Button(stopwatch_tab, text='Reset', state='disabled', command=lambda: stopwatch_counter('reset'))
stopwatch_reset.pack(anchor='center')
