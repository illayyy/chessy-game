import socket
import threading
import random
import sqlite3
import hashlib

PORT = 59920


def register(client, what):
    # connection confirmation message
    client.send("ok".encode())

    # listening loop, wait to receive request from client
    while True:
        msg = client.recv(1024).decode()
        req = msg.split("|")

        # request is a login request
        if req[2] == "login":
            if login(req[0], req[1]):
                # login successful, send confirmation and break listening loop
                client.send("1".encode())
                break
            else:
                # login unsuccessful, send error message
                client.send("0".encode())

        # request is a signup request
        else:
            if signup(req[0], req[1]):
                # signup successful, send confirmation message
                client.send("1".encode())
            else:
                # signup unsuccessful, send error message
                client.send("0".encode())


def login(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username='" + username + "'")
    f = c.fetchall()
    if len(f) != 1 or f[0][1] != hashlib.sha256(password.encode()).hexdigest():
        return False
    return True


def signup(username, password):
    # establish connection with database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # execute sql command to find if the selected username already exists
    c.execute("SELECT * FROM users WHERE username='" + username + "'")

    if len(c.fetchall()) != 0:
        # a match has been found, signup unsuccessful
        return False
    else:
        # no matches found
        # hash password
        password = hashlib.sha256(password.encode()).hexdigest()
        # execute sql command to insert the new user's information to the database
        c.execute("INSERT INTO users VALUES ('" + username + "','" + password + "')")

        # apply changes to db, signup successful
        conn.commit()
        return True


# once two clients have been found, a game will begin
def game(client1, client2):
    # randomly selects which client goes first (white)
    # red player to go will always be referred to as "client1"
    if random.randint(0, 1) == 1:
        client1, client2 = client2, client1
    client1.send("white".encode())
    client2.send("black".encode())

    # receive usernames from clients
    name1 = client1.recv(1024)
    name2 = client2.recv(1024)

    # send each client their opponent's username
    client1.send(name2)
    client2.send(name1)

    # receive confirmation
    client1.recv(1024)
    client2.recv(1024)

    # send the white player a message to begin playing, and begin the game loop
    client1.send("play".encode())

    while True:
        # white's turn :
        move = ""
        # tell black to wait
        client2.send("wait".encode())
        while True:
            move = client1.recv(1024)
            if move:
                # white has sent a move, send black and break out of the listening loop
                client2.send(move)
                print("CLIENT 1 PLAYED", move.decode())
                break
        # if the move resulted in game over, break out of the game loop entirely and close the thread
        if move == "resign" or move[-4:] == "MATE":
            break

        # black's turn :
        move = ""
        # tell white to wait
        client1.send("wait".encode())
        while True:
            move = client2.recv(1024)
            if move:
                # black has sent a move, send white and break out of the listening loop
                client1.send(move)
                print("CLIENT 2 PLAYED", move.decode())
                break
        # if the move resulted in game over, break out of the game loop entirely and close the thread
        if move == "resign" or move[-4:] == "MATE":
            break


def main():
    # socket setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen()

    # thread variables
    main_thread = []
    last_client = None

    # look for clients
    while True:
        client_socket, client_address = server_socket.accept()
        msg = client_socket.recv(1024)
        if msg.decode() == "connect":
            print("CLIENT CONNECTED")
            client_socket.send("name".encode())

            msg = client_socket.recv(1024).decode()
            print("CLIENT NAMED : ", msg)
            client_socket.send("connected".encode())
            # add client to thread
            if last_client:
                t = threading.Thread(target=game, args=(last_client, client_socket))
                main_thread.append(t)
                t.start()
                last_client = None
            else:
                last_client = client_socket
        elif msg.decode() == "db":
            t = threading.Thread(target=register, args=(client_socket, ""))
            main_thread.append(t)
            t.start()
            last_client = None


if __name__ == "__main__":
    main()
