import time
import http.client
import json
import ssl

# Ваш рабочий токен бота
TOKEN = "8933061429:AAEYSgsyCSEy7yomFKGxpJDsueoeBwf5fP8"

def send_api_request(method, data=None):
    """Безопасная функция запросов без SSL для корректной работы в облаке"""
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
        print(f"Ошибка сети: {e}")
        return None
    finally:
        connection.close()

def main():
    print("Бот для суда успешно запущен в облаке и работает 24/7!")
    offset = 0
    
    while True:
        try:
            # Получаем новые сообщения из группы
            updates = send_api_request("getUpdates", {"offset": offset, "timeout": 10})
            if updates and updates.get("result"):
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        message = update["message"]
                        chat_id = message["chat"]["id"]
                        text = message.get("text", "").strip().lower()
                        
                        # Проверяем, если триггерное слово содержит "суд"
                        if text == "суд":
                            user_name = message["from_user"].get("first_name", "Игрок")
                            
                            # Бот отправляет сообщение ровно 10 раз подряд
                            for i in range(10):
                                send_api_request("sendMessage", {
                                    "chat_id": chat_id,
                                    "text": f"⚖️ Игрок {user_name} подал в суд! Начните аудиозвонок, чтобы выяснить, что случилось!"
                                })
                                # Краткая пауза в полсекунды между сообщениями, чтобы Telegram не заблокировал за спам
                                time.sleep(0.5)
                                
        except Exception as e:
            print(f"Ошибка в цикле: {e}")
            time.sleep(5)
            
        time.sleep(1)

if __name__ == "__main__":
    main()
