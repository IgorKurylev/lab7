import socket
from select import select
import fcntl
import struct

ifname = "wlp2s0".encode()


def get_ip_address(ifname: bytes) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


server_ip = get_ip_address(ifname)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_ip, 5001))
server_socket.listen()

to_monitor = []


def accept_connection(server_socket: socket.socket):
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} is established")

        to_monitor.append(client_socket)


def send_message(client_socket: socket.socket):
    request = client_socket.recv(4096)

    if request:
        print(request.decode())
        response = f"Hello from {server_ip}!\n".encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        try:
            ready_to_read, _, _ = select(to_monitor, [], [])

            for sock in ready_to_read:
                if sock is server_socket:
                    accept_connection(sock)
                else:
                    send_message(sock)
        except ValueError:
            print("One of client connections is crashed!")
            to_monitor[:] = [server_socket]


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
