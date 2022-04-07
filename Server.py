import threading
from _thread import *
import _thread
import socket
import time
import json

IP = "127.0.0.1"
TIMER = time.time()

def remove_failed_link(node, failure):
    print(f"Node {node.get_id()} failure links")
    print(failure)
    for k,v in node.get_table().items():
        path, link_cost = v
        if k in failure:
            node.get_table()[k] = (path, float('inf'))  # sets to infinity


def calc_cost(node, original_dist, new_dist, from_node, target_node, dir):
    # d(x, y) = min( C(x, v) + d(v, y), d(x, y) )
    # d(B, C) = min( 1 + 2.5, 1)
    # mapp = {}
    # queue[]

        
    #     if child not in mapp or( child in mapp and org.val+dis(org,child)<mapp[child]):
    #         mapp[child][0] = org[0]+child
    #         mapp[child][1] = org[1]+dist(org,child)
    #     queue.append(child)

    # A {"A:" 0, "B": 1, "C": 2.5}
    # B {"B": 0, "A": 1, "C": 1}
    # C {"C": 0, "A": 2.5, "B": 1}

    original_dir, original_link_cost = original_dist

    table = node.get_table()
    neighbour_dist = table[from_node]
    neighbour_dir, neighbour_link_cost = neighbour_dist
    if new_dist + neighbour_link_cost < original_link_cost:
        key = node.get_id() + dir
        val = round(new_dist + neighbour_link_cost, 1)
        # print(f"Node.py: Key is {key}, Val is {val}\n")
        table[target_node] = (key, val)
        # print("Id in table. Updated table: ", end="")
        # print(table[target_node])

        # Link Cost changes
         

        for n in node.get_neighbours(): 
            # print("IM HERE")
            # print(n)
            n_id, n_port = n
            if n_id == from_node:
                # print("IS A NEIGHBOUR")
                # is a neighbour
                if n_id not in node.received:
                    node.received[n_id] = 1
                else: 
                    node.received[n_id] += 1
                node.config = True
                break
        return False
    else:
        return True

def update_table(node, packets):
    
    # B {"A: 2", "C": 1}
    # A {"B": 2, "C": 4}

    # A {"A:" 0, "B": 1, "C": 2.5}
    # B {"B": 0, "A": 1, "C": 1}
    # C {"C": 0, "A": 2.5, "B": 1}

    # print(f'Packets: {packets}')
    # print(len(packets))

    if packets == None:
        print("PACKETS IS NULL")
        return
        

    global TIMER

    from_node = "" 
    converged = True

    for id, link_cost_array in packets.items():
        dir, link_cost = link_cost_array
        # print(dir, link_cost)
        # print('---------------------------')
        if id == node.get_id(): continue  # if id is itself
        if link_cost == float('inf'): continue  # failed link
        if link_cost == 0: 
            from_node = id 
            continue
        # Start bellford algorithm 
        
        # Check if the target node already exists 
        # if not, then just add it to the table
        if id not in node.get_table():
            key = node.get_id() + dir
            val = round(link_cost + node.get_table()[from_node][1], 1)
            
            # print(f"Node.py: Key is {key}, Val is {val}\n")
            node.get_table()[id] = (key, val)
            # print("Id not in table. Updated table: ", end="")
            # print(node.get_table()[id])

            # Link Cost changes

            for n in node.get_neighbours(): 
                # print("IM HERE")
                # print(n)
                n_id, n_port = n
                if n_id == from_node:
                    # print("IS A NEIGHBOUR")
                    # is a neighbour
                    if n_id not in node.received:
                        node.received[n_id] = 1
                    else: 
                        node.received[n_id] += 1
                    node.config = True
                    break 

            continue
        # original distance

        original_dist = node.get_table()[id]
        new_dist = link_cost
        # print(f"original_dist from {node.get_id()} to {id}: {original_dist}")
        # print(f"new_dist from {node.get_id()} to {id}: {new_dist}")
        
        
        is_converge = calc_cost(node, original_dist, new_dist, from_node, id, dir)
        if is_converge == False: converged = False
    
    if converged: node.counter += 1
    if node.counter == len(node.get_neighbours()):
        # converged
        node.updated = True
        node.counter = 0
    
    failure = []
    end_timer = time.time() - TIMER
    if end_timer >= 20:     # 20 seconds threshold for not sending packets
        for n in node.get_neighbours():
            n_id, n_port = n
            if n_id not in node.received: 
                failure += [n_id]
        node.received = {}
        remove_failed_link(node, failure)
        node.config = True
        TIMER = time.time()    # reset timer


    # print('---------------------------')
    # print(node.get_table())
    # {'A': 0, 'B': 1.0, 'C': 2.0}
    # {'B': 0, 'A': 1.0, 'C': 1.0}


    # print("Information packets updated successfully")


def on_new_client(c, addr, node):
    # DEBUG HERE
    
    # socket_address =  c.getsockname()
    try:
        # c.settimeout(10)
        # time.sleep(2)
        # print('Connection from', socket_address)
        # print("Blocked")
        data_rev = c.recv(1024)
        # print("Unblocked")
        # print(data_rev)
        # print(addr)

        # link failure
        if not data_rev:
            print("Server: Didn't get data or connection is closed by Client")
            update_table(node, None)
        
        else:
            # print("Received packets: ",end=" ")
            received_packets = data_rev.decode('utf-8')
            # print(received_packets)

            # update information packets
            packets_in_dict = json.loads(received_packets)
            update_table(node, packets_in_dict)
            # print("Updated information packets\n\n\n")

            # time.sleep(1) # wait one second before relaying messages to client
            # c.sendall(data_rev)     # relay the received packets from other clients to its own client socket
    except Exception as e:
        print(e)
        print("Closing Connection......")

    c.close()
    #print("Connection closed")

class Server():
    def __init__(self, node):
        self.node = node

    def run(self):
        # print(self.args)
        try:
            # print("Server.py")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # print(f"Server port {self.node.get_port()} start...") 
                s.bind((IP, self.node.get_port()))         # Bind to the port
                s.listen(10)            # max 10 queued connections
                while True:
                    c, addr = s.accept()
                    # print()
                    # print(f"New Connection from {addr}\n\n\n")
                    # threading.Thread(target=on_new_client, args=(c, addr)).start()
                    # print(f"Socket name: {c.getsockname()}")
                    _thread.start_new_thread(on_new_client,(c, addr, self.node))
                    # print(f"Server: Number of active threads: {threading.active_count()}")
                s.close()
        except Exception as e:
            print("Server Can't connect to the Socket")
            print(e)


