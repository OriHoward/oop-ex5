from GraphAlgo import GraphAlgo
from agent import Agent
from client import Client
import os
import json

from pokemon import Pokemon


class GameHandler:

    def __init__(self):
        self.client = None
        self.graph_algo = GraphAlgo()
        self.agents: dict[int, Agent] = {}
        self.parsed_pokemons: list[Pokemon] = []

    def update_agents(self):
        agents_info_dict = json.loads(self.client.get_agents())
        for agent_item in agents_info_dict.get("Agents", []):
            agent_info = agent_item.get("Agent")
            if agent_info is None:
                continue
            curr_agent = self.agents.get(agent_info.get('id'), None)
            if curr_agent is None:
                continue
            del agent_info["id"]
            curr_agent.update_agent(**agent_info)

    def create_agents(self, num_of_agents):
        payload = {}
        print(f"Initialising {num_of_agents} agents")
        for num in range(num_of_agents):
            start_pos = self.get_graph().get_node(num).get_pos().get_as_tuple()
            # the id in the payload is the id of the start node of the pokemon
            payload["id"] = num
            self.agents[num] = Agent(num)
            self.client.add_agent(json.dumps(payload))
        self.update_agents()

    def parse_game_info(self):
        try:
            game_info = json.loads(self.client.get_info())
            game_info = game_info.get("GameServer", None)
            if game_info is None:
                raise ValueError("Bad JSON")
            self.graph_algo.load_from_json(os.path.join("../", game_info.get("graph")))
            self.create_agents(game_info.get("agents", 0))

        except Exception as e:
            print(f"Couldn't parse game info : {e}")

    def add_pokemon(self):
        try:
            pokemon_json = json.loads(self.client.get_pokemons())
            pokemon_json = pokemon_json.get("Pokemons", [])
            if pokemon_json is []:
                raise ValueError("Bad JSON")
            for pok in pokemon_json:
                curr_pok = pok.get("Pokemon")
                value = curr_pok.get("value")
                _type = curr_pok.get("type")
                pos = curr_pok.get("pos")
                self.parsed_pokemons.append(Pokemon(value, _type, pos))
        except Exception as e:
            print(f"Couldn't parse pokemons : {e}")

    def init_connection(self):
        self.client = Client()
        self.client.start_connection(os.getenv("HOST"), int(os.getenv("PORT")))

    def get_client(self):
        return self.client

    def start_game(self):
        self.client.start()

    def get_graph(self):
        try:
            return self.graph_algo.get_graph()
        except Exception as e:
            print("error.. no graph was loaded from json")

    def is_running(self):
        return Client.is_running(self.client)
