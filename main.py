import os
import json
import http.client
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer

# Ваш новый безопасный токен бота
TOKEN = "8943567222:AAEVUVR5QDY-DWhlP9erjQiJ4jjzSR28mD8"

def send_api_request(method, data=None):
    context = ssl._create_unverified_context()
    connection = http.client.HTTPSConnection("api.telegram.org", timeout=10, context=context)
    path = f"/bot{TOKEN}/{method}"
    try:
        headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        if data:
            body = json.dumps(data).encode('utf-8')
            connection.request("POST", path, body=body, headers=headers)
        else:
            connection.request("GET", path, headers=headers)
        response = connection.getresponse()
        return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Ошибка Telegram API: {e}")
        return None
    finally:
        connection.close()

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip().lower()
                
                # Реагируем на команду "суд" в любом регистре
                if text == "суд":
                    user_name = message["from"].get("first_name", "Игрок")
                    for _ in range(10):
                        send_api_request("sendMessage", {
                            "chat_id": chat_id,
                            "text": f"⚖️ Игрок {user_name} подал в суд! Начните аудиозвонок, чтобы выяснить, что случилось!"
                        })
        except Exception as e:
            print(f"Ошибка обработки вебхука: {e}")
            
        self.send_response(200)
        self.end_headers()

def run():
    # Сервер автоматически подхватит порт от хостинга
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebhookHandler)
    print(f"Сервер бота запущен на порту {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
