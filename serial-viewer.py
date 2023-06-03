import serial
import time
import argparse
import tkinter as tk
import threading # in python std lib
buffA=""
buffB=""
buffC=""
buffX=""
program_end = False
lock = threading.Lock()
def win_insert(d,channel):
    #print(channel," len=",len(buff))
    #print(buff)
    if channel == 'A':
        log1.config(state=tk.NORMAL)
        log1.insert(tk.END, d)
        log1.see(tk.END)
        log1.config(state=tk.DISABLED)
    elif channel=='B':
        log2.config(state=tk.NORMAL)
        log2.insert(tk.END, d)
        log2.see(tk.END)
        log2.config(state=tk.DISABLED)
    elif channel=='C':
        log3.config(state=tk.NORMAL)
        log3.insert(tk.END, d)
        log3.see(tk.END)
        log3.config(state=tk.DISABLED)
    elif channel=='X':
        log4.config(state=tk.NORMAL)
        log4.insert(tk.END, d)
        log4.see(tk.END)
        log4.config(state=tk.DISABLED)

def window_update():
    global buffA
    global buffB
    global buffC
    global buffX
    lock.acquire()
    if len(buffA)>0:
        win_insert(buffA,'A')
        buffA=""
    if len(buffB)>0:
        win_insert(buffB,'B')
        buffB=""
    if len(buffC)>0:
        win_insert(buffC,'C')
        buffC=""
    if len(buffX)>0:
        win_insert(buffX,'X')
        buffX=""
    lock.release()
    pass
    root.after(500,window_update)
def append_to_buffer(d,channel):
    global buffA
    global buffB
    global buffC
    global buffX
    lock.acquire()
    if channel=='A':
        buffA = buffA+d
    if channel=='B':
        buffB = buffB+d
    if channel=='C':
        buffC = buffC+d
    if channel=='X':
        buffX = buffX+d
    lock.release()
def serial_read():
    state=0
    channel = 'X'
    #print("reading")
    while True:
        e = ser.read()
        if program_end:
            print('the end')
            break
        try:
            d = e.decode('utf-8')
        except:
            #state=0
            d='?'
        if d is not '':
            #print(d,state, end=' | ')
            pass
        match state:
            case 0:
                if d == '/':
                    state=5
                pass
            case 5:
                if d == '*':
                    state=10
                elif d=='/':
                    state=10
                else:
                    state=0
                pass
            case 10:
                channel=d
                state=20
                pass
            case 20:
                if d == '*':
                    dp = d
                    state=30
                else:
                    append_to_buffer(d, channel)
                pass
            case 30:
                if d=='/':
                    state=0
                    #buff = buff+"\r\n"
                    #print(buff)
                    #win_insert(buff)
                    #buff=""
                elif d=='*':
                    state=30
                    append_to_buffer(dp, channel)
                else:
                    state=20
                    append_to_buffer(dp + d, channel)
                pass

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help="Time in seconds", type=int, default=10)
    parser.add_argument("-ch", "--channel", help="Serial Sub Channel", type=str, default='A')
    parser.add_argument("-ser", "--serial", help="Serial Main Channel", type=str, default='COM6')
    args = parser.parse_args()
    seconds = args.time
    com_port = args.serial
    com_ch = args.channel
    if len(com_ch)!=1:
        print("Channel can be single character")
        exit()
    seconds_stop= time.time()+1*seconds
    ser = serial.Serial( com_port ,9600,timeout=0.1)
    #-------------------------------------
    # Tk inter config
    import tkinter as tk
    #make a TkInter Window
    root = tk.Tk()
    root.wm_title("Serial-Viewer")

    # make a scrollbar
    scbar1 = tk.Scrollbar(root)
    scbar2 = tk.Scrollbar(root)
    # make a text box to put the serial output
    log1 = tk.Text ( root, width=30, height=30, takefocus=0)
    log2 = tk.Text ( root, width=30, height=30, takefocus=0)
    log3 = tk.Text ( root, width=30, height=30, takefocus=0)
    log4 = tk.Text ( root, width=30, height=30, takefocus=0)
    # Text
    lable1 = tk.Label(text="Channel A")
    lable2 = tk.Label(text="Channel B")
    lable3 = tk.Label(text="Channel C")
    lable4 = tk.Label(text="Channel X")
    # attach text box to scrollbar
    log1.config(yscrollcommand=scbar1.set)
    scbar1.config(command=log1.yview)

    log1.grid(column=0, row=1)   # grid dynamically divides the space in a grid
    log2.grid(column=1, row=1)
    log3.grid(column=2, row=1)
    log4.grid(column=3, row=1)

    lable1.grid(column=0,row=0)
    lable2.grid(column=1,row=0)
    lable3.grid(column=2,row=0)
    lable4.grid(column=3,row=0)
    #scbar1.grid(column=1, row=0)   # and arranges widgets accordingly
    # end of Tk inter
    #-------------------------------------
    print("Start Time since epoch =", time.time())
    t1 = threading.Thread(target=serial_read)
    t1.start()
    root.after(100, window_update)
    root.mainloop()
    program_end=True
    t1.join()
