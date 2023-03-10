import cv2
import numpy as np
import time
import serial
from CashewDetector import CashewDetector
from DeltaCommand import DeltaCommand

if __name__ == '__main__':
    frame = cv2.imread("data/raw_data/frame_330.png")
    cv2.imshow('frame', frame)
    x_start, x_end, y_start, y_end = 0, 640, 210, 338
    grid_height, grid_width = 64, 64
    start_point, end_point = (x_start, y_start), (x_end, y_end)
    detector = CashewDetector(frame, start_point, end_point)
    dc = DeltaCommand()
    #Show ảnh grid
    grid_frame = detector.draw_grid(
        grid_height=grid_height, grid_width=grid_width)
    cv2.imshow("Grid frame", grid_frame)
    #Tìm centroids trong hình
    black_img, centroid_points = detector.get_centroid_points()
    cv2.imshow("Black image", black_img)
    print("Original centroid points:")
    print(centroid_points)
    print("Delta centroid points:")
    delta_centroid_points = []
    for centroid_point in centroid_points:
        x_delta, y_delta = dc.transform_to_delta_points(centroid_point[0], centroid_point[1])
        delta_centroid_points.append((x_delta, y_delta))
    print(delta_centroid_points)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
    #Gửi về delta
    ser = serial.Serial('COM3', 9600, timeout=1)
    ser.reset_input_buffer()
    send_flag = dc.SEND_FLAGS['stop_conveyor']
    while True:
        if send_flag == dc.SEND_FLAGS['stop_conveyor']:
            command = dc.get_stop_conveyor_command()                                                                                                                                                                                                       
            print("[+] Sending: " + command)    
            ser.write(command.encode())
            time.sleep(2)
            send_flag = dc.SEND_FLAGS['send_centroids']
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
        elif send_flag == dc.SEND_FLAGS['send_centroids']:
            commands = dc.get_send_centroids_commands(delta_centroid_points)
            for com in commands:
                command = command + com + " "
            print("[+] Sending: " + command) 
            ser.write(command.encode())
            time.sleep(2)
            send_flag = dc.SEND_FLAGS['stop_conveyor']
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
    