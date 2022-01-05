from GraphAlgo import GraphAlgo
from GraphEdge import GraphEdge
from agent import Agent
from client import Client
import os
import json
from pokemon import Pokemon
import math


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
        # keep popping if there are pokemon left in the pokemon list otherwise just put the agent in the node == id
        sorted_pokes = sorted(self.parsed_pokemons.values(), key=lambda x: x.get_value(), reverse=True)
        for num in range(num_of_agents):
            new_agent = Agent(num)
            if bool(sorted_pokes):
                payload["id"] = sorted_pokes.pop(0).get_edge().get_src()

            else:
                payload["id"] = num
            new_agent.set_placement(payload.get("id"))
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
            self.update_pokemons()
            self.create_agents(game_info.get("agents", 0))
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
            min_load_factor = float('inf')
            dist_to_update = None
            min_path = None
            chosen_poke = None
            for poke in self.parsed_pokemons.values():
                if not poke.is_assigned and len(self.agents_map[agent]) == 0 and agent.dest == -1:
                    if agent.src == poke.get_edge().get_src():
                        dist, path = self.graph_algo.shortest_path(agent.src, poke.get_edge().get_dest())
                    else:
                        dist, path = self.graph_algo.shortest_path(agent.src, poke.get_edge().get_src())
                        path.append(poke.get_edge().get_dest())
                        dist += poke.get_edge().get_weight()
                    load_factor = agent.calculate_load_factor(dist)
                    if load_factor < min_load_factor and len(path) > 0:
                        min_load_factor = load_factor
                        min_path = path
                        chosen_poke = poke
                        dist_to_update = dist
            if chosen_poke is not None and len(self.agents_map[agent]) == 0:
                self.agents_map[agent] = min_path
                chosen_poke.set_assigned(True)
                agent.update_load_factor(dist_to_update)
                agent.set_curr_pokemon(chosen_poke)

    def set_pokemon_edge(self, pokemon):
        for edge in self.get_graph().get_parsed_edges():
            src_node, dest_node = self.get_graph().get_node(edge.get_src()), self.get_graph().get_node(edge.get_dest())
            if not pokemon.is_assigned and pokemon.is_between(src_node, dest_node):
                # print(pokemon)
                min_id, max_id = min(edge.get_src(), edge.get_dest()), max(edge.get_src(), edge.get_dest())
                if pokemon.get_type() == -1:
                    chosen_edge = self.get_graph().get_edge(max_id, min_id)
                    pokemon.set_edge(chosen_edge)
                else:
                    chosen_edge = self.get_graph().get_edge(min_id, max_id)
                    pokemon.set_edge(chosen_edge)
                break

    def choose_next_edge(self):
        payload_list = []
        for agent, path in self.agents_map.items():
            if agent.dest == -1 and len(path) > 0:
                new_dest = path.pop(0)
                dist, _ = self.graph_algo.shortest_path(agent.src, new_dest)
                if bool(path):
                    agent.set_refresh_interval(dist)

                payload = {"agent_id": agent._id, "next_node_id": new_dest}
                payload_list.append(payload)
        if bool(payload_list):
            for payload in payload_list:
                self.client.choose_next_edge(json.dumps(payload))
