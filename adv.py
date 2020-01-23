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
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
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

import pdb
pdb.set_trace()

class adv_graph:
    def __init__(self, size=0):
        self.rooms = {}
        self.size = size

    def add_room(self, id):
        self.rooms[id] = { 'n': '?', 's': '?', 'e': '?', 'w': '?' }
        self.size += 1



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
