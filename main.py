from flask import Flask, jsonify, request

# Examples
small_maze = {"forward": "tiger",
              "left": {"forward": {"upstairs": "exit"},
                       "left": "dragon"},
              "right": {"forward": "dead end"}}

two_exits = {"forward": "tiger",
             "left": {"forward": {"upstairs": "exit"},
                      "left": "exit"},
             "right": {"forward": "dead end"}}

Exit = {"forward": "exit"}

no_exit = {"forward": "tiger", "left": "ogre", "right": "demon"}


# the_maze uses recursion to give the available exit in the room. This function ius the used in maze function
def the_maze(direction, room):
    for x in room:
        if room[x] == "exit":
            direction = direction + x + " "
            return direction
        elif type(room[x]) == type(room):
            direction = direction + x + " "
            return the_maze(direction, room[x])
    return "sorry"


# Testing the_maze function with the examples
print("---------- the_maze function--------")
print()
print(the_maze("", small_maze))
print(the_maze("", two_exits))
print(the_maze("", Exit))
print(the_maze("", no_exit))
print()
print()


# uses the_maze function to find the exit direction if available. The function only suggests one exit route at a call
def maze(room):
    direction = ""
    return the_maze(direction, room)


# Testing maze function with the examples
print("----------maze function--------")
print()
print(maze(small_maze))
print(maze(two_exits))
print(maze(Exit))
print(maze(no_exit))
print()
print()

"""
A post endpoint to give direction of the maze provided in json.
sample_input = {"maze": {"forward": "tiger",
              "left": {"forward": {"upstairs": "exit"},
                       "left": "dragon"},
              "right": {"forward": "dead end"}}}

sample_output = left forward upstairs (these are the directions in order to exit the maze)
"""
app = Flask(__name__)


# This POST endpoint can be tested on postman. Gives you the direction to exit a given maze
@app.route('/maze/solve', methods=['POST'])
def solve_maze():
    room = {'maze': request.json['maze']}
    return maze(room["maze"])


# (Bonus): Input: maximum_children. Output: list of mazes with the input number as maximum number of nodes
@app.route('/maze/generate/<string:max_children>', methods=['GET'])
def get_maze(max_children):
    if max_children == "2":
        mazes = [small_maze, two_exits]
        return jsonify({'maze': mazes})
    elif max_children == "1":
        mazes = [Exit, no_exit]
        return jsonify({'maze': mazes})
    else:
        return "no maze with such nodes"


if __name__ == '__main__':
    app.run(debug=True, port=8080)


# (Bonus): How to generate an Infinite maze
"""
We can generate an infinite maze using a simple Depth-first search algorithm
1. Start at a random cell.
2. Mark the current cell as visited, and get a list of its neighbors. For each neighbor, 
starting with a randomly selected neighbor:
    If that neighbor hasn't been visited, remove the wall between this cell and that neighbor, 
    and then recurse with that neighbor as the current cell.
"""
