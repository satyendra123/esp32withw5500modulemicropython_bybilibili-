from machine import Pin, SPI
import time

from wiznet5k import WIZNET5K
import wiznet5k_socket as socket
import sma_esp32_w5500_requests as requests

spi = SPI(2)
cs = Pin(5, Pin.OUT)
rst = Pin(34)
nic = WIZNET5K(spi, cs, rst)

print("Chip Version:", nic.chip)
print("MAC Address:", [hex(i) for i in nic.mac_address])
print("My IP address is:", nic.pretty_ip(nic.ip_address))

# TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest_addr = ('192.168.1.50', 6000)

try:
    tcp_socket.connect(dest_addr)  # Connect to the remote server
    print("Connected to", dest_addr)

    for i in range(10):
        send_data = "hello world..%d" % i
        tcp_socket.send(send_data.encode('utf-8'))
        time.sleep(1)

    tcp_socket.close()
    print("Socket closed")

except Exception as e:
    print("Error:", e)