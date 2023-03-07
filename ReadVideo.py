# Program To Read video
# and Extract Frames
import cv2
# Function to extract frames
def FrameCapture():
    vidObj = cv2.VideoCapture(1)
    count = 0
    success = 1
    while success:
        success, frame = vidObj.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            cv2.imwrite("data/raw_data/frame_"+str(count)+".png", frame)
            print("Frame saved: " + str(count))
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# Driver Code
if __name__ == '__main__':
    FrameCapture()