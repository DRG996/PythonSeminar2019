import socket
from _thread import *
import pickle
from game import Game

server = "5.179.9.196"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetGueassing()
                    elif data != "getPoints":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    gameId = (idCount - 1)//3
    if idCount % 3 == 1:
        games[gameId] = Game(gameId)
        p = 0
        print("Creating a new game...")
    elif idCount % 3 == 2:
        p = 1
    else:
        games[gameId].gameReady = True
        p = 2

    start_new_thread(threaded_client, (conn, p, gameId))
