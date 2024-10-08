import tkinter as tk

def on_button_nogi_click(frame):
    frame.tkraise()
    button_n.config(bg='red')
    button_h.config(bg=original_color)
    button_s.config(bg=original_color) 
def on_button_hinata_click(frame):
    frame.tkraise()
    button_n.config(bg=original_color)
    button_h.config(bg='red')
    button_s.config(bg=original_color) 
def on_button_sakura_click(frame):
    frame.tkraise()
    button_n.config(bg=original_color)
    button_h.config(bg=original_color)
    button_s.config(bg='red') 

# create main window
root = tk.Tk()
root.title("Sakamichi member's blog")

#get the width,height of computer's screen
#so that window can show at its center
window_width = 1200
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 40 #minus the height(40 or 75) of taskbar below the screen
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
#set W,H of the window
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

#create three frames for 3 groups
frame_n = tk.Frame(root)
frame_h = tk.Frame(root)
frame_s = tk.Frame(root)

for frame in (frame_n, frame_h, frame_s):
    frame.grid(row=0, column=0, sticky='nsew')
    # frame.pack(fill='both', expand=True)

# add something on each frame
tk.Label(frame_n, text='this is nogi blog!').pack()
tk.Label(frame_h, text='this is hinata blog!').pack()
tk.Label(frame_s, text='this is sakura blog!').pack()


# create 3 buttons
button_n = tk.Button(root, text="nogi", command=lambda: on_button_nogi_click(frame_n))
button_h = tk.Button(root, text="hinata", command=lambda: on_button_hinata_click(frame_h))
button_s = tk.Button(root, text="sakura", command=lambda: on_button_sakura_click(frame_s))
button_n.grid(row=0, column=100)
button_h.grid(row=0, column=200)
button_s.grid(row=0, column=300)
original_color = button_n.cget('bg')
# print(original_color)

#show nogi by default
frame_n.tkraise()

# run the app
root.mainloop()
