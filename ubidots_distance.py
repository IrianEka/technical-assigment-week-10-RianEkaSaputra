import time
import requests

# Replace with your Ubidots API Key and Variable ID
API_KEY = "BBFF-itYMZyU3lk1QUEZX4KRlub6v9s5aIN"
VARIABLE_ID = "BBFF-058d5e9909a272b657b1e0643bd645988f7"

# Define the GPIO pins for the HC-SR04 sensor
TRIG_PIN = 17
ECHO_PIN = 27

def measure_distance():
    # Import necessary libraries
    import RPi.GPIO as GPIO

    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    # Send a pulse to the trigger pin
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Measure the time it takes for the pulse to return
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate distance in centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in air (343 m/s) divided by 2
    distance = round(distance, 2)

    # Clean up GPIO
    GPIO.cleanup()

    return distance

def send_to_ubidots(value):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/device1/?token={API_KEY}"
    payload = {"distance": value}
    response = requests.post(url, json=payload)
    return response

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance} cm")
        
        response = send_to_ubidots(distance)
        print("Data sent to Ubidots:", response.status_code)

        time.sleep(1)  # Send data every 1 seconds

except KeyboardInterrupt:
    print("Measurement stopped by user")
