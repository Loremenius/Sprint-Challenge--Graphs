from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
def choose_direction(room):
    if room['s'] == '?':
        return 's'
    elif room['w'] == '?':
        return 'w'
    elif room['e'] == '?':
        return 'e'
    elif room['n'] == '?':
        return 'n'
    else:
        return None

def opposite_direction(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'

def bfs_unknown_path(locations):
    start_node = {
        'cardinal_path': [],
        'id_path': [player.current_room.id]
    }
    q = Queue()
    q.enqueue(start_node)
    visted = {}
    while q.size() > 0:
        node = q.dequeue() 
        current_room_id = node['id_path'][-1]
        current_room = locations[current_room_id]
        if current_room_id not in visted:
            for direction in current_room:
                if current_room[direction] == '?':
                    return node['cardinal_path']
            visted[current_room_id] = 'Visited'
            for direction in current_room:
                if current_room[direction] is not None:
                    new_cardinal_path = list(node['cardinal_path'])
                    new_cardinal_path.append(direction)
                    new_id_path = list(node['id_path'])
                    new_id_path.append(current_room[direction])
                    new_path = {
                        'cardinal_path': new_cardinal_path,
                        'id_path': new_id_path
                    }
                    q.enqueue(new_path)
    
traversal_path = []
locations = {}
unknown_exits = 0
previous_id = 0
locations[player.current_room.id] = {'n': None, 's': None, 'e': None, 'w':None}
for direction in player.current_room.get_exits():
    locations[player.current_room.id][direction] = '?'
    unknown_exits += 1

while bfs_unknown_path(locations) is not None:
    direction = choose_direction(locations[player.current_room.id])
    if direction is not None:
        traversal_path.append(direction)
        player.travel(direction)
        if player.current_room.id not in locations:
            locations[player.current_room.id] = {'n': None, 's': None, 'e': None, 'w':None}
            for room_exit in player.current_room.get_exits():
                if room_exit == opposite_direction(direction):
                    locations[player.current_room.id][room_exit] = previous_id
                else:
                    locations[player.current_room.id][room_exit] = '?'
                    unknown_exits += 1
        else:
            locations[player.current_room.id][opposite_direction(direction)] = previous_id
        locations[previous_id][direction] = player.current_room.id
        unknown_exits = unknown_exits - 1
    else:
        return_path = bfs_unknown_path(locations)
        for direciton in return_path:
            traversal_path.append(direciton)
            player.travel(direciton)
    
    previous_id = player.current_room.id


print(traversal_path)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
