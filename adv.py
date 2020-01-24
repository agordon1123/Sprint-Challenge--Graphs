from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# TODO: COMPLETE THIS!!!

class Queue:
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

class Stack:
    def __init__(self):
        self.stack = []
    
    def add(self, value):
        self.stack.append(value)
    
    def pop(self):
        if self.size() > 0:
            return self.stack.pop(0)

    def size(self):
        return len(self.stack)

class AdventureGraph:
    def __init__(self, size=0):
        self.rooms = {}
        self.size = size

    def add_room(self, id):
        self.rooms[id] = {}
        self.size += 1

    def bfs(self, starting_node):
        """
        Search to find closest unexplored room by using
         a breadth-first search for a room with a `'?'`
        """

        q = Queue()
        q.enqueue([starting_node])
        visited = set()
        previous = None

        while q.size() > 0:
            path = q.dequeue()

            last = path[-1]
            print("last: ", last)

            if last not in visited:
                for neighbor in self.rooms[last]:
                    if self.rooms[last][neighbor] == '?':
                        # continue in that direction
                        print("path: ", path[1:])
                        return path[1:]
                    elif self.rooms[last][neighbor] == previous:
                        # previous room
                        print("do nothing")
                    else:
                        # find nearest '?'
                        # perform bfs
                        visited.add(last)
                        path = path[:]
                        
                        # need an actual room object for this to work...
                        # y = self.rooms[last].get_room_in_direction(neighbor)

                        print("108: ", self.rooms[last][neighbor])
                        path.append(self.rooms[last][neighbor])
                        q.enqueue(path)
                        previous = int(last)
                        print("112: ", previous)
            else:
                # dead-end in wrong direction
                for neighbor in self.rooms[last]:
                    path.append(last)
                    path.append(self.rooms[last][neighbor])
                    q.enqueue(path)
                    previous = int(last)

def dft(self, starting_node):
    """
    Print each vertex in depth-first order
    beginning from starting_node.
    """
    # Create an empty stack and push the starting vertex ID
    s = Stack()
    s.add(starting_node)
    # Create a Set to store visited vertices
    visited = set()
    # While the stack is not empty...
    while s.size() > 0:
        # Pop the first vertex
        v = s.pop()
        if v not in visited:
            print(v)
            visited.add(v)
            for neighbor in self.rooms[v]:
                s.add(neighbor)

# instantiate graph and queue
adv_graph = AdventureGraph()
# q = Queue()
# add starting room
# q.enqueue(player.current_room)
# previous = None
# crumb_trail = []
num_rooms = len(world.rooms)

# adv_graph.add_room(player.current_room.id)
# adv_graph.rooms[player.current_room.id] = player.current_room.get_exits()

import pdb

path = [None]

# used to hold exits yet to be explored
room_exits = {}
# add room to graph
adv_graph.rooms[player.current_room.id] = player.current_room.get_exits()
# add exits
room_exits[player.current_room.id] = player.current_room.get_exits()
# dirs used to turn around
reverse = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }

# while all rooms have not been loaded into graph
while len(adv_graph.rooms) < num_rooms:
    if player.current_room.id not in adv_graph.rooms:
        # add room
        adv_graph.rooms[player.current_room.id] = player.current_room.get_exits()
        # add exits
        room_exits[player.current_room.id] = player.current_room.get_exits()
        # remove last exit explored from room
        last_dir = path[-1]
        room_exits[player.current_room.id].remove(last_dir)

    # no exits in room -> turn around until find a room with exits
    while len(room_exits[player.current_room.id]) < 1: 
        last_dir = path.pop()
        traversal_path.append(last_dir)
        player.travel(last_dir)

    # grab available exit
    exit_dir = room_exits[player.current_room.id].pop(0)
    # travel
    traversal_path.append(exit_dir)
    path.append(reverse[exit_dir])
    player.travel(exit_dir)

    # add exits for final room
    if len(world.rooms) - len(adv_graph.rooms) == 1:
        adv_graph.rooms[player.current_room.id] = player.current_room.get_exits()

    # # if room has been visited previously
    # if adv_graph.rooms.get(room.id):

    #     if previous is not None and opposite is not None:
    #         adv_graph.rooms[room.id][opposite] = previous.id

    #     possibilities = []
    #     for neighbor in adv_graph.rooms[room.id]:
    #         # z = room.get_room_in_direction(neighbor)
    #         # if z.id == previous.id:
    #         #     # link
    #         #     adv_graph.rooms[room.id][neighbor] = z.id

    #         if adv_graph.rooms[room.id][neighbor] == '?':
    #             possibilities.append(neighbor)
        
    #     if len(possibilities) > 0:
    #         # randonly choose and move
    #         d = random.randint(0, len(possibilities) -1)
    #         traversal_path.append(possibilities[d])
    #         y = room.get_room_in_direction(possibilities[d])
    #         # room.connect_rooms(possibilities[d], y)
    #         previous = player.current_room
    #         player.travel(possibilities[d])
    #     else:
    #         # find nearest '?'
    #         # perform bfs

    #         # returns a path with a list of room IDS to the nearest room with a '?'
    #         path = adv_graph.bfs(player.current_room.id)
    #         directions = ['n', 's', 'e', 'w']
    #         for room_id in path:
    #             # looks like this will do a double check on current room because
    #             # it is passed in and out of bfs
    #             print("rooms: ", adv_graph.rooms)
    #             for d in directions:
    #                 if room.get_room_in_direction(d):
    #                     z = room.get_room_in_direction(d)
    #                     if z.id == room_id:
    #                         # move player, connect rooms
    #                         traversal_path.append(d)
    #                         previous = player.current_room
    #                         player.travel(d)
                            
    #                         if d == 'n':
    #                             opposite = 's'
    #                         if d == 's':
    #                             opposite = 'n'
    #                         if d == 'e':
    #                             opposite = 'w'
    #                         if d == 'w':
    #                             opposite = 'e'
                
    #             # at final destination


    #                 # player.travel(move)
    #                 # q.enqueue(player.current_room)
    
    # else:
    #     # add to graph
    #     adv_graph.add_room(room.id)
    #     if previous is not None and opposite is not None:
    #         adv_graph.rooms[room.id][opposite] = previous.id
    #     # find all exits
    #     neighbors = room.get_exits()

    #     for neighbor in neighbors:
    #         # check if room in previous
    #         y = room.get_room_in_direction(neighbor)
    #         if y == previous:
    #             # link current room to previous in direction
    #             adv_graph.rooms[room.id][neighbor] = y.id
    #         else:
    #             adv_graph.rooms[room.id][neighbor] = '?'

    #     # get random neighbor
    #     possibilities = []
    #     for neighbor in adv_graph.rooms[room.id]:
    #         if adv_graph.rooms[room.id][neighbor] == '?':
    #             possibilities.append(neighbor)
        
    #     # if unexplored neighbor
    #     if len(possibilities) > 0:
    #         d = random.randint(0, len(possibilities) -1)
    #         # connect move to path
    #         traversal_path.append(possibilities[d])
    #         # get room in direction traveling to
    #         y = room.get_room_in_direction(possibilities[d])
    #         # assign neighbor in current room before moving
    #         adv_graph.rooms[room.id][possibilities[d]] = y.id
    #         # iterate
    #         previous = room
    #         # connect new room to previous room
    #         player.travel(possibilities[d])

    #         if possibilities[d] == 'n':
    #             opposite = 's'
    #         if possibilities[d] == 's':
    #             opposite = 'n'
    #         if possibilities[d] == 'e':
    #             opposite = 'w'
    #         if possibilities[d] == 'w':
    #             opposite = 'e'
            
    #         # q.enqueue(player.current_room)
    #     else:
    #         # unexplored but no unexplored neighbors -> dead-end

    #         # returns a path with a list of room IDS to the 
    #         #   nearest room with a n unexplored neighbor

    #         path = adv_graph.bfs(player.current_room.id)
                        
    #         directions = ['n', 's', 'e', 'w']
    #         for room_id in path:
    #             print("room_id: ", room_id)
    #             print(player.current_room.id)
    #             # looks like this will do a double check on current room because
    #             # it is passed into bfs and checked
    #             # import pdb
    #             # pdb.set_trace()
    #             for d in directions:
    #                 print("243 d: ", d)
    #                 if room.get_room_in_direction(d):
    #                     z = room.get_room_in_direction(d)
    #                     if z.id == room_id:
    #                         # move player, connect rooms
    #                         traversal_path.append(d)
    #                         previous = player.current_room
    #                         player.travel(d)

    #                         if d == 'n':
    #                             opposite = 's'
    #                         if d == 's':
    #                             opposite = 'n'
    #                         if d == 'e':
    #                             opposite = 'w'
    #                         if d == 'w':
    #                             opposite = 'e'

    #                         # adv_graph.rooms[player.current_room.id][opposite] = previous.id



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
