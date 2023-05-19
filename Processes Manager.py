from tkinter.messagebox import showinfo
from tkinter import *
import subprocess
from datetime import date, datetime

mainProcesses = []

def getMainProcesses(showSys):
    global mainProcesses

    if showSys:
        cmd = 'powershell "Get-Process | Format-Table Id, StartTime, CPU, Name, mainWindowtitle -AutoSize'
    else:
        cmd = 'powershell "Get-Process | where {$_.MainWindowTitle} | Format-Table Id, StartTime, CPU, Name, mainWindowtitle -AutoSize'

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    mainProcesses = []
    titleString = ""

    skipper = 0

    for line in proc.stdout:
        if skipper < 3:
            skipper += 1
            continue
        if line.rstrip():
            lineData = line.decode().rstrip()
            lineData = lineData.split()
            try:
                for i in range(6, len(lineData)):
                    titleString += lineData[i]
                mainProcesses.append({"Id":lineData[0]
                                    , "Start Date": lineData[1]
                                    , "Start Time": lineData[2]+lineData[3] 
                                    , "CPU": str(round(float(lineData[4]),2))
                                    , "Name": lineData[5]
                                    , "Title":titleString})
                titleString = ""
            except:
                continue

    return mainProcesses

def KillProcessByID(id, showSys):
    global mainProcesses

    startTime = ""
    startDate = ""
    for i in mainProcesses:
        if id in i.values():
            startTime = i["Start Time"]
            startDate = i["Start Date"]
            break
    cmd = 'powershell "taskkill /F /PID ' + str(id)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout != b'':
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
        open_popup(stdout)
        open_popup("\nProcess started at " +  startTime + " " + startDate + "\nProcess ended at " + dt_string)
    if stderr != b'':
        open_popup(stderr)

    Start(showSys)
    return

def KillProcessByName(name, showSys):
    global mainProcesses

    startTime = ""
    startDate = ""
    for i in mainProcesses:
        if name in i.values():
            startTime = i["Start Time"]
            startDate = i["Start Date"]
            break

    cmd = 'powershell "taskkill /IM ' + str(name) +'.exe /F'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout != b'':
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
        open_popup(stdout)
        open_popup("\nProcess started at " +  startTime + " " + startDate + "\nProcess ended at " + dt_string)
    if stderr != b'':
        open_popup(stderr)
    
    Start(showSys)
    return

def CreateProcess(fullPath, showSys):
    cmd = 'powershell "Start-Process ' + str(fullPath)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout != b'':
        open_popup(stdout)
    if stderr != b'':
        open_popup(stderr)

    Start(showSys)
    return

window = Tk()

window.title("Processes Management APP")

widthWindow = 1190
heightWindow = 680
window.geometry(str(widthWindow)+"x"+str(heightWindow))

frame = Frame(window)
frame.pack(side="top", expand=True, fill="both")
frame.configure(bg="#29827a")

def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()

def open_popup(textData):
   showinfo("info", textData)

def Start(showSys):

    processes = getMainProcesses(showSys)

    #### text to put all processes in ####
    text = Text(frame, height=16, width=150, font=("Arial Bold", 13), bg = "#29827a", fg = "white")
    text.place(x = 0, y = 0)

    scrollbar = Scrollbar(text, orient='vertical', command=text.yview)

    text['yscrollcommand'] = scrollbar.set

    for i in range(len(processes)):
        position = f'{i}.0'
        text.insert(position
                    , " "
                    + processes[i]["Id"] 
                    + "\t" 
                    + processes[i]["Start Date"] 
                    + "\t    " 
                    + processes[i]["Start Time"]
                    + "\t\t" 
                    + processes[i]["CPU"]
                    + "\t"
                    + processes[i]["Name"]
                    + "\t\t\t\t"
                    + processes[i]["Title"]
                    +"\n")

    text.insert(0.0, " ====================================================================================================================== \n")
    text.insert(0.0, "  ID\tStartDate\t   StartTime\t\tCPU\tName\t\t\t\tTitle \n")
    text.insert(0.0, " ====================================================================================================================== \n")
    ######################################

    #### kill process by id ####
    sentence = Label(frame, text="Enter process ID to kill", font=("Arial Bold", 12), bg="#29827a", fg="white")
    sentence.place(x=80, y=320)

    entry1 = Entry(frame, fg="black", font=("Arial Bold", 11)) 
    entry1.place(x=85, y=360)

    button_border = Frame(frame, highlightbackground = "black", bg = "black", highlightthickness = 0, bd=2)
    button_border.place(x=140, y=400)
    KillID = Button(button_border, text="Kill ID", bg="#d2bf4a", fg="white", font=("Arial Bold", 10), command = lambda:KillProcessByID(entry1.get(), showSys))
    KillID.pack()   
    ############################# 

    #### kill process by name ####
    sentence2 = Label(frame, text="Enter process Name to kill", font=("Arial Bold", 12), bg="#29827a", fg="white")
    sentence2.place(x=80, y=450)

    entry2 = Entry(frame, fg="black", font=("Arial Bold", 11)) 
    entry2.place(x=85, y=490)

    button_border2 = Frame(frame, highlightbackground = "black", bg = "black", highlightthickness = 0, bd=2)
    button_border2.place(x=130, y=530)
    KillName = Button(button_border2, text="Kill Name", bg="#d2bf4a", fg="white", font=("Arial Bold", 10), command = lambda:KillProcessByName(entry2.get(), showSys))
    KillName.pack()   
    ############################# 

    #### Create process by path or name if it's system process ####
    sentence3 = Label(frame, text="Enter process Path to create \nor process name if it's system's", font=("Arial Bold", 12), bg="#29827a", fg="white")
    sentence3.place(x=780, y=370)

    entry3 = Entry(frame, fg="black", font=("Arial Bold", 11)) 
    entry3.place(x=820, y=430)

    button_border3 = Frame(frame, highlightbackground = "black", bg = "black", highlightthickness = 0, bd=2)
    button_border3.place(x=850, y=470)
    CreateProcessB = Button(button_border3, text="Create Process", bg="#d2bf4a", fg="white", font=("Arial Bold", 10), command = lambda:CreateProcess(entry3.get(), showSys))
    CreateProcessB.pack()   
    ############################# 
    
    # Refresh button
    button_border4 = Frame(frame, highlightbackground = "black", bg = "black", highlightthickness = 0, bd=2)
    button_border4.place(x=widthWindow/2-80, y=370)
    Refresh = Button(button_border4, text="Refresh", bg="#d2bf4a", fg="white", font=("Arial Bold", 10), command = lambda:Start(showSys))
    Refresh.pack() 

    # Show system processes button
    button_border5 = Frame(frame, highlightbackground = "black", bg = "black", highlightthickness = 0, bd=2)
    button_border5.place(x=widthWindow/2-130, y=420)
    ShowSysB = Button(button_border5, text="Show System Processes", bg="#d2bf4a", fg="white", font=("Arial Bold", 10), command = lambda:Start(True))
    ShowSysB.pack() 

    # Show main processes button
    button_border6 = Frame(frame, highlightbackground = "black", bg = "black", highlightthickness = 0, bd=2)
    button_border6.place(x=widthWindow/2-120, y=470)
    ShowMainB = Button(button_border6, text="Show Main Processes", bg="#d2bf4a", fg="white", font=("Arial Bold", 10), command = lambda:Start(False))
    ShowMainB.pack() 

Start(False)

window.mainloop()

