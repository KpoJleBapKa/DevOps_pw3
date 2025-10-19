import redis
import json
import os

class RedisManager:
    def __init__(self):
        # Підключення до Redis (використовуємо змінні середовища для Docker)
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            # Перевіряємо з'єднання
            self.redis_client.ping()
            print(f"Підключено до Redis на {redis_host}:{redis_port}")
        except redis.ConnectionError:
            print("Не вдалося підключитися до Redis. Використовується локальне збереження.")
            self.redis_client = None

    def save_score(self, score, lost):
        """Збереження результату гри"""
        game_result = {
            'score': score,
            'lost': lost,
            'timestamp': str(int(time.time()))
        }
        
        if self.redis_client:
            try:
                # Зберігаємо в Redis як JSON
                self.redis_client.lpush('game_scores', json.dumps(game_result))
                # Зберігаємо тільки останні 10 результатів
                self.redis_client.ltrim('game_scores', 0, 9)
                print(f"Результат збережено в Redis: {score} спіймано, {lost} пропущено")
            except Exception as e:
                print(f"Помилка збереження в Redis: {e}")
        else:
            print(f"Результат (локально): {score} спіймано, {lost} пропущено")

    def get_best_scores(self, limit=5):
        """Отримання найкращих результатів"""
        if self.redis_client:
            try:
                scores = self.redis_client.lrange('game_scores', 0, limit-1)
                best_scores = []
                for score_json in scores:
                    score_data = json.loads(score_json)
                    best_scores.append(score_data)
                return best_scores
            except Exception as e:
                print(f"Помилка отримання результатів з Redis: {e}")
                return []
        else:
            return []

    def get_stats(self):
        """Отримання статистики"""
        if self.redis_client:
            try:
                total_games = self.redis_client.llen('game_scores')
                return {'total_games': total_games}
            except Exception as e:
                print(f"Помилка отримання статистики: {e}")
                return {'total_games': 0}
        else:
            return {'total_games': 0}
