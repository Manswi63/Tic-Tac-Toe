from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [""] * 9
current_player = "X"

def check_winner():
    win_positions = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for x,y,z in win_positions:
        if board[x] == board[y] == board[z] != "":
            return board[x]
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global current_player

    data = request.json
    idx = data["index"]

    if board[idx] == "":
        board[idx] = current_player
        winner = check_winner()

        if winner:
            return jsonify({"status": "win", "player": winner})

        if "" not in board:
            return jsonify({"status": "draw"})

        current_player = "O" if current_player == "X" else "X"
        return jsonify({"status": "continue", "player": current_player})

    return jsonify({"status": "invalid"})

@app.route("/reset")
def reset():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)