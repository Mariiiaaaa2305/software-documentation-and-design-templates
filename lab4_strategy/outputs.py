import json
import redis
from abc import ABC, abstractmethod
from kafka import KafkaProducer


class ShootingIncident:
    def __init__(self, incident_key, boro, occur_date):
        self.incident_key = incident_key
        self.boro = boro
        self.occur_date = occur_date

    def to_dict(self):
        return {
            "incident_key": self.incident_key,
            "boro": self.boro,
            "date": self.occur_date,
        }

    def __str__(self):
        return f"ID: {self.incident_key} | Borough: {self.boro} | Date: {self.occur_date}"


class OutputStrategy(ABC):
    @abstractmethod
    def write(self, data):
        pass


class ConsoleOutput(OutputStrategy):
    def write(self, data):
        print("\n=== OUTPUT TO CONSOLE ===")
        for item in data[:10]:
            print(item)
        print(f"\nTotal processed: {len(data)} records.")


class FileOutput(OutputStrategy):
    def __init__(self, output_file="data/output.json"):
        self.output_file = output_file

    def write(self, data):
        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump(
                [item.to_dict() for item in data],
                file,
                ensure_ascii=False,
                indent=2,
            )
        print(f"Saved {len(data)} records to file")


class RedisOutput(OutputStrategy):
    def __init__(self, host="redis", port=6379):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    def write(self, data):
        for item in data:
            self.r.set(
                f"shooting:{item.incident_key}",
                json.dumps(item.to_dict()),
            )
        print(f"Saved {len(data)} records to Redis")


class KafkaOutput(OutputStrategy):
    def __init__(self, bootstrap_servers="kafka:9092", topic="shootings"):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

    def write(self, data):
        for item in data:
            self.producer.send(self.topic, item.to_dict())
        self.producer.flush()
        print(f"Sent {len(data)} records to Kafka")