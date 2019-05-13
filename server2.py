"""
单线程程序，同时只能处理一个客户的请求。
同时只与最多一台客户建立连接，与该客户维持着连接时，其它客户只能进入backlog，等待目前的这位用户处理完并挂断连接。
"""
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
        fib_handler(client)
        
def fib_handler(client):
    try:
        while True:
            req = client.recv(100)
            if not req:
                break
            n = int(req)
            resp = fib(n)
            client.send(str(resp).encode('ascii') + b'\n') 
    except ConnectionError as e:  # 客户主动挂断
        print(e)
        print("Connection Closed(by client)!")
    

fib_server(('',25000))
