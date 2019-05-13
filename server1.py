from socket import *
from fib import fib

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        resp = fib(n)
        client.send(str(resp).encode('ascii') + b'\n') 
        del client  # 连接终止

fib_server(('',25000))
