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
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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
    
    # def get_room(self, id):
    #     if self.rooms.get(id) != None:
    #         return True
    #     else:
    #         return False

    def bfs(self, starting_node):
        """
        Search to find closest unexplored room by using
         a breadth-first search for a room with a `'?'`
        """

        q = Queue()
        q.enqueue([starting_node])
        visited = set()

        while q.size() > 0:
            path = q.dequeue()

            last = path[-1]
            previous = None

            if last not in visited:
                for neighbor in self.rooms[last]:
                    if neighbor == '?':
                        # continue in that direction
                        return path
                    elif self.rooms[last][neighbor] == previous:
                        # previous room
                        continue
                    else:
                        # find nearest '?'
                        # perform bfs
                        visited.add(last)
                        path = path[:]
                        
                        # need an actual room object for this to work...
                        # y = self.rooms[last].get_room_in_direction(neighbor)


                        path.append(self.rooms[last][neighbor])
                        q.enqueue(path)
                        previous = last

    
def dfs(starting_node, direction, queue, graph, player):
    """
    Move in one direction until no node in direction
    """

    s = Stack()
    s.add(starting_node)

    while s.size() > 0:
        room = s.pop()
        if graph.get_room(room.id) is False:
            # travel in dir and repeat
            # add room in dir to stack and repeat
            # for room in room.get_directions()
            # if room in dir given -> repeat
            # for every room not in dir -> enqueue
            pass
        # continue to traverse in direction and add to dictionary, connecting rooms as below


# create algorithm to traverse map
# push up direction headed each time player.move is called
# perform bfs to find any rooms with a '?' in any direction
#   if not, add to queue
# if so
# add to adv_graph.rooms
# continue bfs until self.rooms

# naive implimentation

# pick a smaller map
# travel in any available direction recursively until you cannot
# as you pass through rooms, add those to a queue to be recursively 
#   checked once that dead end is reached

# may need to pass traversal_path around if graph is searching for me

# instantiate graph and queue
adv_graph = AdventureGraph()
q = Queue()
# add starting room
q.enqueue(player.current_room)
num_rooms = len(world.rooms)

adv_graph.add_room(player.current_room.id)

# need to figure out how this is going to work entirely
# need to keep feeding the queue for this to work
while adv_graph.size < num_rooms:
    # do I need this queue ????
    # room = q.dequeue()
    
    # pop out a room
    room = player.current_room
    
    # if room has been visited previously
    if adv_graph.rooms.get(room.id):
        # x = room.get_exits()
        
        for neighbor in adv_graph.rooms[room.id]:
            # I'm hitting the else below before it checks all
            if neighbor == '?':
                # continue in that direction
                traversal_path.append(neighbor)
                print("moving", neighbor)
                y = room.get_room_in_direction(neighbor)
                room.connect_rooms(neighbor, y)
                player.travel(neighbor)
                # q.enqueue(player.current_room)
            else:
                # find nearest '?'
                # perform bfs
                
                import pdb
                pdb.set_trace()

                # returns a path with a list of room IDS to the nearest room with a '?'
                path = adv_graph.bfs(player.current_room.id)
                directions = ['n', 's', 'e', 'w']
                for room_id in path:
                    # **** need to change id to dir once received and execute steps ****
                    # check all directions and see if room in that direction == id
                    # looks like this will do a double check on current room because
                    # it is passed in and out of bfs
                    for d in directions:
                        z = room.get_room_in_direction(d)
                        if z.id == room_id:
                            # move player, connect rooms
                            traversal_path.append(d)
                            player.travel(d)
                    
                    # at final destination


                    # player.travel(move)
                    # q.enqueue(player.current_room)
    
    else:
        print(room.id)
        # add to graph
        adv_graph.add_room(room.id)
        # do things
        neighbors = room.get_exits()
        for neighbor in neighbors:
            adv_graph.rooms[room.id][neighbor] = '?'
            
        # get random neighbor
        d = random.randint(0, len(neighbors) -1)
        traversal_path.append(neighbors[d])
        # *** need to connect rooms as I move ***
        print("moving", d)
        y = room.get_room_in_direction(neighbors[d])
        room.connect_rooms(neighbors[d], y)
        player.travel(neighbors[d])
        # q.enqueue(player.current_room)
        
        # start moving in that direction
        # add to traversal path
        # record room for path
        # continue in dir until we cannot
        # find closest neighbor
    


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
