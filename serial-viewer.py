import serial
import time
import argparse
import tkinter as tk

state=0
channel = 'X'
buff=""
def win_insert(d):
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
def serial_read():
    global state
    global channel
    global buff
    #print("reading")
    while True:
        e = ser.read()
        if len(e)==0:
            break
        try:
            d = e.decode('utf-8')
        except:
            state=0
            d=''
            break
        #print(d,end='')
        match state:
            case 0:
                if d == '/':
                    state=5
                pass
            case 5:
                if d == '*':
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
                    buff = buff+d
                pass
            case 30:
                if d=='/':
                    state=0
                    buff = buff+"\r\n"
                    win_insert(buff)
                    buff=""
                else:
                    state=20
                    buff = buff + dp + d
                pass
    root.after(100,serial_read)

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
    ser = serial.Serial( com_port ,9600, timeout=0.01, writeTimeout=0)
    #-------------------------------------
    # Tk inter config
    import tkinter as tk
    #make a TkInter Window
    root = tk.Tk()
    root.wm_title("Reading Serial")

    # make a scrollbar
    scbar1 = tk.Scrollbar(root)
    scbar2 = tk.Scrollbar(root)
    # make a text box to put the serial output
    log1 = tk.Text ( root, width=30, height=30, takefocus=0)
    log2 = tk.Text ( root, width=30, height=30, takefocus=0)
    log3 = tk.Text ( root, width=30, height=30, takefocus=0)
    # attach text box to scrollbar
    log1.config(yscrollcommand=scbar1.set)
    scbar1.config(command=log1.yview)

    log1.grid(column=0, row=0)   # grid dynamically divides the space in a grid
    log2.grid(column=1, row=0)
    log3.grid(column=2, row=0)
    #scbar1.grid(column=1, row=0)   # and arranges widgets accordingly
    # end of Tk inter
    #-------------------------------------
    print("Start Time since epoch =", time.time())
    root.after(500, serial_read)
    root.mainloop()
