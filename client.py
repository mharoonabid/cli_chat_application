# modules
from socket import *
import json


# network configurations
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)


# connecting with server
clientSocket.connect((serverName, serverPort))


# main logic
login_signup = input("enter /new to sign up or just enter to login: ")

for i in range(3,0,-1):

    # sign up
    if login_signup == "/new":
        username = input("enter your username: ")
        pssd = input("enter your password: ")

        req = {
            "op" : 2,
            "data" : {
                "username" : username,
                "pssd" : pssd
            }
        }
    else:
        # login


        # asking for credentials
        username = input("Enter your username: ")
        pssd = input("Enter your password: ")

        # creating the req
        req = {
            "op": 1,
            "data": {
                "username": username,
                "pssd": pssd
            }
        }
    req_json = json.dumps(req)

    # sending the message
    clientSocket.send(req_json.encode())
    res = clientSocket.recv(1024).decode()


    if res == "True" :

        print(f"welcome {username}")
        break

    else:
        if i == 1:
            break
        print(f"Username or Password is incorrect. {i-1} attempts are remaining.")
clientSocket.close()