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
# attach text box to scrollbar
log1.config(yscrollcommand=scbar1.set)
scbar1.config(command=log1.yview)

log1.grid(column=0, row=0)   # grid dynamically divides the space in a grid
log2.grid(column=1, row=0)
#scbar1.grid(column=1, row=0)   # and arranges widgets accordingly

count = 0
def readSerial():
    global count
    log1.config(state=tk.NORMAL)
    log1.insert(tk.END, "Count="+str(count)+"\r\n")
    log1.see(tk.END)
    count=count+1
    log1.config(state=tk.DISABLED)
    root.after(100, readSerial) # check serial again soon
# after initializing serial, an arduino may need a bit of time to reset
root.after(100, readSerial)

root.mainloop()