import requests


class Client:
    def __init__(self, base_url, mode='data'):
        self.base_url = base_url
        self.mode = mode

    def add_data(self, key, value):
        response = requests.put(f"{self.base_url}/{self.mode}/{key}", json={"value": value})
        # print(f"PUT {self.base_url}/{key} {value}")
        # return response.json()
        return response.json()['message']

    def get_data(self, key):
        response = requests.get(f"{self.base_url}/{self.mode}/{key}")
        print(f"{self.base_url}/{key}")
        return response.json()['value']


if __name__ == '__main__':
    client = Client("http://localhost:8000", mode='data2')
    print(client.add_data("key1", "value1"))
    print(client.add_data("key2", "value2"))
    print(client.get_data("key1"))
