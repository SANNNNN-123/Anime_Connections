from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store leaderboard in memory (in a real app, use a database)
leaderboard = []

@app.route('/')
def index():
    return render_template('index.html', leaderboard=leaderboard)

@app.route('/submit-score', methods=['POST'])
def submit_score():
    data = request.json
    score = {
        'name': data['name'],
        'time': data['time'],
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    leaderboard.append(score)
    # Sort leaderboard by time (ascending)
    leaderboard.sort(key=lambda x: x['time'])
    # Keep only top 10 scores
    while len(leaderboard) > 10:
        leaderboard.pop()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)