# modules
import sys
import json
import threading
from socket import *
from typing import Tuple
from getpass import getpass


# network configurations
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)


# other configurations
number_incorrect_attempts = 3
stop_event = threading.Event()


# connecting with server
clientSocket.connect((serverName, serverPort))





def send_messages(username: str):
    while not stop_event.is_set():
        msg = input("> ")

        req = json.dumps({
            "op" : 3,
            "data" : {
                "msg" : msg,
                "sender" : username
            }
        })
        clientSocket.send(req.encode())

        if msg == "/quit":
            stop_event.set()
            clientSocket.shutdown(SHUT_RDWR)
            clientSocket.close()

def rec_messages():
    while not stop_event.is_set():
        data = clientSocket.recv(1024)
        if not data:
            break

        res = json.loads(data.decode())

        print(res["msg"])


def user_info() -> Tuple[str, str]:
    username = input("Enter your username: ").strip().replace(" ", "")
    pssd = getpass("Enter your password: ")

    return username, pssd




# main logic
def start_client():
    login_signup = input("Enter /new to sign up or just enter to login: ")

    for i in range(number_incorrect_attempts, 0, -1):

        # sign up
        if login_signup == "/new":

            username, pssd = user_info()

            req = {
                "op": 2,
                "data": {
                    "username": username,
                    "pssd": pssd
                }
            }
        else:
            # login

            # asking for credentials
            username, pssd = user_info()

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

        if res == "True":

            print(f"welcome {username}")

            break

        else:
            if i == 1:
                clientSocket.close()
                sys.exit()
            print(f"Username or Password is incorrect. {i - 1} attempts are remaining.")

    send_thread = threading.Thread(target=send_messages, args=(username,))
    rec_thread = threading.Thread(target=rec_messages)

    send_thread.start()
    rec_thread.start()

    send_thread.join()
    stop_event.set()
    rec_thread.join()


if __name__ == "__main__":
    start_client()