import unittest
import requests
import time

class TestMessengerIntegration(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"

    def test_full_chat_flow(self):
        # 1. Реєструємо двох юзерів
        u1 = requests.post(f"{self.BASE_URL}/register", json={"username": "Artem", "password": "1"}).json()
        u2 = requests.post(f"{self.BASE_URL}/register", json={"username": "Ivan", "password": "2"}).json()
        
        # 2. Створюємо чат між ними
        chat = requests.post(f"{self.BASE_URL}/conversations", json={
            "name": "Artem & Ivan",
            "participants": [u1['id'], u2['id']]
        }).json()
        
        # 3. Відправляємо повідомлення
        msg_text = "Привіт, це реальний месенджер!"
        requests.post(f"{self.BASE_URL}/messages", json={
            "conversation_id": chat['conversation_id'],
            "sender_id": u1['id'],
            "text": msg_text
        })
        
        # 4. Перевіряємо, чи є воно в історії
        history = requests.get(f"{self.BASE_URL}/conversations/{chat['conversation_id']}/messages").json()
        self.assertTrue(any(m['text'] == msg_text for m in history))

if __name__ == '__main__':
    unittest.main()