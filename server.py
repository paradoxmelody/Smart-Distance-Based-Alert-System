import RPi.GPIO as GPIO

import time
import socket
import threading

import datetime
#tcp since it's reliable
#GPIO SETUP

GPIO.setmode(GPIO.BCM)
TRIG_PIN = 23
ECHO_PIN = 24
CRITICAL_DISTANCE = 50 #IN CENTIMETRES OOH(CM)

#PINS SETUP EX

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIG_PIN, False)

#SERVER SETTINGS FOR TCP
HOST = '0.0.0.0'
PORT = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server started on {HOST}:{PORT}")
clients = []

#measurrinf the distance
def measure_distance():
    # sending 10us pulse for triggering
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    #save start time
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
        #avoiding infinite loop so we add timeout
        if time.time() - stop_time > 0.5:
            return -1


    #saving arrival time
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()
        if stop_time - start_time > 0.5:
            return -1



    #distance calculation
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2 #porque the speed of sound is app 34300 cm/s

    return round(distance, 2)

#HANDLE CLIENT connections
def handle_client(client_socket, client_address):
    print(f"Connected to client: {client_address}")

    try:
        while True:
            distance = measure_distance()
            timestamp = determine.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if distance < 0:
                message = f"{timestamp} | Error measuring distance"
            elif distance < CRITICAL_DISTANCE:
                message = f"{timestamp} | ALERT: Object detected at {distance} cm (critical distance)"
            else:
                message = f"{timestamp} | Distance: {distance} cm"

            print(message)
            client_socket.send(message.encode('utf-8'))
            time.sleep(1)


    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        print(f"Connection closed with {client_address}")

"""
THIS IS THE MAIN 
LOOP TO ACCEPT CONNECTIONS
"""

try:
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client(), args=(client_socket, client_address))
        client_thread.daemon = True
        client_thread.start()

except KeyboardInterrupt:
    print("Server shutting dooooowwwn ....")
finally:
    # clean up
    for client in clients:
        client.close()
    server_socket.close()
    GPIO.cleanup()
    print("Server shut down and GPIO cleaned up")












