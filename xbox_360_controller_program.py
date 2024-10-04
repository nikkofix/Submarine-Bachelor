import pygame
import serial
import time

# Initialize Pygame and the Xbox controller
pygame.init()
pygame.joystick.init()

# Set up the Arduino serial connection
arduino = serial.Serial('/dev/cu.usbmodemDC5475C954042', 9600)  # Replace with your Arduino's port
time.sleep(2)  # Give some time for the connection to establish

# Check if a controller is connected
if pygame.joystick.get_count() == 0:
    print("No controller found!")
    exit()
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller connected: {joystick.get_name()}")

# Function to map joystick input to motor control range (0-255 for PWM)
def map_range(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

try:
    while True:
        pygame.event.pump()  # Update the event queue

        # Read the left analog stick's Y-axis (joystick.get_axis(1))
        left_y = joystick.get_axis(5)  # Y-axis of the left stick

        # Invert Y-axis if needed (many controllers give -1 for up and 1 for down)
        #left_y = -left_y

        # Map joystick input (-1 to 1) to PWM values (0 to 255)
        motor_speed = map_range(left_y, -1, 1, 1500, 1900)

        # Send the motor speed to the Arduino via serial
        arduino.write(f"{motor_speed}\n".encode())

        # Print for debugging
        print(f"Joystick Y: {left_y}, Motor Speed: {motor_speed}")

        # Delay to avoid flooding the serial port
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Program terminated")

finally:
    # Close serial connection and pygame
    arduino.close()
    pygame.quit()
