import customtkinter
import webbrowser
from PIL import Image
import time
from main import get_network_stats, check_connection
from commands.bedtime import computer_sleep
from commands.shutdown import shutdown_machine
from sys import platform
import threading

#internet speed var (if your current speed is less than this value then application will start the countdown)
global INTERNET_SPEED
INTERNET_SPEED = 200 #200kb/s

#check connection status
global internet_status
internet_status = check_connection()


#checks if app is on (by default it is ON)
global is_on
is_on = True

#initialzing download speed variable in order for it to be accessible from other places of code
global download_speed 
download_speed = get_network_stats() 

#initial starting point for timer to count down from (in seconds)
global INITIAL_TIME
INITIAL_TIME = 60
global initial_time
initial_time = INITIAL_TIME

#whether the machine turns off or just goes to sleep
global user_option
# selected to turn off the computer because it's the default option
user_option = "Turn Off The Computer"

customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("dark-blue")

app = customtkinter.CTk()
app.title("Steam Auto ShutDown")
app.geometry("700x500")

def callback(url):
    webbrowser.open_new(url)

def schedule_check_connection():
    global internet_status, is_on

    while True:
        internet_status = check_connection()
       
        if internet_status:
            is_on = True
            internet_connection_warning.pack_forget()
        else:
            is_on = False
            internet_connection_warning.pack(pady=10)

        time.sleep(5)  # Check every 5 seconds

def update_speed_label():
    global download_speed

    while True:
        download_speed = get_network_stats()
        speed_label.configure(text=f"Current Download Speed: {download_speed}KB/S")
        time.sleep(1)  # Update every 1 second

#gives user an option what to do when download finished
def optionmenu_callback(choice):
    global user_option

    user_option = choice
    optionmenu.set(choice)

def switch_event():
    global is_on

    state = switch_var.get()

    if state == "on":
        is_on = True
        switch.configure(text = "Turned On")
    else:
        is_on = False
        switch.configure(text = "Turned Off")

def timer():
    global initial_time, user_option, download_speed

    while True:
        if initial_time > 0 and download_speed < INTERNET_SPEED and is_on and internet_status:
            timer_label.pack(pady = 50)
            initial_time -=1
            timer_label.configure(text = f"{user_option} in {initial_time} seconds", font=("Arial", 20))
        elif initial_time == 0 and download_speed < INTERNET_SPEED and is_on and internet_status:
            if user_option == "Go To Sleep":
                computer_sleep()
                app.destroy()
            else:
                shutdown_machine(platform)
        else:
            #resetings timer in order to use it later
            initial_time = INITIAL_TIME
            timer_label.pack_forget()

        time.sleep(1)
    #app.after(2000,timer)

#internet connection warning
internet_connection_warning = customtkinter.CTkLabel(app, text = "CHECK INTERNET CONNECTION", text_color = "red")


#is on or is off app
switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(app, text = "Turn On", command = switch_event,
                                variable = switch_var, onvalue = "on", offvalue = "off")
switch.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
switch.pack(pady = 40)

#speed label
speed_label = customtkinter.CTkLabel(master=app, text=f"Current Download Speed:{get_network_stats()}KB/S")
speed_label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
speed_label.pack(pady=10)

#Giving user an option
optionmenu = customtkinter.CTkOptionMenu(app, values=["Turn Off The Computer", "Go To Sleep"],
                                         command=optionmenu_callback)
optionmenu.pack(pady=50)

#hyperlink to repo
#link1 is github repo
link1 = customtkinter.CTkLabel(app, text="GitHub Repo", cursor = "heart")
link1.pack(pady=(50,0))
link1.bind("<Button-1>", lambda e: callback("https://github.com/808thlife/SteamAutoShutdown"))


#timer label before some_event happens
timer_label = customtkinter.CTkLabel(app, text=f"Time Remaining: {initial_time} seconds", font=("Arial", 20))

# Create threads for background tasks
check_connection_thread = threading.Thread(target=schedule_check_connection)
update_speed_thread = threading.Thread(target=update_speed_label)
timer_thread = threading.Thread(target=timer)

# Start the threads
check_connection_thread.start()
update_speed_thread.start()
timer_thread.start()

app.mainloop()