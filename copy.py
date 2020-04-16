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
            return self.stack.pop(self.size() -1)
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
            print(last)

            if last not in visited:
                for neighbor in self.rooms[last]:
                    if self.rooms[last][neighbor] == '?':
                        # continue in that direction
                        # slice out room player is currently in
                        return path[1:]

                    elif self.rooms[last][neighbor] == previous:
                        # avoids adding previous room to path
                        continue

                    else:
                        # find nearest room with unexplored exits
                        visited.add(last)
                        path = path[:]
                        path.append(self.rooms[last][neighbor])
                        q.enqueue(path)
                        previous = int(last)
                        
            # else:
            #     # dead-end in wrong direction
            #     # TODO: figure out how to handle turning around with this search
            #     #       need to handle still keeping consistent path
            #     for neighbor in self.rooms[last]:
            #         path.append(self.rooms[last][neighbor])
            #         q.enqueue(path)
            #         previous = int(last)


# instantiate graph
adv_graph = AdventureGraph()
previous = None
# opposite = None
num_rooms = len(world.rooms)

# add starting room
adv_graph.add_room(player.current_room.id)

import pdb

while adv_graph.size < num_rooms:
    # pop out a room
    room = player.current_room
    print("-----", room.id)
    # pdb.set_trace()

    # if room has been visited previously
    if adv_graph.rooms.get(room.id):

        possibilities = []
        for neighbor in adv_graph.rooms[room.id]:
            # double var
            room = room.get_room_in_direction(neighbor)
            if room.id == previous.id:
                # link to previous room
                adv_graph.rooms[room.id][neighbor] = room.id
            # check to see to see if possible next moves
            # pdb.set_trace()
            # TODO: breaking here when we get back to 0 because this 
            #       neighbor is not in the graph. see 186
            if room.id in adv_graph.rooms:
                # covers neighbors that have not been visited yet
                if adv_graph.rooms[room.id][neighbor] == '?':
                    possibilities.append(neighbor)

        if len(possibilities) > 0:
            # randonly random unvisited direction
            d = random.randint(0, len(possibilities) -1)
            # traversal_path.append(possibilities[d])
            y = room.get_room_in_direction(possibilities[d])
            # travel
            previous = player.current_room
            player.travel(possibilities[d])
        else:
            # find nearest '?'
            # perform bfs
            # returns a path with a list of room IDS to the nearest room with a '?'
            path = adv_graph.bfs(player.current_room.id)
            directions = ['n', 's', 'e', 'w']
            
            for room_id in path:
                for way in directions:
                    # if current room has given ID in direction
                    if room.get_room_in_direction(way):
                        z = room.get_room_in_direction(way)
                        if z.id == room_id:
                            # move player, connect rooms
                            # traversal_path.append(way)
                            previous = player.current_room
                            player.travel(way)
    
    else:
        # add to graph
        adv_graph.add_room(room.id)
        # find all exits
        neighbors = room.get_exits()

        for neighbor in neighbors:
            # check if room in previous
            y = room.get_room_in_direction(neighbor)
            if y == previous:
                # link current room to previous in direction
                adv_graph.rooms[room.id][neighbor] = y.id
            else:
                # TODO: may need to rethink this to also add rooms in directions
                #       so they don't come back false on 139
                adv_graph.rooms[room.id][neighbor] = '?'
        # get random neighbor
        possibilities = []
        for neighbor in adv_graph.rooms[room.id]:
            if adv_graph.rooms[room.id][neighbor] == '?':
                possibilities.append(neighbor)
        
        # if unexplored neighbor
        if len(possibilities) > 0:
            d = random.randint(0, len(possibilities) -1)
            # connect move to path
            traversal_path.append(possibilities[d])
            # traversal_path.append(possibilities[d])
            # get room in direction traveling to
            y = room.get_room_in_direction(possibilities[d])
            # assign neighbor in current room before moving
            adv_graph.rooms[room.id][possibilities[d]] = y.id
            # iterate
            previous = room
            # connect new room to previous room
            player.travel(possibilities[d])

        else:
            # unexplored but no unexplored neighbors -> dead-end
            # returns a path with a list of room IDS to the 
            #   nearest room with a n unexplored neighbor
            path = adv_graph.bfs(player.current_room.id)

            directions = ['n', 's', 'e', 'w']
            # can probably move these out to a dict
            
            for room_id in path:
                # match IDs to directions from current room
                for way in directions:
                    if room.get_room_in_direction(way):
                        z = room.get_room_in_direction(way)
                        print("?", way)
                        print("!", z.id)
                        print("*", room_id)
                        if z.id == room_id:
                            # move player, connect rooms
                            # traversal_path.append(way)
                            previous = player.current_room
                            player.travel(way)

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
