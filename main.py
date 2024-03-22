from flask import Flask, request
import socket

app = Flask(__name__)

# Store active connections
active_connections = []

@app.route('/send', methods=['POST'])
def send_message():
    data = request.form.get('message')
    if data:
        for conn in active_connections:
            conn.send(data.encode())
        return "Message sent to all clients."
    else:
        return "No message provided."

def handle_client(conn):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received from client: {data}")
        # You can process the data here or send it to other clients
        # For now, we'll just echo it back to the sender
        conn.send(data.encode())
    conn.close()

@app.route('/connect', methods=['POST'])
def connect_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((get_server_ip(), port))
    active_connections.append(client_socket)
    return "Connected to server."

def get_server_ip():
    return socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    host = get_server_ip()
    port = 5001
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, address = server_socket.accept()
        print(f"Connection from: {address}")
        active_connections.append(conn)
        handle_client(conn)
