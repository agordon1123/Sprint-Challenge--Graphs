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

# create a depth first traveral to move until 
# find a room that has been visited
# check room to see if rooms next to it that have been visited
# if so -> continue depth first traversal
# if not -> perform a breadth first search to find 
# next room unvisited

visited = set()

def bfs(starting_room, visited):
    # create a path from the starting node to 
    # the next unvisited node
    queue = []
    moves = [[]]
    queue.append([starting_room])
    
    while len(queue) > 0:
        current_path = queue.pop(0)
        current_room = current_path[-1]
        path_moves = moves.pop(0)
        
        for direction in current_room.get_exits():
            neighbor = current_room.get_room_in_direction(direction)
            # unvisited room found
            if neighbor.id not in visited: 
                path_moves.append(direction)
                return path_moves
            else:
                # continue bfs
                copy1 = list(current_path)
                copy1.append(neighbor)
                copy2 = list(path_moves)
                copy2.append(direction)
                queue.append(copy1)
                moves.append(copy2)


def dft(starting_direction, starting_room, visited):
    # traverse until reaching a previously visited room
    stack = []
    moves = []
    stack.append(starting_room)
    moves.append(starting_direction)
    
    while len(stack) > 0:
        current_room = stack.pop()
        travel_to = moves.pop()
        # move player while traversing
        player.travel(travel_to)
        traversal_path.append(travel_to)

        if current_room.id not in visited:
            visited.add(current_room.id)
            # create a list of possible next moves
            unvisited_neighbors = []
            for direction in current_room.get_exits():
                neighbor = current_room.get_room_in_direction(direction)
                if neighbor.id not in visited:
                    unvisited_neighbors.append((direction, neighbor))
            # choose a random neighbor to move to
            if len(unvisited_neighbors) > 0:
                rand_index = random.randint(0, len(unvisited_neighbors)-1)
                moves.append(unvisited_neighbors[rand_index][0])
                stack.append(unvisited_neighbors[rand_index][1])
            else:
                return

while len(visited) < len(room_graph):

    current_room = player.current_room

    if current_room.id not in visited:        
        visited.add(current_room.id)
        # create list of possible next moves
        unvisited_neighbors = []
        for direction in current_room.get_exits():
            neighbor = current_room.get_room_in_direction(direction)
            if neighbor.id not in visited:
                unvisited_neighbors.append((direction, neighbor))
        # call dft on randomly chosen neighbor
        if len(unvisited_neighbors) > 0:
            rand_index = random.randint(0, len(unvisited_neighbors)-1)
            dft(unvisited_neighbors[rand_index][0], unvisited_neighbors[rand_index][1], visited)
    else:
        # perform bfs to find closest path to next unvisited room
        path_to_unvisited = bfs(current_room, visited)
        for direction in path_to_unvisited:
            player.travel(direction)
            traversal_path.append(direction)

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
