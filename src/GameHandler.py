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
        self.client = Client()
        self.graph_algo = GraphAlgo()
        self.agents: dict[int, Agent] = {}
        self.parsed_pokemons: dict[tuple[float, float, int], Pokemon] = {}
        self.agents_map: dict[Agent, list] = {}

    def update_agents(self):
        try:
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
        except Exception as e:
            print(f"Bad agents Json from Server {e}")

    def create_agents(self, num_of_agents):
        payload = {}
        print(f"Initialising {num_of_agents} agents")
        for num in range(num_of_agents):
            start_pos = self.get_graph().get_node(num).get_pos().get_as_tuple()
            # the id in the payload is the id of the start node of the pokemon
            payload["id"] = num
            new_agent = Agent(num)
            self.agents[num] = new_agent
            self.agents_map[new_agent] = []
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
            self.add_pokemons()

        except Exception as e:
            print(f"Couldn't parse game info : {e}")

    def add_pokemons(self):
        try:
            pokemon_json = json.loads(self.client.get_pokemons())
            pokemon_json = pokemon_json.get("Pokemons", [])
            if pokemon_json is []:
                raise ValueError("Bad JSON")
            for pok in pokemon_json:
                curr_pok = pok.get("Pokemon")
                new_pokemon = Pokemon(curr_pok.get("value"), curr_pok.get("type"), curr_pok.get("pos"))
                self.parsed_pokemons[new_pokemon.get_identifier()] = new_pokemon
        except Exception as e:
            print(f"Couldn't parse pokemons : {e}")

    def update_pokemons(self):
        try:
            updated_pokemons = {}
            pokemon_json = json.loads(self.client.get_pokemons())
            pokemon_json = pokemon_json.get("Pokemons", [])
            if pokemon_json is []:
                raise ValueError("Bad JSON")
            for pok in pokemon_json:
                curr_poke = pok.get("Pokemon")
                new_pokemon = Pokemon(curr_poke.get("value"), curr_poke.get("type"), curr_poke.get("pos"))
                identifier = new_pokemon.get_identifier()
                if self.parsed_pokemons.get(identifier, None) is not None:
                    updated_pokemons[identifier] = self.parsed_pokemons.get(identifier)
                else:
                    updated_pokemons[identifier] = new_pokemon

            self.parsed_pokemons = updated_pokemons
        except Exception as e:
            print(f"Couldn't parse pokemons : {e}")

    def init_connection(self):
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

    def calculate_fastest_path(self, pokemon: Pokemon):
        chosen_agent = None
        path_dist: float = None
        min_load_factor = float('inf')
        fastest_path: list = []
        chosen_edge = self.get_edge_path(pokemon)
        for agent in self.agents.values():
            if len(self.agents_map.get(agent, [])) == 0:
                dist, curr_path = self.graph_algo.shortest_path(agent.src, chosen_edge.get_src())
                if chosen_edge.get_dest() not in curr_path:
                    curr_path.append(chosen_edge.get_dest())
                    dist += chosen_edge.get_weight()
                curr_load_factor = agent.calculate_load_factor(dist)
                if curr_load_factor < min_load_factor:
                    min_load_factor = curr_load_factor
                    fastest_path = curr_path
                    chosen_agent = agent
                    path_dist = dist
        if chosen_agent is not None:
            chosen_agent.update_load_factor(path_dist)
            self.agents_map[chosen_agent] = fastest_path

    def get_edge_path(self, pokemon) -> (GraphEdge, int, int):
        chosen_edge: GraphEdge = None
        for edge in self.get_graph().get_parsed_edges():
            src_node, dest_node = self.get_graph().get_node(edge.get_src()), self.get_graph().get_node(edge.get_dest())
            if pokemon.is_between(src_node, dest_node):
                min_id, max_id = min(edge.get_src(), edge.get_dest()), max(edge.get_src(), edge.get_dest())
                if pokemon.get_type() == -1:
                    chosen_edge = self.get_graph().get_edge(min_id, max_id)
                else:
                    chosen_edge = self.get_graph().get_edge(max_id, min_id)
                break
        if chosen_edge is None:
            raise ValueError
        return chosen_edge

    def choose_next_edge(self):
        for agent, path in self.agents_map.items():
            if agent.dest == -1 and len(path) > 0:
                kus_rabak = {"agent_id": agent._id, "next_node_id": path.pop(0)}
                self.client.choose_next_edge(json.dumps(kus_rabak))
        self.client.move()
