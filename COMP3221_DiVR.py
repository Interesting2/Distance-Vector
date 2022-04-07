import sys
import socket
import time
import threading
from Node import Node
from Server import Server
from Client import Client

# network = {
#     # keys from A to J 
#     # empty dictionary as value
#     'A': {},
#     'B': {},
#     'C': {},
#     'D': {},
#     'E': {},
#     'F': {},
#     'G': {},
#     'H': {},
#     'I': {},
#     'J': {}

# }
def build_table(id, port, data):
    node = Node(id, port)
    node.init_table(id, 0.0)      # itself
    for line in data:
        node.add_neighbour(line[0], int(line[2]))
        node.init_table(line[0], float(line[1]))
    return node

def parse_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        num_lines = lines[0].strip('\n')
        # print(num_lines)
        data = []
        for i in range(1, int(num_lines) + 1):
            line = lines[i].strip().split(' ')
            data.append(line)
        # print(data)
        return data

def init_server(node):
    return Server(node)

def init_client(node):
    return Client(node)

def start_program(socket):
    socket.run()

def main(id, port, config):
    # pre-processing
    data = parse_file(config)
    node = build_table(id, port, data)
    print(node)

    # 2 threads each running the server and client
    server = init_server(node)
    threading.Thread(target=start_program, args=(server, )).start()

    client = init_client(node)
    time.sleep(1)
    threading.Thread(target=start_program, args=(client, )).start()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 COMP3221_DiVR.py <node_id> <node_port> <node_config_file>")
        sys.exit(1)
    id, port, config = sys.argv[1], int(sys.argv[2]), sys.argv[3]

    main(id, port, config)
