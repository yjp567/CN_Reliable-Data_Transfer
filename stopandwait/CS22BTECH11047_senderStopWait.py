import socket
import struct
import time
import os

senderIP = "10.0.0.1"
senderPort = 20001
receiverAddressPort = ("10.0.0.2", 20002)
bufferSize = 1024  

file_path = "testFile.jpg"   # File to be sent

sequence_number = 0  
timeout = 0.1  # Timeout for retransmission (in seconds)

socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.settimeout(timeout)

start_time = time.time()  # For throughput calculation
file_size = os.path.getsize("testFile.jpg")  # total file size (in bytes) 
retransmissions = 0  # Counter for retransmissions

with open(file_path, "rb") as file:
    while True:
        data_chunk = file.read(bufferSize - 3)
        if not data_chunk:
            break  # EOF

        is_last_chunk = len(data_chunk) < (bufferSize - 3)
        header = struct.pack('!Hb', sequence_number, is_last_chunk)
        packet = header + data_chunk

        ack_received = False
        while not ack_received:
            socket_udp.sendto(packet, receiverAddressPort)  # Sending the packet
            # print("Sent packet with sequence number:", sequence_number)

            ack_start_time = time.time()
            while time.time() - ack_start_time < timeout:
                socket_udp.settimeout(timeout - (time.time() - ack_start_time))
                try:
                    ack_packet, _ = socket_udp.recvfrom(3)
                    ack_seq_num, = struct.unpack('!H', ack_packet[:2])

                    if ack_seq_num == sequence_number:
                        # print("Received ACK for sequence number:", sequence_number)
                        ack_received = True
                        sequence_number = 1 - sequence_number  # Change sequence number
                        break
                except socket.timeout:
                    retransmissions += 1
                    # print("Timeout, resending packet with sequence number:", sequence_number)
                    break  # Timeout reached, resend the packet

end_time = time.time()
transfer_time = end_time - start_time
throughput = (file_size / 1024.0) / transfer_time  
print("Average Throughput: {:.2f} KB/s".format(throughput))
print("Total Retransmissions:", retransmissions)

socket_udp.close()
