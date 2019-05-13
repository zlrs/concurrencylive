"""
多线程程序，可同时处理多个客户的请求。
由于Global Interpretor Lock, Python进程会Pin在一个CPU核上，也就是说python线程只能在同一个核上. 通过运行多个perf1.py，时间会倍乘，来验证这点。
操作系统给短任务更高的优先级，但是GIL会给强计算任务更高的优先级，短任务会受到强计算任务的巨大影响

"""
from socket import *
from fib import fib
from threading import Thread

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        Thread(target=fib_handler, args=(client,), daemon=True).start()

        
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
