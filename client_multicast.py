import socket
import struct
import sys

message = 'HELLO!'
multicast_group = ('224.3.29.71', 5001)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.settimeout(0.5)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:

    # Send data to the multicast group
    print(f'sending  {message}')
    sent = sock.sendto(message.encode(), multicast_group)

    while True:
        print ('waiting to receive')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print(f'received {data} from {server}')

finally:
    print('closing socket')
    sock.close()