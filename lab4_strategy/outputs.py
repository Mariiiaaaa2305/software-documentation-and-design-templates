import json
import redis
from abc import ABC, abstractmethod


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
        return (
            f"ID: {self.incident_key} | "
            f"Borough: {self.boro} | "
            f"Date: {self.occur_date}"
        )


class OutputStrategy(ABC):
    @abstractmethod
    def write(self, data):
        pass


class ConsoleOutput(OutputStrategy):
    def write(self, data):
        print("\n=== [STRATEGY: CONSOLE] ===")
        for item in data[:10]:
            print(item)
        print(f"Total processed: {len(data)} records.")


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
        print(f"[FILE] Saved {len(data)} records to file: {self.output_file}")


class RedisOutput(OutputStrategy):
    def __init__(self, host="localhost", port=6379):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    def write(self, data):
        print("\n=== [STRATEGY: REDIS] ===")
        for item in data:
            self.r.set(
                f"shooting:{item.incident_key}",
                json.dumps(item.to_dict(), ensure_ascii=False),
            )
            print(
                f"[REDIS] Saved: "
                f"ID={item.incident_key} | BORO={item.boro} | DATE={item.occur_date}"
            )
        print(f"Successfully saved {len(data)} records to Redis.")


class KafkaOutput(OutputStrategy):
    def __init__(self, bootstrap_servers="localhost:9092", topic="shootings"):
        from kafka import KafkaProducer

        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda value: json.dumps(
                value,
                ensure_ascii=False
            ).encode("utf-8"),
        )

    def write(self, data):
        print("\n=== [STRATEGY: KAFKA] ===")
        for item in data:
            self.producer.send(self.topic, item.to_dict())
            print(
                f"[KAFKA] Sent: "
                f"ID={item.incident_key} | BORO={item.boro} | DATE={item.occur_date}"
            )
        self.producer.flush()
        print(f"Sent {len(data)} records to Kafka topic: {self.topic}")