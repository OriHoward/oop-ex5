from GraphAlgo import GraphAlgo
from GraphEdge import GraphEdge
from agent import Agent
from client import Client
import os
import json
from Position import Position
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

    def calculate_fastest_path(self, pokemon: Pokemon) -> (Agent, list):
        chosen_agent = None
        path_dist: float = None
        min_load_factor = float('inf')
        fastest_path: list = []
        chosen_edge, src, dest = self.get_edge_path(pokemon)
        for agent in self.agents.values():
            dist, curr_path = self.graph_algo.shortest_path(agent.src, src)
            curr_path.append(dest)
            dist += chosen_edge.get_weight()
            curr_load_factor = agent.calculate_load_factor(dist)
            if curr_load_factor < min_load_factor:
                min_load_factor = curr_load_factor
                fastest_path = curr_path
                chosen_agent = agent
                path_dist = dist
        chosen_agent.update_load_factor(path_dist)
        return chosen_agent, fastest_path

    def get_edge_path(self, pokemon) -> (GraphEdge, int, int):
        curr_dest: int = None
        chosen_edge: GraphEdge = None
        for edge in self.get_graph().get_parsed_edges():
            if Position.is_between(edge.get_src(), edge.get_dest(), pokemon.get_pos()):
                chosen_edge = edge
                if pokemon.get_type() == -1:
                    curr_dest = max(edge.get_src(), edge.get_dest())
                else:
                    curr_dest = min(edge.get_src(), edge.get_dest())
                break
        if chosen_edge is None:
            raise ValueError
        if curr_dest == chosen_edge.get_dest():
            return chosen_edge, chosen_edge.get_dest(), chosen_edge.get_src()
        else:
            return chosen_edge, chosen_edge.get_src(), chosen_edge.get_dest()

    def choose_next_edge(self):
        pass
