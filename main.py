from flask import Flask, request, jsonify
from waitress import serve
import socket

app = Flask(__name__)


@app.route('/home', methods=['GET', 'POST'])
def anything():
    print("Done")
    return "Let's do this"


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5001  # initiate port no above 1024

    print(host)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(3)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


server_program()


@app.route('/api')
def nix():
    return 'Wait a minute'


mode = "prod"

if __name__ == '__main__':
    if mode == "dev":
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        serve(app, host='0.0.0.0', port=5001)
