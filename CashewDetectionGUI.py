# import Tkinter module
from tkinter import *
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
from CashewDetection import *
from DeltaCommand import *

if __name__ == '__main__':
    def update_frame():
        global original_image_canvas, photo
        _, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        original_image_canvas.create_image(0, 0, image = photo, anchor=NW)
        window.after(15, update_frame)
    
    def update_masked_area():
        global x_start, y_start, x_end, y_end
        global x_start_entry, x_end_entry, y_start_entry, y_end_entry
        x_start, y_start = int(x_start_entry.get()), int(y_start_entry.get())
        x_end, y_end = int(x_end_entry.get()), int(y_end_entry.get())
        print("[+] Change masked area: ")
        print(x_start, y_start, x_end, y_end)
    
    #Starting main area
    window = Tk()
    # # configure the grid
    # window.columnconfigure(0, weight=1)
    # window.columnconfigure(1, weight=3)
    video = cv2.VideoCapture(0)
    ret, frame = video.read()
    frame_width, frame_height = frame.shape[1], frame.shape[0]
    x_start, y_start, x_end, y_end = 0, 210, 640, 338
    window.title("Cashew detection for Delta Robot")
    #create title for GUI
    program_title = Label(window, text="Delta Robot Cashew Detection Ver 0.1", 
                             fg="blue", font=("Roboto", 25))
    program_title.grid(row=0, column=0,columnspan=6, sticky=N, padx=5, pady=5)
    #canvas for original picture
    program_title.grid(row=0, column=0,columnspan=3, sticky=N, padx=5, pady=5)
    original_image_canvas = Canvas(window, width=frame_width, height=frame_height)
    original_image_canvas.grid(row=1, column=0, columnspan=3, sticky=N, padx=5, pady=5)
    update_frame()
    
    # Start point
    start_point_label = Label(window, text="Start point:")
    end_point_label = Label(window, text="End point:")
    start_point_label.grid(row=2, column = 0, sticky = W, pady = 5, padx=5)
    end_point_label.grid(row=3, column= 0, sticky=W, pady=5, padx=5)
    # entry widgets, used to take entry from user
    x_start_entry = Entry(window)
    x_start_entry.grid(row=2, column=0, padx=5)
    x_start_entry.insert(0, x_start)
    x_end_entry = Entry(window)
    x_end_entry.grid(row=3, column=0, padx=5)
    x_end_entry.insert(0, x_end)
    y_start_entry = Entry(window)
    y_start_entry.grid(row=2, column=1, padx=0)
    y_start_entry.insert(0, y_start)
    y_end_entry = Entry(window)
    y_end_entry.grid(row=3, column=1, padx=0)
    y_end_entry.insert(0, y_end)
    # submit button
    submit_button = Button(window, text="Enter value for masked area", command=update_masked_area)
    submit_button.grid(row=2, column=3, sticky=W, padx=5, pady=5)
    #mask area
    window.mainloop()

