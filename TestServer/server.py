import socket
import threading
import json

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))

BOOKS = [{'BookId': 1, 'Name': 'Тонкое Искуство'},
{'BookId': 2, 'Name': 'Исповедь Чудовеща'},
{'BookId': 3, 'Name': 'Хочу і буду'},
{'BookId': 4, 'Name': 'Сила нтроверта'},
{'BookId': 2, 'Name': 'Исповедь Чудовеща'},
{'BookId': 3, 'Name': 'Хочу і буду'},
{'BookId': 4, 'Name': 'Сила нтроверта'},
{'BookId': 2, 'Name': 'Исповедь Чудовеща'},
{'BookId': 3, 'Name': 'Хочу і буду'},
{'BookId': 3, 'Name': 'Хочу і буду'},
{'BookId': 4, 'Name': 'Сила нтроверта'}]

BOOKS2 = [{'BookId': 1, 'Name': 'Тонкое Искуство'},
{'BookId': 2, 'Name': 'Исповедь Чудовеща'},
{'BookId': 3, 'Name': 'Хочу і буду'},
{'BookId': 4, 'Name': 'Сила нтроверта'},
{'BookId': 2, 'Name': 'Ілюша зробив уроки'}]

JANRES = [{'GenreId': 1, 'Name': 'Детектив'},
{'GenreId': 2, 'Name': 'Фэнтези'},
{'GenreId': 3, 'Name': 'Фантастика'},
{'GenreId': 4, 'Name': 'Стихи'},
{'GenreId': 5, 'Name': 'Проза'},
{'GenreId': 6, 'Name': 'Ужасы'},
{'GenreId': 7, 'Name': 'Приключенчиские романы'}]

def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode()
    print('Received {}'.format(request))
    response = ''
    if "ALL" in request:
        response = json.dumps(BOOKS)
    elif "LOGIN" in request:
        response = json.dumps({"Result": True})
    elif "GETGENRES" in request:
        response = json.dumps(JANRES)
        print(response)
    else:
        response = json.dumps(BOOKS2)
    client_socket.send((response + "EndQuery").encode())
    client_socket.close()
    print("heee")

while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
