# modules
from socket import *
import json, sys, threading


# opening the file
def get_file() -> list:
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
        return credentials

    except FileNotFoundError:
        sys.exit("Credentials.json not found")
    except json.decoder.JSONDecodeError:
        sys.exit("Credentials.json could not be decoded")

# signup

def signup(username: str, pssd: str) -> bool:
        ls = get_file()
        ls.append({"username": username, "pssd": pssd})

        try:
            with open("credentials.json", "w") as f:
                f.write(json.dumps(ls))

        except FileNotFoundError:
            sys.exit("Credentials.json not found")
        except json.decoder.JSONDecodeError:
            sys.exit("Credentials.json could not be decoded")

        return True



# checking the username and password
def checking_credentials(username : str, pssd : str) -> bool:
    for credential in get_file():

        if username == credential["username"] and pssd == credential["pssd"]:
            return True
    return False



def handle_client(connectionSocket, addr):
    print("Connected to ", addr)

    while True:
        data = connectionSocket.recv(1024)
        if not data:
            break

        res = json.loads(data.decode())

        # if a user is login
        if res["op"] == 1:
            isValid = checking_credentials(res["data"]["username"], res["data"]["pssd"])
        # if user signs up
        elif res["op"] == 2:
            isValid = signup(res["data"]["username"], res["data"]["pssd"])

        try:
            connectionSocket.send(str(isValid).encode())
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





# network configurations
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(3)
print("The server is ready.")


while True:
    connectionSocket, addr = serverSocket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,addr))
    client_thread.start()