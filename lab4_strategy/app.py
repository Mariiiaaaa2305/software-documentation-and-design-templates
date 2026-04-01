import yaml
from reader import DataReader
from outputs import ConsoleOutput, FileOutput, RedisOutput, KafkaOutput


def main():
    with open("config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    mode = config.get("output_strategy", "console")

    if mode == "redis":
        strategy = RedisOutput(
            config["redis"]["host"],
            config["redis"]["port"],
        )
    elif mode == "kafka":
        strategy = KafkaOutput(
            config["kafka"]["bootstrap_servers"],
            config["kafka"]["topic"],
        )
    elif mode == "file":
        strategy = FileOutput(
            config["file"]["output_file"],
        )
    else:
        strategy = ConsoleOutput()

    reader = DataReader(config["csv_file_path"], strategy)
    reader.execute()


if __name__ == "__main__":
    main()