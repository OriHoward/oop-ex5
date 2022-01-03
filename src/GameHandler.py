from GraphAlgo import GraphAlgo
from agent import Agent
from client import Client
import os
import json


class GameHandler:

    def __init__(self):
        self.client = None
        self.graph_algo = GraphAlgo()
        self.agents: [Agent] = []

    def create_agents(self, num_of_agents):
        payload = {}
        for num in range(num_of_agents):
            self.agents.append(Agent(num))
            payload["id"] = num
            self.client.add_agent(json.dumps(payload))

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
