import socket
# import fcntl
# import struct

# ifname = "wlp2s0".encode()
#
#
# def get_ip_address(ifname: bytes) -> str:
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     return socket.inet_ntoa(fcntl.ioctl(
#         s.fileno(),
#         0x8915,  # SIOCGIFADDR
#         struct.pack('256s', ifname[:15])
#     )[20:24])
#
#
# server_ip = get_ip_address(ifname)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server_socket.bind(('localhost', 5001))

def receive_message(server_socket: socket.socket):
    request, addr = server_socket.recvfrom(4096)

    if request:
        print(addr, " : ", request.decode())
        print('sending acknowledgement to', addr)
        server_socket.sendto('answer!!'.encode(), addr)
    else:
        server_socket.close()


if __name__ == '__main__':
    print(server_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF))
    while True:
        receive_message(server_socket)
