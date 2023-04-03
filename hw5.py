import socket

HOST, PORT = '', 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()

print(f'Serving HTTP on port {PORT}...')

while True:
    client_connection, client_address = s.accept()

    request_data = client_connection.recv(1024)
    request_lines = request_data.decode('utf-8').split('\r\n')
    request_uri = request_lines[0].split()[1]

    try:
        with open('.' + request_uri, 'rb') as f:
            response_data = f.read()
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    except FileNotFoundError:
        response_data = b'<html><body><h1>File Not Found</h1></body></html>'
        response_headers = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'

    response = response_headers.encode('utf-8') + response_data
    client_connection.sendall(response)

    client_connection.close()
