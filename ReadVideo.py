# Program To Read video
# and Extract Frames
import cv2
import math
from CameraCalibration import FrameCalibration
# Function to extract frames

def transform_to_arduino_points(x, y, offset_origin):
    x_img, y_img = x + offset_origin[0], y + offset_origin[1]

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("My points: ")
        print(x, ' ', y)
        print("Arduino points:")
    if event==cv2.EVENT_RBUTTONDOWN:
        print(x, ' ', y)
    return

def crop_and_save_picture(image, x_start, x_end, y_start, y_end, grid_width, grid_height, index):
    img = image[y_start:y_end, x_start:x_end]
    height, width, _ = img.shape
    cols = int(width/grid_width)
    rows = int(height/grid_height)
    crop_images_idx = 0
    for i in range(rows):
        for j in range(cols):
            # Tính toạ độ của ảnh nhỏ
            y1 = i * grid_height
            y2 = (i + 1) * grid_height
            x1 = j * grid_width
            x2 = (j + 1) * grid_width
            # Cắt vật thể và lưu vào ảnh nhỏ
            small_img = img[y1:y2, x1:x2]
            path = 'D:/Code/MachineLearning/HatDieu/data/all_crop_images/crop_images12/'
            cv2.imwrite(path+"crop_image_" + str(i) + "_" + str(j)
                        + "_" +str(index)+ ".png", small_img)
            crop_images_idx += 1
    print("[+] Saving: " + str(cols*rows) + " images with index: " + str(index))
    return 

def draw_grid(image, x_start, x_end, y_start, y_end, grid_width, grid_height):
    grid_image = image.copy()
    crop_img_width = grid_width
    crop_img_height = grid_height
    color = (0, 255, 0)
    thickness = 1
    cols = int((x_end - x_start)/crop_img_width)
    rows = int((y_end - y_start)/crop_img_height)
    #rectangle
    start_point = (x_start, y_start)
    end_point = (x_end, y_end)
    grid_image = cv2.rectangle(grid_image, start_point, end_point, color, thickness)
    #horizontal
    for idx in range(rows):
        start_point = (x_start, y_start + crop_img_height*idx)
        end_point = (x_end, y_start + crop_img_height*idx)
        grid_image = cv2.line(grid_image, start_point, end_point, color, thickness)
    #vertical
    for idy in range(cols):
        start_point = (x_start + idy*crop_img_width, y_start)
        end_point = (x_start + idy*crop_img_width, y_end)
        grid_image = cv2.line(grid_image, start_point, end_point, color, thickness)
    return grid_image

def FrameCapture():
    vidObj = cv2.VideoCapture(0)
    count = 0
    success = 1
    fc = FrameCalibration()
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    force_fps = 10
    _, frame = vidObj.read()
    image_count = 0
    mtx, dist, newcameramtx, roi = fc.get_calibrate_parameter(frame, 'calibration/calibration.yaml')
    while success:
        success, frame = vidObj.read()
        h,  w = frame.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w,:]
        #Crop for processing area
        x_start, y_start, x_end, y_end = 10, 120, 515, 260
        grid_height, grid_width = 64, 64
        
        dst = dst[y_start:y_end, x_start:x_end,:]
        grid_frame = draw_grid(image=dst, 
                x_start=x_start, x_end=x_end, y_start=y_start, y_end=y_end,
                grid_height=grid_height, grid_width=grid_width)
        
        cv2.imshow('calibresult', grid_frame)
        cv2.setMouseCallback('calibresult', click_event)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('a'):
            cv2.imwrite("data/raw_data/frame_"+str(count)+".png", frame)
            crop_and_save_picture(image=frame, 
                x_start=x_start, x_end=x_end, y_start=y_start, y_end=y_end,
                grid_height=grid_height, grid_width=grid_width, index=image_count)
            image_count = image_count+1
            print("Frame saved: " + str(count))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# Driver Code
if __name__ == '__main__':
    FrameCapture()