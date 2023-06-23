import tkinter as tk
from tkinter import *
import threading
from time import sleep
import ctypes
import obspython as obs


# --------------------------------------------------

lastClickX = 0
lastClickY = 0

clickReleaseX = 0
clickReleaseY = 0

x = 0
y = 0

window = None

timer_enable = True

is_paused = False

#----------------------------------------------------------------------------------------

# ***** VARIABLES *****
# use a boolean variable to help control state of time (running or not running)
running = False
# time variables initially set to 0
hours, minutes, seconds = 0, 0, 0

#----------------------------------------------------------------------------------------

loop_destroy = False 
window_start = False

class Application(tk.Frame):              
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.config(bg="grey")   
        self.pack()                
        self.master.attributes('-alpha', 0.4) # window opacity
        self.master.overrideredirect(True)


        def get_scale_factor(self):
            user32 = ctypes.windll.user32
            dpi_scale = user32.GetDpiForWindow(self.master.winfo_id()) / 96
            return dpi_scale


        # changes the window default opacity 0 to 1
        win_opacity = 0.8

        # calculate the screen width based on the resolution
        screen_width = self.master.winfo_screenwidth()
        screen_x= int(screen_width/2)

        self.master.attributes('-alpha', win_opacity) # window opacity
        self.master.configure(bg='grey') # window color
        self.master.overrideredirect(1) # borderless window
        self.master.attributes('-topmost', True) # keep always on top
        self.master.geometry(f'{140}x{28}+{screen_x}+{0}') # window size(x) and position (+)

        global canvas
        canvas = Canvas(self,height='25',width='30', bg='grey',highlightthickness=0) # canvas for REC button
        canvas.create_oval(21, 21, 2, 3, outline='grey25', fill='grey40')
        canvas.create_oval(20, 20, 4, 5, fill='red', outline='' )
        canvas.grid(row=0, column=0, pady=(1,0))

        global label
        label = Label(self,text="Recording")
        label.grid(row=0,column=1, pady=(1,0))
        label.config(bg="grey",fg="white")

        if timer_enable == True:
            global stopwatch_label # modify the stopwatch from global
            stopwatch_label = Label(self, text='00:00:00', font=('Arial', 20),bg="grey",fg="white" )  # show the clock an pack it
            stopwatch_label.grid(row='1',column= '0',columnspan='2')
            self.master.geometry(f'{140}x{61}+{screen_x}+{0}')
            # start()  #start the timer function


        # snap window to borders function
        def ClickRelease(event):
            resolutionX = self.master.winfo_screenwidth() # gets the actual screen resolution
            resolutionY = self.master.winfo_screenheight()
            global x, y
            if self.master.winfo_y() < 0:  # if the current window position is below 0 , then move the window
                self.master.geometry("+%s+%s" % (x, 0))
            if self.master.winfo_y() > (resolutionY-60):
                self.master.geometry("+%s+%s" % (x,(resolutionY-61)))
            if self.master.winfo_x() < 0:
                self.master.geometry("+%s+%s" % (0, y))
            if self.master.winfo_x() > (resolutionX-140):
                self.master.geometry("+%s+%s" % ((resolutionX-140), y))

        # left click window dragging function
        def SaveLastClickPos(event):
            global lastClickX, lastClickY
            lastClickX = event.x
            lastClickY = event.y


        def Dragging(event):
            global x, y
            x, y = event.x - lastClickX + self.master.winfo_x(), event.y - lastClickY + self.master.winfo_y()
            self.master.geometry("+%s+%s" % (x , y))

            self.master.attributes('-alpha', win_opacity)
            self.master.attributes('-topmost', True)
            self.master.bind('<ButtonRelease-1>', ClickRelease)

            self.master.bind('<Button-1>', SaveLastClickPos)  # click to drag and drop window
            self.master.bind('<B1-Motion>', Dragging)
        
                # open the popup menu
        def open_menu(e):
            popup_menu.tk_popup(e.x_root, e.y_root)

        def pause_from_menu():
            global is_paused
            if not is_paused:
                popup_menu.entryconfig(0, label='Pause Recording')
                obs.obs_frontend_recording_pause(True)
                is_paused = True
            else:
                popup_menu.entryconfig(0, label='Unpause Recording')
                obs.obs_frontend_recording_pause(False)
                is_paused = False
        
        def stop_from_menu():
            global window_start
            global is_paused
            window_start = False
            is_paused = False
            obs.obs_frontend_recording_stop()

        # adds a right-click popup menu to the main frame
        popup_menu = Menu(self, tearoff=False)
        popup_menu.add_command(label='Pause Recording', command=pause_from_menu)
        popup_menu.add_separator()
        popup_menu.add_command(label='Stop Recording', command=stop_from_menu)
        self.master.bind('<Button-3>', open_menu)

        self.master.bind('<ButtonRelease-1>', ClickRelease)
        self.master.bind('<Button-1>', SaveLastClickPos)  # click to drag and drop window
        self.master.bind('<B1-Motion>', Dragging)


    # update stopwatch function
    def update(self):
        # update seconds with (addition) compound assignment operator
        global hours, minutes, seconds
        seconds += 1
        if seconds == 60:
            minutes += 1
            seconds = 0
        if minutes == 60:
            hours += 1
            minutes = 0
        # format time to include leading zeros
        hours_string = f'{hours}' if hours > 9 else f'0{hours}'
        minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
        seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
        # update timer label after 1000 ms (1 second)
        stopwatch_label.config(text=hours_string + ':' + minutes_string + ':' + seconds_string)
        # after each second (1000 milliseconds), call update function
        # use update_time variable to cancel or pause the time using after_cancel
        global update_time
        update_time = stopwatch_label.after(1000, self.update)

    def start(self):
        global running
        if not running:
            self.update()
            running = True

    # reset function
    def reset(self):
        global running
        if running:
            # cancel updating of time using after_cancel()
            stopwatch_label.after_cancel(update_time)
            running = False
        # set variables back to zero
        global hours, minutes, seconds
        hours, minutes, seconds = 0, 0, -1
        # set label back to zero
        stopwatch_label.config(text='00:00:00')
    
    # pause function
    def pause(self):
        global running
        if running:
            # cancel updating of time using after_cancel()
            stopwatch_label.after_cancel(update_time)
            running = False


    def check_loop_status(self):
        global window_start
        global loop_destroy
        global is_paused
        global label
        global canvas
        
        if window_start and not is_paused:
            self.start()
            self.master.attributes('-alpha', 0.9) # window opacity
            label.config(text='Recording')
            canvas.delete("all")
            canvas.create_oval(21, 21, 2, 3, outline='grey10', fill='grey40')
            canvas.create_oval(20, 20, 4, 5, fill='red', outline='' )
        elif not window_start:
            try: # ingnore the error when the clock stops..
                self.reset()
            except Exception:
                pass
            self.master.attributes('-alpha', 0.0) # window opacity

        if loop_destroy:
            self.destroy()
        
        elif is_paused:
            self.pause()
            label.config(text='Recording paused')
            canvas.delete("all")
            canvas.create_rectangle(10, 20, 5, 5, fill='grey20', outline='grey30')
            canvas.create_rectangle(20, 20, 15, 5, fill='grey20', outline='grey30')

        self.after(100, self.check_loop_status)  # Check again after delay.
    
 
def runtk():  # runs in background thread
    app = Application()                        
    app.master.title('Sample application')  
    app.check_loop_status()
    app.mainloop()
        
    
thd = threading.Thread(target=runtk)   # gui thread
thd.daemon = True  # background thread will exit if main thread exits



# ----------------------------   OBS script    ------------------------------------------------------------


class Data:
    OutputDir = None

# this function responds to events inside OBS
def frontend_event_handler(data):
    global is_paused
    global window_start
    global loop_destroy

    if data == obs.OBS_FRONTEND_EVENT_FINISHED_LOADING:
        if not thd.is_alive():
            thd.start()

    if data == obs.OBS_FRONTEND_EVENT_RECORDING_STARTING:
        window_start = True
        is_paused = False

    if data == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        window_start = False
        is_paused = False
        print('REC stops..')

    if data == obs.OBS_FRONTEND_EVENT_RECORDING_PAUSED:
        is_paused = True
        print('REC paused..')

    if data == obs.OBS_FRONTEND_EVENT_RECORDING_UNPAUSED:
        is_paused = False


def script_description():
    return ("OBS RECORDING NOTIFICATION\n\n"
            
            "ATTENTION:\n\n"
            " Restart OBS after adding the script\n\n\n"
            " Installation: \n"
            " You have to select a Python 3.6.8 version package "
            " in the configuration that includes TKinter library,"
            " you can find the embedded package and instructions in my github \n\n "
            " github.com/tobsailbot/obs_recording_notification\n\n")



obs.obs_frontend_add_event_callback(frontend_event_handler)
