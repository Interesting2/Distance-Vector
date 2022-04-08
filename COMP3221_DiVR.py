import sys
import socket
import time
import threading
from Node import Node
from Server import Server
from Client import Client

def build_table(id, port, data):
    node = Node(id, port)

    neighbours = {}
    for line in data:
        node.add_node_timer(line[0])    # initialize a timer for each neighbour node
        node.add_neighbour(line[0], int(line[2]))
        neighbours[line[0]] = float(line[1])

    # init routing table
    table = {
        'A': ('', 0.0), 
        'B': ('', 0.0), 
        'C': ('', 0.0), 
        'D': ('', 0.0), 
        'E': ('', 0.0), 
        'F': ('', 0.0), 
        'G': ('', 0.0), 
        'H': ('', 0.0), 
        'I': ('', 0.0), 
        'J': ('', 0.0)
    }
    for k in table:
        if k == id: table[k] = (k, 0.0); continue
        if k in neighbours:
            table[k] = (id, neighbours[k])
        else:
            table[k] = ('', float('inf'))       # currently unknown nodes set to infinity
    node.init_table(table)
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
    # test = {
    #        'A': {'A': ('', 0),
    #             'B': ('', 1.0),
    #             'C': (2, 1.0)
    #         },
    #         'B': {'B': ('', 0),
    #             'A': ('', 1.0),
    #             'C': ('', 1.0)
    #         },
    #         'C': {'C': ('', 0),
    #             'B': ('', 1.0),
    #             'A': ('', 1.0)
    #         }
    # } 


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
