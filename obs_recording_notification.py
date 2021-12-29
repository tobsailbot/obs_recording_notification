
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

def ClickRelease(event):
    resolutionX = window.winfo_screenwidth()
    resolutionY = window.winfo_screenheight()
    global x, y
    if window.winfo_y() < 0:
        window.geometry("+%s+%s" % (x, 0))
    if window.winfo_y() > (resolutionY-35):
        window.geometry("+%s+%s" % (x,(resolutionY-35)))
    if window.winfo_x() < 0:
        window.geometry("+%s+%s" % (0, y))
    if window.winfo_x() > (resolutionX-140):
        window.geometry("+%s+%s" % ((resolutionX-140), y))


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
        window.geometry(f'{140}x{35}+{screen_x}+{0}') # window size(x) and position (+)

        frame = Frame(window)
        frame.pack()
        frame.pack(side=RIGHT)   # frame positioning
        frame.config(width=10,height=25,bg="grey")

        canvas = Canvas(width=10, height=25, bg='grey',highlightthickness=0) # canvas for REC button
        canvas.create_oval(25, 25, 10, 10, fill='red')
        canvas.pack(expand=YES, fill=BOTH)

        label = Label(frame,text="OBS is recording...")
        label.pack(ipady=6,pady=1)
        label.config(bg="grey",fg="white")

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

    if data == obs.OBS_FRONTEND_EVENT_EXIT:
        window.destroy()



def script_description():
    return ("OBS RECORDING NOTIFICATION\n\n"
            "How it works:\n\n"
            "When the 'Start recording' button is pressed,\n"
            "a popup window appears on top of the screen "
            " showing you that OBS is recording.."
            " Installation: \n\n"
            " You have to configure Python by selecting"
            " the folder with version 3.6.8 that includes"
            " the necessary libraries,"
            " you can find the embedded package and instructions in my github \n\n "
            " github.com/tobsailbot/obs_recording_notification\n\n"
            "ATTENTION:\n\n"
            "Restart OBS after installation")



obs.obs_frontend_add_event_callback(frontend_event_handler)










