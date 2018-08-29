import socket
import sys
import thread
import time
import binascii
import struct

def hex_replace(hex,find_str,replace_str):
    return hex.replace(find_str,replace_str)

def main(setup):
    for settings in parse(setup):
        thread.start_new_thread(server, settings)

    while True:
       time.sleep(60)

def parse(setup):
    settings = list()
    for line in file(setup):
        if line.startswith('#'):
            continue

        parts = line.split()
        settings.append((parts[0], int(parts[1]), parts[2], int(parts[3])))
    return settings

def server(*settings):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, 1)
        dock_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        dock_socket.bind((settings[0], settings[1]))
        dock_socket.listen(1000)
        while True:
            client_socket = dock_socket.accept()[0]
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, 1)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.connect((settings[2], settings[3]))
            thread.start_new_thread(forward, (client_socket, server_socket))
            thread.start_new_thread(forward, (server_socket, client_socket))
    finally:
        thread.start_new_thread(server, settings)

def forward(source, destination):
    string = ' '
    while string:
        string = source.recv(1024)
        if string:
            #print(binascii.b2a_hex(string[0:2]))
            if binascii.b2a_hex(string[0:2]) == "1603":
                #print "in"
                string = hex_replace(binascii.b2a_hex(string),binascii.b2a_hex("www.steam-chat.com"),binascii.b2a_hex("steamcommunity.com")) #domain length = communiyn domain length = 18
                string = binascii.a2b_hex(string)
                #print "replace"
            #print string[0:1].hex()
            destination.sendall(string)
        else:
            source.shutdown(socket.SHUT_RD)
            destination.shutdown(socket.SHUT_WR)

if __name__ == '__main__':
    main('S302.config')
