import time
import http.client
import json
import ssl

# Твой рабочий токен
TOKEN = "8943567222:AAEVUVR5QDY-DWhlP9erjQiJ4jjzSR28mD8"

def send_api_request(method, data=None):
    context = ssl._create_unverified_context()
    connection = http.client.HTTPSConnection("api.telegram.org", timeout=15, context=context)
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
        print(f"Ошибка запроса: {e}")
        return None
    finally:
        connection.close()

def main():
    print("Бот слушает команды...")
    offset = 0
    
    # Сбрасываем старые вебхуки, чтобы работал обычный опрос
    send_api_request("deleteWebhook")
    
    while True:
        try:
            updates = send_api_request("getUpdates", {"offset": offset, "timeout": 20})
            if updates and updates.get("result"):
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg.get("text", "").strip().lower()
                        
                        # Ловит /sud или /sud@юзернейм
                        if text.startswith("/sud"):
                            user = msg.get("from", {}).get("first_name", "Игрок")
                            for _ in range(10):
                                send_api_request("sendMessage", {
                                    "chat_id": chat_id,
                                    "text": f"⚖️ Игрок {user} подал в суд! Начните аудиозвонок, чтобы выяснить, что случилось!"
                                })
                                time.sleep(0.4)
        except Exception as e:
            print(f"Ошибка цикла: {e}")
            time.sleep(3)
        time.sleep(1)

if __name__ == "__main__":
    main()
