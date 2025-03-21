import socket
import datetime
import time
import os

SERVER_HOST = '192.168.1.100'
SERVER_PORT = 5000

#File to log alerts

log_filename = f"distance_alert_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def log_event(message):
    with open(log_filename, 'a') as log_file:
        log_file.write(f"{message}\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    try:
        print(f"Connecting to server at {SERVER_HOST}:{SERVER_PORT}....")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server!")
        print(f"Logging events to {log_filename}")
        print("\nPress ctrl+c to exit\n")


        while True:
            data = client_socket.recv(1024).decode('utf-8')


            if not data:
                print("Connection lost. Server may have closed the connection.")
                break


            #displaying le message
            clear_screen()
            print("\n" + "=" * 50)
            print("DISTANCE MONITOR ALERT SYSTEM")
            print("="*50)


            #Check if it's an alert message
            if "ALERT" in data:
                print("\n⚠️ CRITICAL ALERT")
                print(data)
                print("\nObject detected within critical range!")

                #log the alert
                log_event((data))
            else:
                print("\nStatus: Normal")
                print(data)

            print("\n" + "=" *50)
            print(f"Log file: {log_filename}")
    except KeyboardInterrupt:
        print("\nClient shutting dowwwn..")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    main()
