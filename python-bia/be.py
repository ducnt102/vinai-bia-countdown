from flask import Flask, jsonify,send_from_directory
import threading
import time

app = Flask(__name__)

count_down = 60
running = False

def start_countdown():
    global count_down, running
    if not running:
        running = True
        while count_down > 0:
            count_down -= 1
            time.sleep(1)  # Đợi 1 giây
        running = False

def start_countdown_thread():
    countdown_thread = threading.Thread(target=start_countdown)
    countdown_thread.start()

@app.route('/')
def get_countdown():
    return jsonify({'count_down': count_down})

@app.route('/start')
def start():
    global count_down, running
    count_down = 60
    running = False
    start_countdown_thread()
    return jsonify({'message': 'Countdown started.'})

@app.route('/reset')
def reset():
    global count_down, running
    count_down = 60
    running = False
    return jsonify({'message': 'Countdown reset.'})

@app.route('/reboot')
def reboot():
    global count_down, running
    count_down = 60
    running = False
    return jsonify({'message': 'Rebooted without starting the countdown.'})

@app.route('/add')
def add_time():
    global count_down
    if not running:
        count_down += 30
        return jsonify({'message': 'Added 30 seconds to countdown.'})
    else:
        return jsonify({'message': 'Cannot add time while countdown is running.'})
@app.route('/fe')
def serve_html():
    return send_from_directory('static', 'index.html')

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='18088', debug=True)

