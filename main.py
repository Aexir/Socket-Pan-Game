# Maciej Dąbkowski WCY19IJ3S1

import server

IP = "127.0.0.1"
PORT = 2137
MAX_CONNECTIONS = 4

if __name__ == '__main__':
    print('Starting new server...')
    new_server = server.Server(IP, PORT, MAX_CONNECTIONS)
    new_server.start()
