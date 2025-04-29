import json


class FileManager:
    @staticmethod
    def save_data(data, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f)
            print(f"✅ Data saved to {filename}")
        except Exception as e:
            print("❌ Error saving data:", e)

    @staticmethod
    def load_data(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"🆕 {filename} not found. Starting fresh.")
            return {}
        except Exception as e:
            print("❌ Error loading data:", e)
            return {}