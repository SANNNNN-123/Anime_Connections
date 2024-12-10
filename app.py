from flask import Flask, render_template, request, jsonify
from src.database import init_db,get_onepiece_data,get_ALL_data
from datetime import datetime

app = Flask(__name__)

# Store leaderboard in memory (in a real app, use a database)
leaderboard = []

@app.route('/')
def index():

    initial_data = {
        'easy': get_onepiece_data('easy'),
        'medium': get_onepiece_data('medium'),
        'hard': get_onepiece_data('hard')
    }
    print("Intial data from route:",initial_data)
    return render_template('index.html', leaderboard=leaderboard, initial_data=initial_data)


@app.route('/api/onepiece-data')
def onepiece_data():
    difficulty = request.args.get('difficulty', 'easy')
    try:
        data = get_onepiece_data(difficulty)
        print(f"Fetched data for difficulty {difficulty}:", data)
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
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
    init_db()
    app.run(debug=True)