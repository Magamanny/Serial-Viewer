import serial
import time
import argparse
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
    print("Start Time since epoch =", time.time())
    state = 0
    with serial.Serial( com_port ,9600) as ser:
        while 1:
            e = ser.read()
            try:
                d = e.decode('utf-8')
            except:
                state=0
                d==''
            #print(d,state)
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
                    if d == com_ch:
                        state=20
                    else:
                        state=0
                    pass
                case 20:
                    if d == '*':
                        dp = d
                        state=30
                    else:
                        print(d,end='')
                    pass
                case 30:
                    if d=='/':
                        state=0
                        print()
                    else:
                        print(dp+d,end='')
                    pass
            if time.time() > seconds_stop:
                print("Stop time since epoch =", time.time())	
                break
