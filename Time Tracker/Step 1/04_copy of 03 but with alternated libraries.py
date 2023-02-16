import time
from tkinter import *
from tkinter import font
from plyer import notification
import playsound
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

"""The script sends each second a notification """

import wxPython

class TimeTrackerTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.icon = wx.Icon("path/to/icon.png")
        self.SetIcon(self.icon, "Time Tracker")

    def CreatePopupMenu(self):
        menu = wx.Menu()
        show_window_item = menu.Append(wx.ID_ANY, "Show Window")
        self.Bind(wx.EVT_MENU, self.OnShowWindow, show_window_item)
        return menu

    def OnShowWindow(self, event):
        self.frame.Show()

def show_window(icon):
    """Brings the main window back into view."""
    icon.visible = False
    root.deiconify()


def update_icon(icon):
    while True:
        # Create an image with a black background and yellow text for the time
        img = Image.new('RGB', (100, 100), color=(0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((5, 5), time.strftime('%H:%M:%S'), fill=(255, 255, 0))
        # Update the icon with the new image
        icon.icon = img
        # Pause for 1 second before updating again
        time.sleep(1)


# Create the initial image for the icon
img = Image.new('RGB', (100, 100), color=(0, 0, 0))
d = ImageDraw.Draw(img)
d.text((5, 5), time.strftime('%H:%M:%S'), fill=(255, 255, 0))

# Create the icon and start the update function
icon = Icon('Time Tracker', img)
icon.visible = True
update_icon(icon)

# create the initial system tray icon
img = Image.new('RGB', (100, 100), color=(73, 109, 137))
d = ImageDraw.Draw(img)
d.text((5, 5), "00:00:00", fill=(255, 255, 0))
icon = Icon("name", img, "Time Tracker")


# icon.run()


def update_clock():
    """This function updates the clock display and schedules itself to run again after 1 second."""

    current_time = time.strftime("%Y/%m/%d %H:%M:%S")
    login_time = time.strftime("%H:%M:%S", time.localtime(start_time))
    elapsed_time = int(time.time() - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_time = calculate_remaining_time()

    # update the system tray icon with the current time
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((5, 5), f"{hours:02}:{minutes:02}:{seconds:02}", fill=(255, 255, 0))
    icon.icon = Icon("name", img, "Time Tracker")

    # Create a Pystray menu with a "Show Window" item that calls show_window() when clicked
    menu = Menu(MenuItem('Show Window', show_window))

    # Set the icon menu to the Pystray menu
    icon.menu = menu

    clock_label.config(
        text=f"Current time {current_time}\n\n"
             f"Login Time: {login_time}\n\n"
             f"Time Worked: {hours:02}:{minutes:02}:{seconds:02}\n\n"
             f"Remaining Time: {remaining_time}")
    clock_label.after(1000, update_clock)
    check_for_lunch_break()
    transmit_signal(
        f"Time Tracker Update:\nTime Worked: {hours:02}:{minutes:02}:{seconds:02}\n"
        f"Remaining Time: {remaining_time}", "Time Tracker Update", hours, minutes, seconds)


def send_notification(message, title):
    """Displays the notification message with the given title."""

    n = notification.notify(title=title, message=message, timeout=5)
    n.send()


def transmit_signal(message, title, hours, minutes, seconds):
    """Show live update in the taskbar"""

    n = notification.notify(
        title=title,
        message=f"Time Worked: {hours:02}:{minutes:02}:{seconds:02}\nRemaining Time: {calculate_remaining_time()}",
        timeout=5)
    if n is not None:
        n.send()


def set_lunch_break():
    """the function sets the lunch break time and disables the lunch break entry field."""
    global lunch_break_set
    global lunch_break_hour
    global lunch_break_minute
    lunch_break_hour = int(lunch_break_entry.get().split(":")[0])
    lunch_break_minute = int(lunch_break_entry.get().split(":")[1])
    lunch_break_set = True
    lunch_break_entry.config(state='disabled')
    set_lunch_break_button.config(text='Edit', command=edit_lunch_break)


def edit_lunch_break():
    """This function enables editing of the lunch break time and enables the lunch break entry field."""
    global lunch_break_set
    lunch_break_set = False
    lunch_break_entry.config(state='normal')
    set_lunch_break_button.config(text='Set', command=set_lunch_break)


def check_for_lunch_break():
    if lunch_break_set:
        current_hour = int(time.strftime("%H"))
        current_minute = int(time.strftime("%M"))
        if current_hour == lunch_break_hour and current_minute == lunch_break_minute:
            playsound('C:\Windows\Media\Alarm08.wav')


def calculate_remaining_time():
    """this function calculates remaining time if the end of the working day is considered to be 18:30 each day"""
    end_of_day = 18 * 3600
    current_seconds = int(time.time() - time.mktime(time.localtime()[:3] + (0, 0, 0, 0, 0, 0)))
    remaining_seconds = end_of_day - current_seconds
    if remaining_seconds < 0:
        return "Working day ended"

    hours, remainder = divmod(remaining_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# Initialize the notification system
# notification.init('Time Tracker')

# Set the start time and lunch break variables
start_time = time.time()
lunch_break_set = False

# Set up the window
root = Tk()
root.geometry("400x330")
root.attributes("-topmost", True)
root.attributes("-toolwindow", True)
root.resizable(False, False)
root.title("Time Tracker")

# Set up the clock appearance
clock_font = font.Font(family="calibri", size=15, weight="normal")
clock_label = Label(root, text="", font=clock_font)
clock_label.pack(pady=20)

# Set up the lunch break labels and buttons
lunch_time_label = Label(root, text="Lunch Time (HH:MM):")
lunch_time_label.pack()
lunch_break_entry = Entry(root)
lunch_break_entry.pack()
lunch_break_entry.insert(0, "12:00")
set_lunch_break_button = Button(root, text="Set", command=set_lunch_break)
set_lunch_break_button.pack()


def check_for_lunch_break_notification():
    if lunch_break_set:
        current_hour = int(time.strftime("%H"))
        current_minute = int(time.strftime("%M"))
        if current_hour == lunch_break_hour and current_minute == lunch_break_minute:
            notification.notify(title="Time Tracker", message="It's time for lunch!", timeout=5)


# Start the clock and hide the window
update_clock()
# root.withdraw()
root.mainloop()
