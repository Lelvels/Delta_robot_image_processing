# Program To Read video
# and Extract Frames
import cv2
# Function to extract frames

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
    if event==cv2.EVENT_RBUTTONDOWN:
        print(x, ' ', y)
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
    # #vertical
    for idy in range(cols):
        start_point = (x_start + idy*crop_img_width, y_start)
        end_point = (x_start + idy*crop_img_width, y_end)
        grid_image = cv2.line(grid_image, start_point, end_point, color, thickness)
    return grid_image

def FrameCapture():
    vidObj = cv2.VideoCapture(0)
    count = 0
    success = 1
    while success:
        success, frame = vidObj.read()
        x_start, x_end, y_start, y_end = 0, 640, 130, 258
        grid_height, grid_width = 64, 64
        grid_frame = draw_grid(image=frame, 
                x_start=x_start, x_end=x_end, y_start=y_start, y_end=y_end,
                grid_height=grid_height, grid_width=grid_width)
        cv2.imshow('frame', grid_frame)
        cv2.setMouseCallback('frame', click_event)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('a'):
            cv2.imwrite("data/raw_data/frame_"+str(count)+".png", frame)
            print("Frame saved: " + str(count))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# Driver Code
if __name__ == '__main__':
    FrameCapture()