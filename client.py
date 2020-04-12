import socket
from sys import argv

is_broadcast = False

if __name__ == '__main__':
    if len(argv) != 2:
        print("Usage: python3 client.py <message>")
        exit(1)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client_socket.settimeout(0.5)
    if is_broadcast:
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.sendto(argv[1].encode(), ('localhost', 5001))

    while True:
        print ('waiting to receive')
        try:
            data, server = client_socket.recvfrom(4096)
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print(f'received {data} from {server}')