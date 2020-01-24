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
traversal_path = []

# TODO: COMPLETE THIS!!!

class AdventureGraph:
    def __init__(self, size=0):
        self.rooms = {}
        self.exits = {}
        self.size = size

# instantiate graph and queue
adv_graph = AdventureGraph()
num_rooms = len(world.rooms)
path = [None]
# dirs used to turn around
reverse = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }

# add starting room to graph
adv_graph.rooms[player.current_room.id] = player.current_room.get_exits()
# add exits
adv_graph.exits[player.current_room.id] = player.current_room.get_exits()

# while all rooms have not been loaded into graph
while len(adv_graph.rooms) < num_rooms:
    if player.current_room.id not in adv_graph.rooms:
        # add room
        adv_graph.rooms[player.current_room.id] = player.current_room.get_exits()
        # add exits
        adv_graph.exits[player.current_room.id] = player.current_room.get_exits()
        # remove last exit explored from room
        last_dir = path[-1]
        adv_graph.exits[player.current_room.id].remove(last_dir)

    # no exits in room -> turn around until find a room with exits
    while len(adv_graph.exits[player.current_room.id]) < 1: 
        last_dir = path.pop()
        traversal_path.append(last_dir)
        player.travel(last_dir)

    # grab available exit
    exit_dir = adv_graph.exits[player.current_room.id].pop(0)
    # travel
    traversal_path.append(exit_dir)
    path.append(reverse[exit_dir])
    player.travel(exit_dir)

    # add exits for final room
    if len(world.rooms) - len(adv_graph.rooms) == 1:
        adv_graph.rooms[player.current_room.id] = player.current_room.get_exits()


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
