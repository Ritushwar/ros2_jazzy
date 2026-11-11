#!/usr/bin/env python3
import socket
import struct

# UDP Configuration
UDP_IP = "0.0.0.0"
UDP_PORT = 8000

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

try:
    while True:

        # Receive binary UDP packet
        data, address = sock.recvfrom(1024)
        if len(data) != 12:
            print(f"Invalid packet size: {len(data)} bytes")
            continue

        # Unpack three signed 32-bit integers
        value_x, value_y, value_z = struct.unpack('<iii', data)

        # Display received values
        print(
            f"X: {value_x:4d} | "
            f"Y: {value_y:4d} | "
            f"Z: {value_z:2d}"
        )

except KeyboardInterrupt:
    print("\nReceiver stopped.")
    
finally:
    sock.close()