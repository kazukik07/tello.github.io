from flask import Flask, render_template, request, jsonify
from djitellopy import Tello
import socket

app = Flask(__name__)
tello = Tello()

# Telloへの接続を一度だけ行う
is_connected = False

def safe_connect():
    global is_connected
    if not is_connected:
        try:
            tello.connect()
            is_connected = True
            return True
        except socket.error as e:
            print(f"接続エラー: {e}")
            return False
    return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_connection')
def check_connection():
    if safe_connect():
        return jsonify({"status": "Success"})
    else:
        return jsonify({"status": "Error"})

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    forward_distance = data.get('forward', 0)
    left_distance = data.get('left', 0)
    right_distance = data.get('right', 0)

    try:
        if not safe_connect():
            raise Exception("Telloとの接続に失敗しました")

        # Telloの離陸
        tello.takeoff()

        # 受け取ったデータに基づいてドローンを移動
        if forward_distance > 0:
            tello.move_forward(forward_distance)
        if left_distance > 0:
            tello.move_left(left_distance)
        if right_distance > 0:
            tello.move_right(right_distance)

        # 着陸
        tello.land()
        return jsonify({"status": "Success", "message": "Tello completed the movements"})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

    finally:
        try:
            # 安全に終了処理
            tello.end()
        except:
            pass

if __name__ == '__main__':
    app.run(debug=True)
