import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('', 5001)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:

    data, address = sock.recvfrom(1024)
    
    print(f'received {len(data)} bytes from {address}')
    print(data)

    print('sending acknowledgement to', address)
    sock.sendto('answer!!'.encode(), address)