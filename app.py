import threading
from flask import Flask
import spamdis

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Trần Minh Đức đang hoạt động 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    # Chạy Web Server Flask trên luồng riêng để giữ dịch vụ luôn mở
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # Khởi chạy Bot Discord chính
    TOKEN = spamdis.os.getenv("DISCORD_TOKEN")
    if TOKEN:
        spamdis.bot.run(TOKEN)
    else:
        print("❌ Lỗi: Chưa cấu hình DISCORD_TOKEN trong biến môi trường!")
