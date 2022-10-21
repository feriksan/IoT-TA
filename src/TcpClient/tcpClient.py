import socket
import pickle

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(('192.168.56.1',5000))

def sendData(x, y, z):
    # datas = str(x/100)
    # datas = [(x/10)-27, ",",  (y/10)-26, ",", ((z*37.79527559*0.01))]
    datas = x, ",", y, ",", z
    dict = "".join([str(i) for i in datas])
    # print(dict)
    clientSocket.send(dict.encode())