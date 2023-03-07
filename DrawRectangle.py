# Program To Read video
# and Extract Frames
import cv2
# Function to extract frames
def FrameCapture():
    vidObj = cv2.VideoCapture(1)
    success = 1
    start_point = (0, 100)
    end_point = (640, 356)
    thickness = 1
    color = (0, 255, 0)
    interval = 5
    fps = int(vidObj.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    
    while success:
        success, frame = vidObj.read()
        frame_count = frame_count + 1
        if frame_count % (interval*fps) == 0:
            cv2.imshow('frame', frame)
            path = "data/raw_data/raw_picture_"+str(count)
            cv2.imwrite(path, frame)
            count = count+1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
if __name__ == '__main__':
    FrameCapture()