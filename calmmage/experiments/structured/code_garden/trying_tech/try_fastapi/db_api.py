from db_client import Client


class CLI:
    def __init__(self, client: Client):
        self.client = client

    def process_message(self, message: str):
        parts = message.split(maxsplit=2)
        if len(parts) == 2 and parts[0] == '/get':
            key = parts[1]
            result = client.get_data(key)
            return result
        elif len(parts) == 3 and parts[0] == '/add':
            key = parts[1]
            value = parts[2]
            result = client.add_data(key, value)
            return result
        else:
            return "Invalid command. Try again."

    def run(self):
        while True:
            user_input = input("Enter a command (e.g. '/add key value' or '/get key'): ")
            response = self.process_message(user_input)
            print(response)


if __name__ == '__main__':
    client = Client("http://localhost:8000")
    cli = CLI(client)
    cli.run()
