#PC remote control ESP32 LED light
# 整体流程
# 1. 链接wifi
# 2. 启动网络功能（UDP）
# 3. 接收网络数据
# 4. 处理接收的数据


import socket
import time
import network
import machine


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('dongfeiqiu', 'wangmingdong1225')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())


def start_udp():
    # 2. （UDP）

    # 2.1. create udp socket by writting this socket.SOCK_DGRAM, and if we need to make tcp sockt then we need to write socket.SOCK_STREAM
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2.2. bind the udp connection
    udp_socket.bind(("0.0.0.0", 7788))

    return udp_socket


def main():
    # 1.connect to wifi
    do_connect()
    # 2. start udp connection
    udp_socket = start_udp()
    # 3. control led
    led = machine.Pin(2, machine.Pin.OUT)
    # 4. make the connection with hercules udp connection and control the led by sending the message light on and light off
    while True:
        recv_data, sender_info = udp_socket.recvfrom(1024)
        print("{}发送{}".format(sender_info, recv_data))
        recv_data_str = recv_data.decode("utf-8")
        try:
            print(recv_data_str)
        except Exception as ret:
            print("error:", ret)
        
        # 5. agar command light on aata hai ya light off command aata hai to hume kya karna hai
        if recv_data_str == "light on":
            print("led is on...")
            led.value(1)
        elif recv_data_str == "light off":
            print("led is off...")
            led.value(0)


if __name__ == "__main__":
    main()
