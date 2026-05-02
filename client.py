# client.py 修正版
import socket

SERVER_ADDRESS = ('127.0.0.1', 5555)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(SERVER_ADDRESS)
print("连接成功")

# 接收欢迎消息
welcome = client_sock.recv(1024).decode('utf-8')
print(welcome)

while True:
    msg = input("你: ")
    if msg.lower() == 'quit':
        break
    client_sock.send(msg.encode('utf-8'))
    
    # 接收 AI 回复（服务器会发送两条消息：回复和提示）
    ai_reply = client_sock.recv(1024).decode('utf-8')
    print("AI:", ai_reply)
    next_prompt = client_sock.recv(1024).decode('utf-8')
    print(next_prompt)

client_sock.close()