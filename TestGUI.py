# import Tkinter module
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from CashewDetection import *
from DeltaCommand import *

window = tk.Tk()
window.title("Delta Robot GUI")

video = cv2.VideoCapture(0)
ret, frame = video.read()
frame_width, frame_height = frame.shape[1], frame.shape[0]
#create canvas
canvas = tk.Canvas(window, width=frame_width, height=frame_height)
canvas.pack()
bw = 0

def update_frame():
    global canvas, photo, bw
    ret, frame = video.read()
    if bw == 0:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if bw == 1:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image = photo, anchor=tk.NW)
    window.after(15, update_frame)

update_frame()
#button

def handle_black_and_white():
    global bw
    bw = 1 - bw

btn = tk.Button(window, text="Black & White", command=handle_black_and_white)
btn.pack()

window.mainloop()
