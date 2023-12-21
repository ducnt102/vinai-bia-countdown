from flask import Flask, render_template
import threading
import time

app = Flask(__name__)

# Biến global để lưu trạng thái của countdown
countdown_time = 30

# Hàm để thực hiện countdown
def countdown():
    global countdown_time
    while countdown_time > 0:
        countdown_time -= 1
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html', countdown_time=countdown_time)

@app.route('/start')
def start_countdown():
    global countdown_time
    countdown_time = 30
    countdown_thread = threading.Thread(target=countdown)
    countdown_thread.start()
    return 'Started countdown'

@app.route('/reset')
def reset_countdown():
    global countdown_time
    countdown_time = 30
    return 'Reset countdown'

@app.route('/add')
def add_time():
    global countdown_time
    countdown_time += 30
    return 'Added 30 seconds'

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="18088")

