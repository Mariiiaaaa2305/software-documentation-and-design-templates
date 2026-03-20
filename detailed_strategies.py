import json
from strategy import OutputStrategy


class ConsoleStrategy(OutputStrategy):
    def save(self, data):
        print(
            f"STDOUT: ID: {data.get('incident_key')}, "
            f"дата: {data.get('occur_date')}, "
            f"час: {data.get('occur_time')}, "
            f"район: {data.get('boro')}, "
            f"тип: {data.get('loc_classfctn_desc')}"
        )


class KafkaStrategy(OutputStrategy):
    def save(self, data):
        print(
            f"KAFKA: Event ID {data.get('incident_key')} | "
            f"район: {data.get('boro')} -> topic 'fire_incidents'"
        )


class RedisStrategy(OutputStrategy):
    def save(self, data):
        print(
            f"REDIS: Cache incident {data.get('incident_key')} "
            f"({data.get('boro')})"
        )


class FileStrategy(OutputStrategy):
    def save(self, data):
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

        print(f"FILE: Записано інцидент ID {data.get('incident_key')}")