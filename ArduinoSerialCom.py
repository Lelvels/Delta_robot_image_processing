import serial # Module needed for serial communication
import json
import time

def is_json(element) -> bool:
    try:
        json.loads(element)
    except ValueError as e:
        return False
    return True

if __name__ == '__main__':
    ser = serial.Serial('COM3', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        ser.write(b"Hello from rasp\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
