import requests
import PySimpleGUI as sg
import time

"""
This is a simple python I made just for TAG SSR, the sole function of this code is to get traffic data from a web page
"""

#literally does it
def fuckcharachters(inputstring):
    numbers = ["1","2","3","4","5","6","7","8","9","0"]
    if inputstring[0] not in numbers:
        inputstring = inputstring[1:]
        inputstring = fuckcharachters(inputstring)
    else:
        pass
    return inputstring

#parsing returned package into a list, essentially 3 traffic strings are packed into a list
def gettraffic():
    s = requests.session()
    #put username behind email and password behind passwd
    payload = {"email":"!!!!!!","passwd":"!!!!!"}
    response = s.post("http://taggood-2.xyz/auth/login",data=payload)
    r = s.get("http://taggood-2.xyz/user").content
    r = r.decode("utf-8") 
    GB_list = []
    for i in range(len(r)-2):
        if r[i:i+2] == "GB":
            GB_list.append(i)
    #pack 3 strings into a list, get rid of charachters in the process
    outputlist = [fuckcharachters(r[GB_list[0]-6:GB_list[0]]),fuckcharachters(r[GB_list[1]-6:GB_list[1]]),fuckcharachters(r[GB_list[2]-6:GB_list[2]])]
    return outputlist

def time_as_int():
    return int(round(time.time() * 100))

outputlist = gettraffic()

# ----------------  Create Form  ----------------
sg.theme('Black')

layout = [[sg.Text('已用流量: '+outputlist[0]+"GB",key="traf")],
          [sg.Text('共计使用: '+outputlist[1]+"GB",key="traf_total")],
          [sg.Text('今天使用: '+outputlist[2]+"GB",key="traf_today")],
          [sg.Text('', size=(8, 2), font=('Helvetica', 20))],
          [sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]
          
          #display pause and reset,it is here because I borrowed the frame of this code from the internet
          #[sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
          # sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-')]
         #display time
        #[sg.Text('', size=(8, 2), font=('Helvetica', 8), key='text')]
         ]

window = sg.Window('Running Timer', layout,
                   no_titlebar=True,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0))

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

while True:
    # --------- Read and update window --------
    if not paused:
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time
    else:
        event, values = window.read()
    # --------- update data --------
    if (current_time // 100) // 60 >= 5: #update frequency, it is 5 minutes here
        outputlist = gettraffic()
        window['traf'].update('已用流量: '+outputlist[0]+"GB")
        window['traf_total'].update('共计使用: '+outputlist[1]+"GB")
        window['traf_today'].update('今天使用: '+outputlist[2]+"GB")
        paused_time = start_time = time_as_int()
        current_time = 0
    # --------- Do Button Operations --------
    if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
        break
        
#    reset button
#    if event == '-RESET-':
#        paused_time = start_time = time_as_int()
#        current_time = 0

#    elif event == '-RUN-PAUSE-':
#        paused = not paused
#        if paused:
#            paused_time = time_as_int()
#        else:
#            start_time = start_time + time_as_int() - paused_time
        # Change button's text
#        window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')

    # --------- Display timer in window --------
    #window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
    #                                                    (current_time // 100) % 60,
    #                                                    current_time % 100))
window.close()
