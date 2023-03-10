class DeltaCommand:
    STOP_CONVEYOR_COMMAND_CODE = 10000
    #TODO: #2 #1 Cần thay đổi cách điều khiển vì nó siêu củ chuối
    SEND_CENTROID_POINTS_COMMAND_CODE = [10001, 10020]
    SEND_FLAGS = {'stop_conveyor':1, 'send_centroids':2}
    INVALID_POINT = -500
    
    def __init__(self)->None:
        pass
    
    def get_stop_conveyor_command(self):
        command = str(self.STOP_CONVEYOR_COMMAND_CODE)+" 0 " + "0"
        return command

    def get_send_centroids_commands(self, delta_centroid_points):
        commands = []
        current_command_code = self.SEND_CENTROID_POINTS_COMMAND_CODE[0]
        for centroid_point in delta_centroid_points:
            if current_command_code < self.SEND_CENTROID_POINTS_COMMAND_CODE[1]:
                command = str(current_command_code) + " " + str(centroid_point[0]) + " " + str(centroid_point[1])
                commands.append(command)
                current_command_code = current_command_code + 1
            else:
                break
        if(current_command_code < self.SEND_CENTROID_POINTS_COMMAND_CODE[1]):
            for i in range(current_command_code, self.SEND_CENTROID_POINTS_COMMAND_CODE[1]):
                command = str(i) + " " + str(self.INVALID_POINT) + " " + str(self.INVALID_POINT)
                commands.append(command)
        return commands
    
    def transform_to_delta_points(self, x, y):
        x_delta = int(x*0.67 - 150)
        y_delta = int(y*0.67 + 133)
        return x_delta, y_delta
    
    def close(self):
        self.ser.close()