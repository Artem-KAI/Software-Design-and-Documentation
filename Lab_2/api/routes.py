from flask import request, jsonify
from storage.database import get_db
import uuid
from datetime import datetime

def setup_routes(app):
    
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        user_id = str(uuid.uuid4())
        try:
            conn = get_db()
            conn.execute('INSERT INTO users (id, username, password) VALUES (?, ?, ?)', 
                         (user_id, data['username'], data['password']))
            conn.commit()
            return jsonify({"id": user_id, "username": data['username']}), 201
        except:
            return jsonify({"error": "User already exists"}), 400

    @app.route('/conversations', methods=['POST'])
    def create_conversation():
        data = request.json
        participants = sorted(data['participants']) # Сортуємо, щоб порядок ID не мав значення
        p_string = ",".join(participants)
        
        conn = get_db()
        
        # Шукаємо, чи є вже чат з такими учасниками (для простоти шукаємо по імені)
        existing = conn.execute('SELECT id FROM conversations WHERE name = ?', (p_string,)).fetchone()
        
        if existing:
            return jsonify({"conversation_id": existing['id']}), 200
            
        # Якщо немає — створюємо новий
        conv_id = str(uuid.uuid4())
        conn.execute('INSERT INTO conversations (id, name, is_group) VALUES (?, ?, ?)', 
                    (conv_id, p_string, data.get('is_group', 0)))
        
        for u_id in participants:
            conn.execute('INSERT INTO participants (conversation_id, user_id) VALUES (?, ?)', (conv_id, u_id))
        
        conn.commit()
        return jsonify({"conversation_id": conv_id}), 201

    @app.route('/messages', methods=['POST'])
    def send_message():
        data = request.json
        msg_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        conn = get_db()
        conn.execute('INSERT INTO messages (id, conversation_id, sender_id, text, timestamp) VALUES (?, ?, ?, ?, ?)',
                     (msg_id, data['conversation_id'], data['sender_id'], data['text'], timestamp))
        conn.commit()
        return jsonify({"id": msg_id, "status": "sent"}), 201

    @app.route('/conversations/<conv_id>/messages', methods=['GET'])
    def get_messages(conv_id):
        conn = get_db()
        # Використовуємо JOIN, щоб дістати ім'я відправника разом із повідомленням
        query = '''
            SELECT m.*, u.username as sender_name 
            FROM messages m 
            JOIN users u ON m.sender_id = u.id 
            WHERE m.conversation_id = ? 
            ORDER BY m.timestamp
        '''
        messages = conn.execute(query, (conv_id,)).fetchall()
        return jsonify([dict(m) for m in messages])