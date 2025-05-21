import socket
import struct

receiverIP = "10.0.0.2"
receiverPort = 20002
bufferSize = 1024  

file_path = "received.jpg"
expected_sequence_number = 0

socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.bind((receiverIP, receiverPort))

print("UDP socket created successfully.....")

with open(file_path, "wb") as file:
    while True:
        #Extracting info from received packet
        packet, senderAddress = socket_udp.recvfrom(bufferSize) 
        header = packet[:3]
        data_chunk = packet[3:]

        sequence_number, is_last_chunk = struct.unpack('!Hb', header)

        
        if sequence_number == expected_sequence_number:
            # print("Received packet with sequence number:", sequence_number)
            file.write(data_chunk)

            ack_packet = struct.pack('!H', sequence_number)
            socket_udp.sendto(ack_packet, senderAddress)
            # print("Sent ACK for sequence number:", sequence_number)

            # Change (flip) the expected sequence number
            expected_sequence_number = 1 - expected_sequence_number

            if is_last_chunk:
                print("Last packet received. File transfer complete.")
                break
        else:
            # print("Duplicate packet received. Resending ACK for sequence:", 1 - expected_sequence_number)
            ack_packet = struct.pack('!H', 1 - expected_sequence_number)
            socket_udp.sendto(ack_packet, senderAddress)

socket_udp.close()
