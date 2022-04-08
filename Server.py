import threading
from _thread import *
import _thread
import socket
import time
import json

IP = "127.0.0.1"

def remove_failed_link(node, id):
    node.get_table()[id] = ('failed', float('inf'))


def bellman_ford(node, neighbours_id):
    # for all nodes in the the routing table
    # recalculate the shortest path to all those nodes

    link_cost_changed = False
    routing_table, neighbours = node.get_table(), node.get_neighbours()

    for n in routing_table:
        if n == node.get_id(): continue
        if routing_table[n][0] == 'failed': continue    # if link failure, skip


        # calculate the shortest path to node n using the following formula
        # min(cost of node.get_id() to its neighbour node plus the distance of the neighbour node to the target node, d(x, y))
        for neighbour in neighbours:
            if neighbour[0] == n: continue      # if neighbour is equal to the target node
            if not node.in_reach(neighbour[0]): continue
            dir, cost_to_neighbour = routing_table[neighbour[0]]        # cost of node going to its neighbour

            neighbour_routing_table = node.get_reachability(neighbour[0])   # routing table of the neighbour
            dir_from_neighbour_to_target, cost_from_neighbour_to_target = neighbour_routing_table[n]    # cost of neighbour going to target node

            if cost_from_neighbour_to_target == float('inf'): 
                continue
            
            new_cost = cost_to_neighbour + cost_from_neighbour_to_target
            original_cost = routing_table[n][1]

            if new_cost < original_cost:
                key = dir + dir_from_neighbour_to_target
                val = round(new_cost, 1)
                routing_table[n] = (key, val)
                if n in neighbours_id: node.config = True
                link_cost_changed = True
    
    if link_cost_changed: 
        node.triggered = True # send packets to its neighbours if link costs to a particular code has changed

    node.counter += 1
    if node.counter >= len(neighbours_id) - 1:
        # check when network is converged
        node.updated = True
        node.counter = 0

        
def recalculate_links(node, failed_node):
    table = node.get_table()
    for k,v in table.items():
        if k == node.get_id(): continue
        if k == failed_node: continue
        path, link_cost = v

        # if the id of the failed node is in the current shortest path to a target node, reset the path and link cost 
        if failed_node in path:
            table[k] = ('' , float('inf'))


def update_table(node, packets):
    
    if packets == None:
        print("PACKETS IS NULL")
        return

    from_node = "" 

    for id, link_cost_array in packets.items():
        if link_cost_array[1] == 0:
            from_node = id

    node.add_reach_table(from_node, packets)        # add to reachability matrix

    neighbours_id = []  # keep track of neighbour ids
    for n in node.get_neighbours(): 
        # print("IM HERE")
        # print(n)
        n_id, n_port = n
        neighbours_id.append(n_id)


    for id, link_cost_array in packets.items():
        dir, link_cost = link_cost_array

        if id == node.get_id(): continue

        if dir == 'failed': 
            # failed link
            remove_failed_link(node, id)
            recalculate_links(node, id)

        else:
            # if link cost is infinity, then set infinity to the new cost immediately
            if node.get_table()[id][1] == float('inf'):
                key = node.get_id() + dir
                val = round(link_cost + node.get_table()[from_node][1], 1)
                
                node.get_table()[id] = (key, val)

                # if the updated node is a neighbour, then we modify the config file
                if id in neighbours_id: node.config = True      # update the config file if the link cost to its neighbour changed
                node.triggered = True
            
    
    # Start bellman ford algorithm 
    bellman_ford(node, neighbours_id)  

    node.add_node_timer(from_node)   # reset from_node's timer

    # check if neighbours are alive
    for n_timer in node.timer:
        time_of_node = node.get_node_timer(n_timer)
        end_timer = time.time() - time_of_node
        if end_timer >= 30:     # 30 seconds threshold for not sending packets
            if node.get_table()[n_timer][1] != float('inf'):
                print(end_timer)
                remove_failed_link(node, n_timer)
                recalculate_links(node, n_timer)
                bellman_ford(node, neighbours_id)  
                node.config = True
                node.triggered = True
                node.timer[n_timer] = time.time()     # reset timer



def on_new_client(c, addr, node):
    try:
        data_rev = c.recv(1024)

        if not data_rev:
            print("Server: Didn't get data or connection is closed by Client")
            update_table(node, None)
        
        else:
            received_packets = data_rev.decode('utf-8')

            # update information packets
            packets_in_dict = json.loads(received_packets)
            update_table(node, packets_in_dict)

    except Exception as e:
        print(e)
        print(str(e.__class__.__name__))
        print("Closing Connection......")

    c.close()


class Server():
    def __init__(self, node):
        self.node = node

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((IP, self.node.get_port()))         # Bind to the port
                s.listen(10)            # max 10 queued connections
                while True:
                    c, addr = s.accept()
                    _thread.start_new_thread(on_new_client,(c, addr, self.node))
                s.close()
        except Exception as e:
            print("Server Can't connect to the Socket")
            print(e)


