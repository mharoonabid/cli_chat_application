# modules
from socket import *
from enums import *
import json, sys, threading


# network configurations
serverPort = 12000
serverName = "127.0.0.1"
NUMBER_CONNECTIONS = 5


# other configurations
active_users = []
PATH = "credentials.json"
file_lock = threading.Lock()
active_lock = threading.Lock()


# opening the file
def load_credentials() -> list:
    try:
        with file_lock:
            with open(PATH, "r") as f:
                credentials = json.load(f)
        return credentials

    except FileNotFoundError:
        sys.exit(f"{PATH} not found")
    except json.decoder.JSONDecodeError:
        sys.exit(f"{PATH} could not be decoded")


# signup
def signup(username: str, pssd: str) -> bool:
        users = load_credentials()

        for user in users: # checking redundant usernames
            if user["username"] == username:
                return False
        users.append({"username": username, "pssd": pssd})

        try:
            with file_lock:
                with open(PATH, "w") as f: # updating the file
                    f.write(json.dumps(users))

        except FileNotFoundError:
            sys.exit(f"{PATH} not found")
        except json.decoder.JSONDecodeError:
            sys.exit(f"{PATH} could not be decoded")

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
            if req["op"] in [ReqType.LOGIN.name, ReqType.SIGNUP.name]: # either log in or sign up

                username = req["data"]["username"]
                pssd = req["data"]["pssd"]

                if req["op"] == ReqType.LOGIN.name: # if a user wants to log in
                    isValid = auth(username, pssd)

                else: # if user signs up
                    isValid = signup(username, pssd)

                connectionSocket.send(json.dumps({"success": isValid}).encode())
                if isValid: # if username and password are correct then added to online users
                    for user in active_users:
                        user[0].send(json.dumps({"msg" : f"\r[server] {username} has joined the conversation.", "type" : ResType.SERVER.name}).encode())

                    with active_lock:
                        active_users.append([connectionSocket, username])

            elif req["op"] == ReqType.PUBLIC.name:

                msg = req["data"]["msg"]
                sender = req["data"]["sender"]

                is_quit = (msg ==  "/quit")

                if is_quit: # someone left the chat
                    with active_lock:
                        active_users[:] = [u for u in active_users if u[0] != connectionSocket]
                    res = json.dumps({"msg" : f"\r[server] {sender} has quit the conversation", "type": ResType.SERVER.name}).encode()
                else: # a general message
                    res = json.dumps({"msg" : f"\r[{sender}] {msg}", "type" : ResType.PUBLIC.name}).encode()

                for user in list(active_users): # sending to all online clients

                    try:
                        if user[0] != connectionSocket:
                            user[0].send(res)
                    except Exception as e:

                        with active_lock:
                            active_users.remove(user)
                        print("Disconnected from ", addr)

                if is_quit:
                    connectionSocket.close()
                    break

            elif req["op"] == ReqType.PRIVATE.name: # private message
                msg = req["data"]["msg"]
                sender = req["data"]["sender"]
                receiver = req["data"]["receiver"]

                for user in list(active_users):
                    if user[1] == receiver:
                        res = json.dumps({"msg" : f"\r[Private: {sender}] {msg}", "type" : ResType.PRIVATE.name}).encode()
                        user[0].send(res)
                        break
                else:
                    connectionSocket.send(json.dumps({"msg": f"[server] {receiver} is not online.", "type" : ResType.SERVER.name}).encode())


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

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverName, serverPort))
    serverSocket.listen(NUMBER_CONNECTIONS)
    print("The server is ready.")

    # getting requests from multiple clients
    while True:

        connectionSocket, addr = serverSocket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()


if __name__ == "__main__":
    start_server()