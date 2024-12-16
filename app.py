from flask import Flask, render_template, request, jsonify
from src.database import init_db,get_onepiece_data,get_new_onepiece_data,insert_data_from_json
from datetime import datetime

app = Flask(__name__)

# Store leaderboard in memory (in a real app, use a database)
leaderboard = []

@app.route('/')
def index():
    return render_template('index.html', leaderboard=leaderboard)


@app.route('/api/onepiece-data')
def onepiece_data():
    difficulty = request.args.get('difficulty', 'easy')
    try:
        data = get_onepiece_data(difficulty)
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return jsonify({"error": str(e)}), 500

#when timer runs out load new data, instead old one
@app.route('/api/new-onepiece-data')
def new_onepiece_data():
    difficulty = request.args.get('difficulty', 'easy')
    try:
        data = get_new_onepiece_data(difficulty)
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching new data: {str(e)}")
        return jsonify({"error": str(e)}), 500

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
    #init_db()
    #insert_data_from_json("puzzles/easy_puzzles_20241215_045446.json")
    app.run(debug=True)