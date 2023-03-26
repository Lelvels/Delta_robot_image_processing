class DeltaCommand:
    #TODO: #2 #1 Cần thay đổi cách điều khiển vì nó siêu củ chuối
    STOP_CONVEYOR_COMMAND_CODE = 10000
    START_CONVEYOR_COMMAND_CODE = 10001
    SEND_CENTROID_POINTS_COMMAND_CODE = 10002
    HOMING_COMMAND_CODE = 9999
    SEND_CENTROID_POINTS_REF = [20000, 20010]
    SEND_FLAGS = {'stop_conveyor':1, 'send_centroids':2}
    HOME_POINT = 0
    
    def __init__(self)->None:
        pass
    
    def get_stop_conveyor_command(self):
        command = str(self.STOP_CONVEYOR_COMMAND_CODE)
        return command
    
    def get_start_conveyor_command(self):
        command = str(self.START_CONVEYOR_COMMAND_CODE)
        return command
    
    def get_homing_command(self):
        command = str(self.HOMING_COMMAND_CODE)
        return command

    def get_send_centroids_commands(self, delta_centroid_points):
        command_str = ""
        current_ref = self.SEND_CENTROID_POINTS_REF[0]
        command_str = command_str + str(self.SEND_CENTROID_POINTS_COMMAND_CODE) + " "
        for centroid_point in delta_centroid_points:
            if current_ref < self.SEND_CENTROID_POINTS_REF[1]:
                command = str(current_ref) + " " + str(centroid_point[0]) + " " + str(centroid_point[1])
                command_str = command_str + command + " "
                current_ref = current_ref + 1
            else:
                break
        if(current_ref < self.SEND_CENTROID_POINTS_REF[1]):
            for i in range(current_ref, self.SEND_CENTROID_POINTS_REF[1]):
                command = str(i) + " " + str(self.HOME_POINT) + " " + str(self.HOME_POINT)
                command_str = command_str + command + " "
        return command_str
    
    def transform_to_delta_points(self, x, y):
        x_delta = int(x*(49/65) - 147)
        y_delta = int(y*(49/65) + 129)
        return x_delta, y_delta
    
    def close(self):
        self.ser.close()