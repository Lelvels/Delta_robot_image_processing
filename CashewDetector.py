import cv2
import numpy as np
import yaml

class CashewDetector:
    def __init__(self, image, start_point, end_point):
        if not (isinstance(image, (np.ndarray))):
            raise ValueError("Expect frame to be a numpy array, got {image} instead!")
        self.image = image
        self.start_point = start_point
        self.end_point = end_point
    
    def draw_grid(self, grid_width, grid_height, color = (0, 255, 0), thickness=1):
        grid_image = self.image.copy()
        x_start, y_start, x_end, y_end = self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1]
        crop_img_width = grid_width
        crop_img_height = grid_height
        cols = int((x_end - x_start)/crop_img_width)
        rows = int((y_end - y_start)/crop_img_height)
        grid_image = cv2.rectangle(grid_image, self.start_point, self.end_point, color, thickness)
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

    def find_contour_areas(self, contours):
        areas = []
        for cnt in contours:
            cont_area = cv2.contourArea(cnt)
            areas.append(cont_area)
        return areas
    
    def get_centroid_points(self):
        #Getting just masked region
        x_start, y_start, x_end, y_end = self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1]
        masked_region = self.image[y_start:y_end, x_start:x_end, :]
        
        gray_img = cv2.cvtColor(masked_region, cv2.COLOR_BGR2YCR_CB)
        _, blackAndWhiteImage = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
        _, threshold = cv2.threshold(blackAndWhiteImage[:, :, [1]], 200, 450, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        result_contour = []
        rectangles = []
        centroid_points = []
        if not contours:      
            return masked_region, centroid_points
        
        sorted_contours_area = sorted(contours, key = cv2.contourArea, reverse=True)
        sorted_areas = self.find_contour_areas(sorted_contours_area)
        max_none_cashew_size = int(sorted_areas[0]*0.7)
        for sc in sorted_contours_area:
            area = cv2.contourArea(sc)
            if (area < max_none_cashew_size) and area > 80:
                result_contour.append(sc)
        for cnt in result_contour:
            (x, y, w, h) = cv2.boundingRect(cnt) 
            rectangles.append((x, y, w, h))
        for rectangle in rectangles:
            (x, y, w, h) = rectangle
            cv2.rectangle(masked_region, (x, y), (x + w, y + h), (255, 0, 0), 2)
            x_c, y_c = int((2*x + w)/2), int((2*y+h)/2)
            centroid_points.append((x_c, y_c))
            cv2.line(masked_region, (x_c, y_c), (x_c+1, y_c+1), (255, 0, 0), 5)
        return masked_region, centroid_points