import requests
import json

from detailed_strategies import (
    ConsoleStrategy,
    KafkaStrategy,
    RedisStrategy,
    FileStrategy
)


class DataManager:
    def __init__(self, strategy):
        self.strategy = strategy

    def process_data(self, data_list):
        if not data_list:
            print("Дані порожні або не завантажені.")
            return

        for item in data_list:
            self.strategy.save(item)


def fetch_data(url):
    print(f"Запит до API: {url}")
    try:
        response = requests.get(url + "?$limit=10")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Помилка при отриманні даних: {e}")
        return []


if __name__ == "__main__":
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {"output_target": "console"}

    api_url = "https://data.cityofnewyork.us/resource/5ucz-vwe8.json"

    mapping = {
        "console": ConsoleStrategy(),
        "kafka": KafkaStrategy(),
        "redis": RedisStrategy(),
        "file": FileStrategy()
    }

    target = config.get("output_target", "console")
    selected_strategy = mapping.get(target, ConsoleStrategy())

    data = fetch_data(api_url)

    manager = DataManager(selected_strategy)
    manager.process_data(data)

    