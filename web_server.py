from flask import Flask, render_template_string, jsonify
import redis
import json
import os
import time

app = Flask(__name__)

# Підключення до Redis
def get_redis_connection():
    try:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        redis_client.ping()
        return redis_client
    except:
        return None

# HTML шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Гра Ловець - Статистика</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .stats { background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .game-info { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .redis-status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .connected { background: #d4edda; color: #155724; }
        .disconnected { background: #f8d7da; color: #721c24; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 Гра "Ловець" - Веб-інтерфейс</h1>
        
        <div class="game-info">
            <h3>Про гру:</h3>
            <p>Це гра "Ловець", де потрібно ловити яйця, що падають зверху. Використовуйте стрілки вліво/вправо для керування.</p>
            <p>Гра зберігає результати в Redis базі даних.</p>
        </div>

        <div class="redis-status" id="redis-status">
            <strong>Статус Redis:</strong> <span id="status-text">Перевірка...</span>
        </div>

        <div class="stats">
            <h3>📊 Статистика:</h3>
            <p><strong>Всього ігор:</strong> <span id="total-games">0</span></p>
            <p><strong>Останні результати:</strong></p>
            <div id="recent-scores">Завантаження...</div>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <button onclick="refreshStats()">🔄 Оновити статистику</button>
            <button onclick="simulateGame()">🎮 Симулювати гру</button>
        </div>
    </div>

    <script>
        function refreshStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-games').textContent = data.total_games;
                    document.getElementById('status-text').textContent = data.redis_connected ? 'Підключено ✅' : 'Не підключено ❌';
                    document.getElementById('redis-status').className = 'redis-status ' + (data.redis_connected ? 'connected' : 'disconnected');
                    
                    let scoresHtml = '';
                    if (data.recent_scores && data.recent_scores.length > 0) {
                        data.recent_scores.forEach(score => {
                            scoresHtml += `<p>Спіймано: ${score.score}, Пропущено: ${score.lost} (${new Date(score.timestamp * 1000).toLocaleString()})</p>`;
                        });
                    } else {
                        scoresHtml = '<p>Поки немає результатів</p>';
                    }
                    document.getElementById('recent-scores').innerHTML = scoresHtml;
                });
        }

        function simulateGame() {
            const score = Math.floor(Math.random() * 20) + 1;
            const lost = Math.floor(Math.random() * 5);
            
            fetch('/api/simulate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({score: score, lost: lost})
            })
            .then(response => response.json())
            .then(data => {
                alert(`Симуляція завершена! Спіймано: ${score}, Пропущено: ${lost}`);
                refreshStats();
            });
        }

        // Автоматичне оновлення кожні 5 секунд
        setInterval(refreshStats, 5000);
        
        // Початкове завантаження
        refreshStats();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    redis_client = get_redis_connection()
    
    if redis_client:
        try:
            total_games = redis_client.llen('game_scores')
            recent_scores = []
            scores = redis_client.lrange('game_scores', 0, 4)  # Останні 5 результатів
            for score_json in scores:
                score_data = json.loads(score_json)
                recent_scores.append(score_data)
            
            return jsonify({
                'redis_connected': True,
                'total_games': total_games,
                'recent_scores': recent_scores
            })
        except Exception as e:
            return jsonify({
                'redis_connected': False,
                'total_games': 0,
                'recent_scores': [],
                'error': str(e)
            })
    else:
        return jsonify({
            'redis_connected': False,
            'total_games': 0,
            'recent_scores': []
        })

@app.route('/api/simulate', methods=['POST'])
def simulate_game():
    from flask import request
    data = request.get_json()
    
    redis_client = get_redis_connection()
    if redis_client:
        try:
            game_result = {
                'score': data.get('score', 0),
                'lost': data.get('lost', 0),
                'timestamp': str(int(time.time()))
            }
            redis_client.lpush('game_scores', json.dumps(game_result))
            redis_client.ltrim('game_scores', 0, 9)  # Зберігаємо тільки останні 10
            
            return jsonify({'success': True, 'message': 'Результат збережено'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Redis не підключено'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
