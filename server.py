# modules
from socket import *
import json, sys, threading


active_users = []
PATH = "credentials.json"


# opening the file
def load_credentials() -> list:
    try:
        with open(PATH, "r") as f:
            credentials = json.load(f)
        return credentials

    except FileNotFoundError:
        sys.exit("Credentials.json not found")
    except json.decoder.JSONDecodeError:
        sys.exit("Credentials.json could not be decoded")



# signup
def signup(username: str, pssd: str) -> bool:
        ls = load_credentials()
        ls.append({"username": username, "pssd": pssd})

        try:
            with open(PATH, "w") as f:
                f.write(json.dumps(ls))

        except FileNotFoundError:
            sys.exit("Credentials.json not found")
        except json.decoder.JSONDecodeError:
            sys.exit("Credentials.json could not be decoded")

        return True


# checking the username and password
def auth(username : str, pssd : str) -> bool:
    for credential in load_credentials():

        if username == credential["username"] and pssd == credential["pssd"]:
            return True
    return False


# main part, handling the requests
def handle_client(connectionSocket, addr):
    print("Connected to ", addr)

    while True:

        # getting request from client
        data = connectionSocket.recv(1024)
        if not data:
            break

        # getting the json data of the req
        req = json.loads(data.decode())


        try:
            if req["op"] in [1,2]: # either log in or sign up

                username = req["data"]["username"]
                pssd = req["data"]["pssd"]

                if req["op"] == 1: # if a user wants to log in
                    isValid = auth(username, pssd)

                else: # if user signs up
                    isValid = signup(username, pssd)

                connectionSocket.send(str(isValid).encode())
                if isValid: # if username and password are correct then added to online users
                    active_users.append([connectionSocket, username])

            elif req["op"] == 3:

                msg = req["data"]["msg"]
                sender = req["data"]["sender"]

                is_quit = (data ==  "/quit")

                if is_quit: # someone left the chat
                    active_users.remove([connectionSocket, sender])
                    res = json.dumps({"msg" : f"{sender} has quit the conversation"}).encode()
                else: # a general message
                    res = json.dumps({"msg" : f"[{sender}] {msg}"}).encode()

                for user in list(active_users): # sending to all online clients
                    if user[0] != connectionSocket:

                        try:
                            user[0].send(res)
                        except Exception as e:
                            active_users.remove(user)

                if is_quit:
                    connectionSocket.close()
                    break


        except BrokenPipeError:
            print("Disconnected to ", addr)
            break
        except ConnectionResetError:
            print("Disconnected to ", addr)
            break
        except ConnectionAbortedError:
            print("Disconnected to ", addr)
            break
    connectionSocket.close()


# starting and configuring server
def start_server():

    # network configurations
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen(5)
    print("The server is ready.")

    # getting requests from multiple clients
    while True:
        connectionSocket, addr = serverSocket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()


if __name__ == "__main__":
    start_server()