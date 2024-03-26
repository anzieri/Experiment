from flask import Flask, request, render_template, jsonify
from waitress import serve
import socket
import threading  # For handling socket communication in a separate thread

app = Flask(__name__, template_folder='templates')
connected_clients = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    data = request.form['data']
    # Process or store the data as needed (optional)
    return render_template('index.html', submitted_data=data)


@app.route('/receive', methods=['GET', 'POST'])
def run_server():
    host = '0.0.0.0'  # Replace with your server's IP address
    port = 10000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(3)

    print(f"Server listening on {host}:{port}")

    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        # Start a separate thread to handle each client connection
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()


# def handle_client(conn):
#     username = conn.recv(1024).decode()  # Receive username from client
#     connected_clients[conn] = username  # Store connection and username
#     print(f"Client connected: {username}")
#
#     while True:
#         data = conn.recv(1024).decode()
#         if not data:
#             break
#
#         # Extract recipient username and message
#         recipient, message = data.split(':', 1)
#
#         # Check if recipient is online
#         if recipient in connected_clients:
#             recipient_conn = [c for c, u in connected_clients.items() if u == recipient][0]
#             try:
#                 recipient_conn.send(f"{username}: {message}".encode())
#             except ConnectionAbortedError:
#                 print(f"Client {recipient} disconnected")
#                 del connected_clients[recipient_conn]  # Remove disconnected client
#         else:
#             conn.send(f"Recipient '{recipient}' not found".encode())
#
#     conn.close()
#     del connected_clients[conn]  # Remove disconnected client
#     print(f"Client disconnected: {username}")


def handle_client(conn):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))

        # Process or store the received data here (optional)

        # Send a response back to the client
        response = f"Server received: {data}"
        conn.send(response.encode())

    conn.close()


mode = 'dev'
if __name__ == '__main__':
    if mode == "dev":
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        serve(app, host='0.0.0.0', port=5001)
