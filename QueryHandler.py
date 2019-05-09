import socket
import json

class QueryHandler(object):
    __ip_address = '77.47.208.43'
    __port = 9050
    __end_of_query = 'EndQuery'

    def __init__(self, ip, port):
        self.__ip_address = ip
        self.__port = port

    def send_request(self, query_type, args):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.__ip_address, self.__port))
        message = self.build_query(query_type, args)
        client.sendall((message).encode())
        response = ""
        while(self.__end_of_query not in response):
            response += client.recv(4096).decode()
        response = response.replace(self.__end_of_query, ' ').strip()
        #print(response)
        data = json.loads(response)
        return data
        '''for product in data:
            print(type(product))
            print()
        print(data)'''

    def build_query(self, query_type, args):
        quantity_of_spaces = 15 - len(query_type)
        query_type = query_type + ' ' * quantity_of_spaces
        return query_type + json.dumps(args) + self.__end_of_query
