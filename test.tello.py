import socket
import time

# TelloのIPアドレスとポート
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889

# コマンドを送信するためのソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = (TELLO_IP, TELLO_PORT)

def send_command(command):
    """
    Telloにコマンドを送信する関数
    """
    try:
        sock.sendto(command.encode('utf-8'), tello_address)
        print(f"Sending command: {command}")
    except Exception as e:
        print(f"Error sending command: {e}")

def receive_response():
    """
    Telloからのレスポンスを受信する関数
    """
    try:
        response, _ = sock.recvfrom(1024)
        print(f"Received response: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error receiving response: {e}")

def main():
    # コマンドモードを開始
    send_command("command")
    time.sleep(2)
    receive_response()

    # 離陸
    send_command("takeoff")
    time.sleep(5)
    receive_response()

    # 前進（100cm）
    send_command("forward 100")
    time.sleep(5)
    receive_response()

    # 後進（100cm）
    send_command("back 100")
    time.sleep(5)
    receive_response()

    # 旋回（時計回りに90度）
    send_command("cw 90")
    time.sleep(5)
    receive_response()

    # 着陸
    send_command("land")
    time.sleep(5)
    receive_response()

if __name__ == "__main__":
    main()