from GraphAlgo import GraphAlgo
from GraphEdge import GraphEdge
from agent import Agent
from client import Client
import os
import json
from pokemon import Pokemon


class GameHandler:

    def __init__(self):
        self.client = Client()
        self.graph_algo = GraphAlgo()
        self.agents: dict[int, Agent] = {}
        self.parsed_pokemons: dict[tuple[float, float, int], Pokemon] = {}
        self.agents_map: dict[Agent, list] = {}

    def update_agents(self, payload=None):
        try:
            if payload is None:
                agents_info_dict = json.loads(self.client.get_agents())
            else:
                agents_info_dict = json.loads(payload)
            for agent_item in agents_info_dict.get("Agents", []):
                agent_info = agent_item.get("Agent", None)
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
        print(f"Initializing {num_of_agents} agents")
        for num in range(num_of_agents):
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
            self.update_pokemons()
        except Exception as e:
            print(f"Couldn't parse game info : {e}")

    def update_pokemons(self):
        try:
            updated_pokemons = {}
            pokemon_json = json.loads(self.client.get_pokemons())
            pokemon_json = pokemon_json.get("Pokemons", [])
            for pok in pokemon_json:
                curr_poke = pok.get("Pokemon")
                new_pokemon = Pokemon(curr_poke.get("value"), curr_poke.get("type"), curr_poke.get("pos"))
                identifier = new_pokemon.get_identifier()
                if self.parsed_pokemons.get(identifier, None) is not None:
                    updated_pokemons[identifier] = self.parsed_pokemons.get(identifier)
                else:
                    updated_pokemons[identifier] = new_pokemon
                    self.set_pokemon_edge(new_pokemon)
            self.parsed_pokemons = updated_pokemons
        except Exception as e:
            print(f"Couldn't parse pokemons: {e}")

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
            print(f"error.. no graph was loaded from json {e}")

    def is_running(self):
        return self.client.is_running()

    def find_path(self):
        """
        for a in agents
            min_dist = inf
            curr_poke = None
            for p in pokemons
                curr_poke = p
                if p is not assigned :(

                    dist, path = shortest path: a.src -> p.get_edge.src
                    path.append(p.get_edge.dest)
                    dist+=p.get_edge.w
        """
        for agent in self.agents.values():
            min_dist = float('inf')
            min_path = None
            chosen_poke = None
            for poke in self.parsed_pokemons.values():
                if not poke.is_assigned:
                    dist, path = self.graph_algo.shortest_path(agent.src, poke.get_edge().get_src())
                    print(agent.src, agent.dest)
                    if poke.get_edge().get_dest() not in path:
                        path.append(poke.get_edge().get_dest())
                        dist += poke.get_edge().get_weight()
                    if dist < min_dist and len(path) > 0:
                        min_dist = dist
                        min_path = path
                        chosen_poke = poke
            if chosen_poke is not None and len(self.agents_map[agent]) == 0:
                if poke.get_type() == -1:
                    min_path.append(poke.get_edge().get_src())
                self.agents_map[agent] = min_path
                chosen_poke.set_assigned(True)

    def set_pokemon_edge(self, pokemon):
        for edge in self.get_graph().get_parsed_edges():
            src_node, dest_node = self.get_graph().get_node(edge.get_src()), self.get_graph().get_node(edge.get_dest())
            if not pokemon.is_assigned and pokemon.is_between(src_node, dest_node):
                # print(pokemon)
                min_id, max_id = min(edge.get_src(), edge.get_dest()), max(edge.get_src(), edge.get_dest())
                if pokemon.get_type() == -1:
                    chosen_edge = self.get_graph().get_edge(min_id, max_id)
                    pokemon.set_edge(chosen_edge)
                else:
                    chosen_edge = self.get_graph().get_edge(max_id, min_id)
                    pokemon.set_edge(chosen_edge)
                break

    def choose_next_edge(self):
        payload_list = []
        for agent, path in self.agents_map.items():
            if agent.dest == -1 and len(path) > 0:
                new_dest = path.pop(0)
                dist, _ = self.graph_algo.shortest_path(agent.src, new_dest)
                agent.set_refresh_interval(dist)
                payload = {"agent_id": agent._id, "next_node_id": new_dest}
                payload_list.append(payload)
        if bool(payload_list):
            for payload in payload_list:
                self.client.choose_next_edge(json.dumps(payload))

    def calculate_fastest_path(self):
        chosen_agent = None
        chosen_poke = None
        path_dist: float = None
        chosen_dist: float = float('inf')
        min_load_factor = float('inf')
        fastest_path: list = []
        chosen_path: list = []
        for curr_pok in self.parsed_pokemons.values():
            chosen_edge = self.get_edge_path(curr_pok)
            if chosen_edge is not None:
                for agent in self.agents.values():
                    if len(self.agents_map.get(agent, [])) == 0:
                        dist, curr_path = self.graph_algo.shortest_path(agent.src, chosen_edge.get_src())
                        # if chosen_edge.get_dest() not in curr_path:
                        curr_path.append(chosen_edge.get_dest())
                        dist += chosen_edge.get_weight()
                        curr_load_factor = agent.calculate_load_factor(dist)
                        if curr_load_factor < min_load_factor:
                            min_load_factor = curr_load_factor
                            fastest_path = curr_path
                            chosen_agent = agent
                            path_dist = dist
                if chosen_agent is not None:
                    if path_dist < chosen_dist:
                        chosen_dist = path_dist
                        chosen_path = fastest_path
                        chosen_poke = curr_pok
        if len(chosen_path) > 0 and chosen_dist < float('inf'):
            chosen_agent.update_load_factor(chosen_dist)
            self.agents_map[chosen_agent] = chosen_path
            print(chosen_path, chosen_dist)
            chosen_poke.set_assigned(True)
