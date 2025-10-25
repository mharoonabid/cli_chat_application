# 🗨️ Assignment #1 — Basic CLI Chat Application

**Name:** Muhammad Haroon Abid  
**CMS ID:** 501577  
**Class:** BESE15B  
**Course:** EE353 — Computer Networks  

---

## 🧠 Overview

This project is a **Command Line Interface (CLI) Chat Application** developed in **Python** using **sockets** and **threading**.  
It enables multiple clients to connect to a central server and exchange messages in real time — both publicly (broadcast) and privately.

The project consists of three main files:

| File | Description |
|------|--------------|
| `server.py` | Manages client connections, message routing, and overall communication. |
| `client.py` | Handles the client-side interface and interactions with the server. |
| `enums.py` | Defines enums used for message operation types and response types. |

---

## ⚙️ Features

- **Multiple Client Handling** — Server supports multiple simultaneous client connections using threading.  
- **Public & Private Messaging**  
  - Broadcast messages to all users.  
  - Send private messages using `@username`.  
- **User Authentication**  
  - `/new` command to sign up.  
  - `/quit` command to exit the chat.  
  - Credentials (`username` & `password`) stored securely in `credentials.json`.  
- **Active User Tracking** — Maintains a list of currently online users.  
- **Thread-Safe Output** — Ensures proper console output during concurrent operations.  
- **Hidden Password Input** — Uses `getpass` for secure password entry.  
- **Terminal Management** — Uses `os` for clearing the screen between operations.  

---

## 🧩 Message Formats

### 1. Private Message
```json
{
  "op": "PRIVATE",
  "data": {
    "msg": "Hello there!",
    "sender": "Alice",
    "receiver": "Bob"
  }
}
```
### 2. Public (Broadcast) Messages
```json
{
  "op": "PUBLIC",
  "data": {
    "msg": "Hi everyone!",
    "sender": "Alice"
  }
}
```

### 3. Login / Signup Request
```json
{
  "op": "LOGIN" or "SIGNUP",
  "data": {
    "username": "Alice",
    "pssd": "securepassword"
  }
}
```
---

## 🖥️ Server Responses

### 1. Login / Signup Response
```json
{"success": isValid}
```

### 2. General Message Response
```json
{
  "msg": "Welcome to the chat!",
  "type": "INFO"
}
```
---

## 📁 File Descriptions

| File               | Description |
|--------------------|--------------|
| `server.py`        | Handles server-side socket setup, client connections, and message routing. |
| `client.py`        | Handles client-side socket communication, user commands, and message display. |
| `enums.py`         | Contains enums for defining message operation (ReqType) and response types (ResType). |
| `credentials.json` | Stores registered users' credentials. Automatically managed by the application. |

---

## How to Run

### 1. Start the Server
```bash
python server.py
```

### 2. Start a Client (in a new terminal)
```bash
python client.py
```

### 3. Available commands

| Command           | Description                  |
|-------------------|------------------------------|
| `/new`              | Sign up for a new account.   |
| `/quit`             | Quit the chat                |
| `@username message` | Send a private message       |
| `message`         | Send a public message. |

---

## 🧰 Dependencies
- Python 3.x
- Standard Libraries:
  - socket
  - threading
  - json
  - os
  - sys
  - getpass
  - enum

---

## 📜 Notes
- All data is transferred in JSON format for simplicity and structure.

- Ensure the server is running before launching clients.

- Multiple clients can be run from separate terminals or machines on the same network.

---

## ✨ Author

### Muhammad Haroon Abid
### BESE15B — EE353 Computer Networks
### Assignment #1