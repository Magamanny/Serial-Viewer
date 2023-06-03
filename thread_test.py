import time
import threading
start = time.perf_counter()
lock = threading.Lock() 
def do_something(d):
    print("Sleep 1 second...")
    for _ in range(100):
        lock.acquire()
        print('I am')
        time.sleep(0.01)
        print(d)
        print(d)
        print("xxxxxxx")
        lock.release()
    print("----------------")

t1 = threading.Thread(target=do_something, args=('TH-2',))
t2 = threading.Thread(target=do_something, args=('TH-1',))

t1.start()
t2.start()

t1.join()
t2.join()

finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} Second(s)')