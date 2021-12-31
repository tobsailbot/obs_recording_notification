
import obspython as obs
from tkinter import *


#--------------------------------------------------

lastClickX = 0
lastClickY = 0

clickReleaseX = 0
clickReleaseY = 0

x = 0
y = 0

window = None

timer_enable = True
#----------------------------------------------------------------------------------------

# ***** VARIABLES *****
# use a boolean variable to help control state of time (running or not running)
running = False
# time variables initially set to 0
hours, minutes, seconds = 0, 0, 0

# ***** NOTES ON GLOBAL *****
# global will be used to modify variables outside functions
# another option would be to use a class and subclass Frame

# ***** FUNCTIONS *****
# start, pause, and reset functions will be called when the buttons are clicked
# start function
def start():
    global running
    if not running:
        update()
        running = True

# pause function
def pause():
    global running
    if running:
        # cancel updating of time using after_cancel()
        stopwatch_label.after_cancel(update_time)
        running = False

# reset function
def reset():
    global running
    if running:
        # cancel updating of time using after_cancel()
        stopwatch_label.after_cancel(update_time)
        running = False
    # set variables back to zero
    global hours, minutes, seconds
    hours, minutes, seconds = 0, 0, 0
    # set label back to zero
    stopwatch_label.config(text='00:00:00')


# update stopwatch function
def update():
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
    update_time = stopwatch_label.after(1000, update)

#----------------------------------------------------------------------------------------

# snap window to borders function
def ClickRelease(event):
    resolutionX = window.winfo_screenwidth() # gets the actual screen resolution
    resolutionY = window.winfo_screenheight()
    global x, y
    if window.winfo_y() < 0:  # if the current window position is below 0 , then move the window
        window.geometry("+%s+%s" % (x, 0))
    if window.winfo_y() > (resolutionY-35):
        window.geometry("+%s+%s" % (x,(resolutionY-35)))
    if window.winfo_x() < 0:
        window.geometry("+%s+%s" % (0, y))
    if window.winfo_x() > (resolutionX-140):
        window.geometry("+%s+%s" % ((resolutionX-140), y))

# left click window dragging function
def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    global x, y
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x , y))



def StartWindow():

        global window
        window = Tk(className='Python Examples - Window Color') # window title

        # changes the window default opacity 0 to 1
        win_opacity = 0.8

        # calculate the screen width based on the resolution
        screen_width = window.winfo_screenwidth()
        screen_x= int(screen_width/2)

        window.attributes('-alpha', win_opacity) # window opacity
        window.configure(bg='grey') # window color
        window.overrideredirect(1) # borderless window
        window.attributes('-topmost', True) # keep always on top
        window.geometry(f'{140}x{28}+{screen_x}+{0}') # window size(x) and position (+)

        frame = Frame(window)
        frame.pack() # frame positioning
        frame.config(bg="grey")

        canvas = Canvas(frame,height='25',width='25', bg='grey',highlightthickness=0) # canvas for REC button
        canvas.create_oval(20, 20, 3, 3, fill='red')
        canvas.grid(row=0, column=0)

        label = Label(frame,text="OBS is recording...")
        label.grid(row=0,column=1)
        label.config(bg="grey",fg="white")

        if timer_enable == True:
            global stopwatch_label # modify the stopwatch from gloabal
            stopwatch_label = Label(frame, text='00:00:00', font=('Arial', 20),bg="grey",fg="white" )  # show the clock an pack it
            stopwatch_label.grid(row='1',column= '0',columnspan='2')
            window.geometry(f'{140}x{60}+{screen_x}+{0}')


            start()  #start the timer function

        window.attributes('-alpha', win_opacity)
        window.attributes('-topmost', True)
        window.bind('<ButtonRelease-1>', ClickRelease)

        window.bind('<Button-1>', SaveLastClickPos)  # click to drag and drop window
        window.bind('<B1-Motion>', Dragging)



        window.mainloop()




# ----------------------------   OBS script    ------------------------------------------------------------



class Data:
    OutputDir = None

# this function responds to events inside OBS
def frontend_event_handler(data):
    if data == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        print('REC start')
        StartWindow()

    if data == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        print('REC stops..')
        window.destroy()
        try:              # ingnore the error when the clock stops..
            reset()
        except Exception:
            pass

    if data == obs.OBS_FRONTEND_EVENT_EXIT:
        window.destroy()

def script_update(settings):
    obs.obs_data_set_default_bool(settings, 'timer_bool', True)
    Data.TimerEnable = obs.obs_data_get_bool(settings,"timer_bool")
    global timer_enable
    if Data.TimerEnable == True:
        timer_enable = True
    else:
        timer_enable = False
    print(f'Enable Timer: {timer_enable}')


def script_description():
    return ("OBS RECORDING NOTIFICATION\n\n"
            
            " Installation: \n\n"
            " You have to select a Python 3.6.8 version package "
            " in the configuration that includes TKinter library,"
            " you can find the embedded package and instructions in my github \n\n "
            " github.com/tobsailbot/obs_recording_notification\n\n"
            "ATTENTION:\n\n"
            "Restart OBS after installation")

def script_properties():
    props = obs.obs_properties_create()
    timer_bool = obs.obs_properties_add_bool(props,"timer_bool","Enable Timer")
    return props



obs.obs_frontend_add_event_callback(frontend_event_handler)
