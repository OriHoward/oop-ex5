from dotenv import load_dotenv

from GameHandler import GameHandler

load_dotenv()


def main():
    game_handler = GameHandler()
    game_handler.init_connection()
    game_handler.parse_game_info()

    # pokemons = client.get_pokemons()
    # agents = client.get_agents()
    # graph_json = client.get_graph()
    #
    # print(client.is_running())
    # print(client.time_to_end())
    #
    # # only after the agents were added the start function actually starts the game
    # client.add_agent("{\"id\":0}")
    #
    # client.start()
    # while client.is_running() == 'true':
    #     print(client.get_info())
    #     print(client.is_running())
    #     print(agents)
    #     print(client.time_to_end())


if __name__ == '__main__':
    main()
