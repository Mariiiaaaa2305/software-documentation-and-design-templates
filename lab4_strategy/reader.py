import csv
from outputs import ShootingIncident


class DataReader:
    def __init__(self, file_path, strategy):
        self.file_path = file_path
        self.strategy = strategy

    def execute(self):
        data = []

        try:
            with open(self.file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if len(data) >= 100:
                        break

                    data.append(
                        ShootingIncident(
                            row.get("INCIDENT_KEY", "N/A"),
                            row.get("BORO", "N/A"),
                            row.get("OCCUR_DATE", "N/A"),
                        )
                    )

            if data:
                self.strategy.write(data)
            else:
                print("No data found.")

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")