from client import Client
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    client = Client()
    client.start_connection(os.getenv("HOST"), int(os.getenv("PORT")))
    pokemons = client.get_pokemons()
    client.get_agents()
    graph_json = client.get_graph()
    client.start()
    print(pokemons)


if __name__ == '__main__':
    main()
