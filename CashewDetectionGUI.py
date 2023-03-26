# import Tkinter module
from threading import Thread
from tkinter import *
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
from CashewDetector import CashewDetector
from DeltaCommand import DeltaCommand
from CameraCalibration import FrameCalibration
import time
import serial

if __name__ == '__main__':
    def update_frame():
        global video, fc, mtx, dist, newcameramtx, roi
        global x_start, y_start, x_end, y_end
        global original_image_canvas, original_photo
        fps = 10
        _, frame = video.read()
        frame = fc.calibrate_frame(frame = frame, mtx=mtx, dist=dist, newcameramtx=newcameramtx, roi=roi)
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        original_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(display_frame))
        original_image_canvas.create_image(0, 0, image = original_photo, anchor=NW)
        detect_cashew(frame=frame)
        window.after(int(1000/fps), update_frame)
    
    def detect_cashew(frame):
        global masked_image_canvas, masked_area_photo, current_centroid_points
        detector = CashewDetector(frame, (x_start, y_start), (x_end, y_end))
        masked_area, current_centroid_points = detector.get_centroid_points()
        masked_area_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(masked_area))
        masked_image_canvas.create_image(0, 0, image = masked_area_photo, anchor=NW)
    
    def send_stop_to_delta_robot():
        command_string = dc.get_stop_conveyor_command()
        print("[+] Sending: " + command_string)
        output_message.insert(END, "[+] Sending: " + command_string + "\n")
        ser.write(command_string.encode())
        line = ser.readline().decode('utf-8').rstrip()
        print("[+] Message from delta - stop: " + line)
        output_message.insert(END, "[+] Message from delta - stop: " + line +"\n")
        
    def send_start_to_delta_robot():
        command_string = dc.get_start_conveyor_command()
        print("[+] Sending: " + command_string)
        output_message.insert(END, "[+] Sending: " + command_string + "\n")
        ser.write(command_string.encode())
        line = ser.readline().decode('utf-8').rstrip()
        print("[+] Message from delta - start: " + line)
        output_message.insert(END, "[+] Message from delta - start: " + line +"\n")

    def send_homing_to_delta_robot():
        command_string = dc.get_homing_command()
        print("[+] Sending: " + command_string)
        output_message.insert(END, "[+] Sending: " + command_string + "\n")
        ser.write(command_string.encode())
        line = ser.readline().decode('utf-8').rstrip()
        print("[+] Message from delta - homing: " + line)
        output_message.insert(END, "[+] Message from delta - homing: " + line +"\n")
    
    def send_centroids_to_delta_robot():
        global dc, ser, current_centroid_points
        if not current_centroid_points:
            print("[+] There isn't any broken cashew in the conveyor!")
            return
        delta_centroid_points = []
        for centroid_point in current_centroid_points:
            x_delta, y_delta = dc.transform_to_delta_points(centroid_point[0], centroid_point[1])
            delta_centroid_points.append((x_delta, y_delta))
        command_string = dc.get_send_centroids_commands(delta_centroid_points)
        print("[+] Sending: " + command_string)
        output_message.insert(END, "[+] Sending: " + command_string + "\n")
        ser.write(command_string.encode())
        line = ser.readline().decode('utf-8').rstrip()
        print("[+] Message from delta - stop: " + line)
        output_message.insert(END, "[+] Message from delta - stop: " + line + "\n")
    
    #Init variables
    window = Tk()
    dc = DeltaCommand()
    fc = FrameCalibration()
    ser = serial.Serial('COM3', 9600, timeout=1)
    ser.reset_input_buffer()
    path_to_calib_file = 'calibration/calibration.yaml'
    
    video = cv2.VideoCapture(0)
    ret, frame = video.read()
    
    mtx, dist, newcameramtx, roi = fc.get_calibrate_parameter(frame, path_to_calib_file)
    frame = fc.calibrate_frame(frame=frame, mtx=mtx, dist=dist, newcameramtx=newcameramtx, roi=roi)
    
    frame_width, frame_height = frame.shape[1], frame.shape[0]
    x_start, y_start, x_end, y_end = 10, 120, 515, 260
    
    #Init for sending data
    last_time_send = time.time() 
    last_time_stop_convoyer = time.time()
    current_centroid_points = []
    
    window.title("Cashew detection for Delta Robot")
    #create title for GUI
    program_title = Label(window, text="Delta Robot Cashew Detection Ver 0.1", 
                             fg="blue", font=("Roboto", 25))
    program_title.grid(row=0, column=0,columnspan=3, sticky=EW, padx=5, pady=5)
    #canvas for original picture
    program_title.grid(row=0, column=0,columnspan=3, sticky=N, padx=5, pady=5)
    original_image_canvas = Canvas(window, width=frame_width, height=frame_height)
    original_image_canvas.grid(row=1, column=0, columnspan=3, sticky=N, padx=5, pady=5)
    # Start point
    start_point_label = Label(window, text="Start point:")
    end_point_label = Label(window, text="End point:")
    start_point_label.grid(row=2, column = 0, sticky = W, pady = 5, padx=5)
    end_point_label.grid(row=3, column= 0, sticky=W, pady=5, padx=5)
    # entry widgets, used to take entry from user
    x_start_entry = Entry(window)
    x_start_entry.grid(row=2, column=0, padx=5)
    x_start_entry.insert(END, x_start)
    
    x_end_entry = Entry(window)
    x_end_entry.grid(row=3, column=0, padx=5)
    x_end_entry.insert(END, x_end)
    
    y_start_entry = Entry(window)
    y_start_entry.grid(row=2, column=1, padx=0)
    y_start_entry.insert(END, y_start)
    
    y_end_entry = Entry(window)
    y_end_entry.grid(row=3, column=1, padx=0)
    y_end_entry.insert(END, y_end)
    
    #mask area
    masked_image_canvas = Canvas(window, height=y_end-y_start, width=x_end-x_start)
    masked_image_canvas.grid(row=1, column=3, columnspan=4, sticky=N, padx=5, pady=5)
    #Buttons settings
    stop_button = Button(window, text ="Stop conveyor", command=send_stop_to_delta_robot, 
                         font=('Roboto', 13), fg='black')
    stop_button.grid(row=2, column=3, sticky=W, padx=5, pady=5)
    start_button = Button(window, text="Start conveyor", command=send_start_to_delta_robot,
                          font=('Roboto', 13), fg='black')
    start_button.grid(row=2, column=4, sticky=W, padx=5, pady=5)
    send_centroid_button = Button(window, text="Send centroids", 
                                  command=send_centroids_to_delta_robot, font=('Roboto', 13), fg='blue')
    send_centroid_button.grid(row=3, column=3, columnspan=2, sticky=W, padx=5, pady=5)
    automatic_button = Button(text="Automatic OFF", font=('Roboto', 13), fg='red')
    automatic_button.grid(row=3, column=4, columnspan=2, sticky=W, padx=5, pady=5)
    homing_button = Button(window, text="Homing", command=send_homing_to_delta_robot,
                          font=('Roboto', 13), fg='black')
    homing_button.grid(row=4, column=3, sticky=W, padx=5, pady=5)
    
    #Output message
    scrollbar=Scrollbar(window, orient='vertical')
    scrollbar.grid(column=6, row=1, sticky=N+S+W)
    output_message = Text(window, width=55, height=17, font=('Roboto', 11), yscrollcommand=scrollbar.set)
    output_message.grid(row=1, column=3, columnspan=2, sticky=SW, padx=5, ipadx=10)

    
    update_frame()
    window.mainloop()

