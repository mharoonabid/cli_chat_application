# modules
import sys, json, threading, os
from socket import *
from typing import Tuple
from getpass import getpass
from enums import *


# network configurations
SERVER_ADDR = '127.0.0.1'
SERVER_PORT = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)


# other configurations
number_incorrect_attempts = 3
stop_event = threading.Event()
print_lock = threading.Lock()


# connecting with server
clientSocket.connect((SERVER_ADDR, SERVER_PORT))


# clear screen
def clear_screen():
    if os.name == 'nt' :
        os.system('cls')
    else:
        os.system('clear')


# to print by blocking other threads
def safe_print(msg: str, msg_type: ResType):
    with print_lock:
        if msg_type == ResType.PRIVATE.name: # for private
            sys.stdout.write(f"\r\033[35m{msg}\033[0m\n> ")
        elif msg_type == ResType.PUBLIC.name: # for broadcasting
            sys.stdout.write(f"\r\033[36m{msg}\033[0m\n> ")
        else: # by server
            sys.stdout.write(f"\r\033[33m{msg}\033[0m\n> ")
        sys.stdout.flush()


# concurrent sending message
def send_messages(username: str):
    while not stop_event.is_set():

        try:
            msg = input("> ").strip()
        except EOFError:
            break

        if not msg:
            continue

        if msg[0] == "@": # for private messages
            req = json.dumps({
                "op" : ReqType.PRIVATE.name,
                "data" : {
                    "msg" : " ".join(msg.split(" ")[1::]),
                    "sender" : username,
                    "receiver" : msg.split(" ")[0][1::]
                }
            })

        else: # for broadcasting
            req = json.dumps({
                "op": ReqType.PUBLIC.name,
                "data": {
                    "msg": msg,
                    "sender": username
                }
            })
        clientSocket.send(req.encode())

        if msg == "/quit": # for quit
            stop_event.set()
            break


# for concurrent receive message
def rec_messages():
    while not stop_event.is_set():
        try:
            data = clientSocket.recv(1024)
            if not data:
                break

            res = json.loads(data.decode())

            safe_print(res["msg"], res["type"])
        except (ConnectionResetError, OSError, json.decoder.JSONDecodeError):
            break
    stop_event.set()

    try:
        clientSocket.shutdown(SHUT_RDWR)
    except OSError:
        pass
    clientSocket.close()


# getting username and password
def user_info() -> Tuple[str, str]:
    username = input("Enter your username: ").strip().replace(" ", "").lower()
    pssd = getpass("Enter your password: ")

    return username, pssd


# either log in or sign up
def login_signup() -> str:
    login_signup_choice = input("Enter /new to sign up or just enter to login: ").rstrip().lower()

    for i in range(number_incorrect_attempts, 0, -1):

        # sign up
        if login_signup_choice == "/new":

            username, pssd = user_info()

            if not username or not pssd:
                print("Empty username or password")
                continue

            req = {
                "op": ReqType.SIGNUP.name,
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
                "op": ReqType.LOGIN.name,
                "data": {
                    "username": username,
                    "pssd": pssd
                }
            }


        # sending the message
        clientSocket.send(json.dumps(req).encode())
        res = json.loads(clientSocket.recv(1024).decode())

        if res["success"]:

            clear_screen()
            print(f"Welcome {username}")

            return username

        else:
            if i == 1:
                clientSocket.close()
                sys.exit()
            print(f"Username or Password is incorrect. {i - 1} attempts are remaining. (repetitive usernames are not allowed while signing up)")
    return ""


# main logic
def start_client():

    username = login_signup()

    send_thread = threading.Thread(target=send_messages, args=(username,))
    rec_thread = threading.Thread(target=rec_messages)

    send_thread.start()
    rec_thread.start()

    send_thread.join()
    stop_event.set()
    rec_thread.join()


if __name__ == "__main__":
    start_client()