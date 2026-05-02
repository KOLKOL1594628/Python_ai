# socket_server.py 修正版
import socket
import threading
from ai_api import AI#将主AI回答稍微修改了一下

# 全局 AI 实例（只加载一次模型）
ai_model = AI()

def handle_client(client_sock, addr):
    """处理单个客户端的所有消息"""
    print(f"客户端 {addr} 已连接")
    client_sock.send("你可以发送消息询问AI".encode('utf-8'))
    try:
        while True:
            # 接收客户端消息
            data = client_sock.recv(1024).decode('utf-8')
            if not data:   # 客户端断开
                break
            print(f"收到来自 {addr} 的消息: {data}")
            
            # 调用 AI 获取回复
            ai_model.get_response(data)
            response_text = ai_model.response
            
            # 发送回复
            client_sock.send(response_text.encode('utf-8'))
            client_sock.send("\n你可以问下一个问题了".encode('utf-8'))
    except (ConnectionResetError, BrokenPipeError):
        print(f"客户端 {addr} 连接异常断开")
    finally:
        client_sock.close()
        print(f"客户端 {addr} 已断开")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("服务器启动，等待连接...")
    while True:
        client_sock, addr = server.accept()
        # 为每个客户端创建一个线程
        t = threading.Thread(target=handle_client, args=(client_sock, addr))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    start_server()