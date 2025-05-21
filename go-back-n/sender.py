import socket
import struct
import time
import os

senderIP = "10.0.0.1"
senderPort = 20001
receiverAddressPort = ("10.0.0.2", 20002)
bufferSize = 1024

window_size = 2
timeout = 0.01  

# File to be sent
file_path = "testFile.jpg"

socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.settimeout(timeout)

sequence_number = 0 
base = 0  # Start of the window
unacked_packets = []  
start_time = time.time()  
file_size = os.path.getsize("testFile.jpg")

with open(file_path, "rb") as file:
    packets = []  
    eof_reached = False
    
    while not eof_reached:
        data_chunk = file.read(bufferSize - 3)
        if not data_chunk:
            break  # EOF
        is_last_chunk = len(data_chunk) < (bufferSize - 3)
        file_size += len(data_chunk)
        
        header = struct.pack('!Hb', sequence_number, is_last_chunk)
        packet = header + data_chunk
        packets.append(packet)
        
        # Check if this is the last packet
        if is_last_chunk:
            eof_reached = True
        sequence_number += 1
    
    while base < len(packets):
        while sequence_number < base + window_size and sequence_number < len(packets):
            socket_udp.sendto(packets[sequence_number], receiverAddressPort)
            # print("Sent packet with sequence number:", sequence_number)
            sequence_number += 1
        
        try:
            ack_packet, _ = socket_udp.recvfrom(3)
            ack_seq_num, = struct.unpack('!H', ack_packet[:2])
            # print("Received ACK for sequence number:", ack_seq_num)
            
            if ack_seq_num >= base:
                base = ack_seq_num + 1  # Move the window base
        except socket.timeout:
            # print("Timeout, resending from sequence number:", base)
            sequence_number = base  # Retransmit starting from the base

end_time = time.time()
transfer_time = end_time - start_time
throughput = (file_size / 1024.0) / transfer_time 
print("Average Throughput: {:.2f} KB/s".format(throughput))

socket_udp.close()
