from flask import Flask, request, jsonify

# starting flask
app = Flask(__name__)

# solver function
def water_jug_solver(x, y, z):
    # initializing a set and a queue to keep track of the states
    visited = set()
    queue = [(0, 0, [])]

    # looping until queue is empty
    while queue:
        current_state = queue.pop(0)
        if current_state[0] == z or current_state[1] == z:
            return [{'x': step[0], 'y': step[1], 'step': step[2]} for step in current_state[2][1:]] + [{'x': current_state[0], 'y': current_state[1], 'step': "Final state"}]

        # adding current state to the visited set
        visited.add((current_state[0], current_state[1], tuple(current_state[2])))

        # possible states
        next_states = [
            (x, current_state[1], current_state[2] + [(current_state[0], current_state[1], "Fill bucket X")]),
            (current_state[0], y, current_state[2] + [(current_state[0], current_state[1], "Fill bucket Y")]),
            (0, current_state[1], current_state[2] + [(current_state[0], current_state[1], "Empty bucket X")]),
            (current_state[0], 0, current_state[2] + [(current_state[0], current_state[1], "Empty bucket Y")]),
            (max(0, current_state[0] - (y - current_state[1])), min(y, current_state[1] + current_state[0]), current_state[2] + [(current_state[0], current_state[1], "Transfer from bucket X to bucket Y")]),
            (min(x, current_state[0] + current_state[1]), max(0, current_state[1] - (x - current_state[0])), current_state[2] + [(current_state[0], current_state[1], "Transfer from bucket Y to bucket X")])
        ]

        # iterating through possible next states
        for next_state in next_states:
            if (next_state[0], next_state[1], tuple(next_state[2])) not in visited:
                queue.append(next_state)

    # returning none in case of no solution
    return None

# getting x y and z data and calling the function
@app.route('/water-jug-solver', methods=['GET'])
def solve_water_jug_problem():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))

    solution = water_jug_solver(x, y, z)
    if solution:
        return jsonify({'solution': solution}), 200
    else:
        return jsonify({'message': 'No solution possible.'}), 404

# running application
if __name__ == '__main__':
    app.run(debug=True)
