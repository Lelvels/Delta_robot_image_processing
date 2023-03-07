import cv2
import numpy as np
import yaml

def getCbCalibration():
    with open('calibration/calibration.yaml') as f:
        loadeddict = yaml.load(f, Loader=yaml.FullLoader)
    mtx = np.array(loadeddict.get('camera_matrix'))
    dist = np.array(loadeddict.get('dist_coeff'))
    return mtx, dist

if __name__ == '__main__':
    mtx, dist = getCbCalibration()
    print(mtx)
    print(dist)