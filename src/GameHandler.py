import json
import math
import os

from GraphAlgo import GraphAlgo
from agent import Agent
from client import Client
from pokemon import Pokemon


class GameHandler:

    def __init__(self):
        self.client = Client()
        self.graph_algo = GraphAlgo()
        self.agents: dict[int, Agent] = {}
        self.parsed_pokemons: dict[tuple[float, float, int], Pokemon] = {}

    """
        update each agent -  position/value /etc..
    """
    def update_agents(self, payload=None):
        try:
            if payload is None:
                agents_info_dict = json.loads(self.client.get_agents())
            else:
                agents_info_dict = json.loads(payload)
            if type(agents_info_dict) is not dict:
                return
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
    """
        Creates the agents by the given number from the server
    """
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
            self.client.add_agent(json.dumps(payload))
        self.update_agents()

    """
        Parsing all the game info from the server
        to load the graph and to create the right amount of agents and pokemons etc..
    """
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

    """
        Create the pokemons and updating them accordingly
    """
    def update_pokemons(self):
        try:
            updated_pokemons = {}
            pokemon_json = json.loads(self.client.get_pokemons())
            if type(pokemon_json) is not dict:
                return
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
        except:
            print(f"Couldn't parse pokemons")

    """
        Starts the connection
    """
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

    def get_agents(self):
        return self.agents

    def get_parsed_pokemons(self):
        return self.parsed_pokemons
    """
        Checks if the server is running
    """
    def is_running(self):
        return self.client.is_running()

    """
        The function finds for each agent according to different calculations
        the best path to catch a pokemon
    """

    def find_path(self):
        for agent in self.agents.values():
            min_load_factor = float('inf')
            dist_to_update = None
            min_path = None
            chosen_poke = None
            for poke in self.parsed_pokemons.values():
                if not poke.get_assigned() and len(agent.get_assigned_path()) == 0 and agent.get_dest() == -1:
                    if agent.get_src() == poke.get_edge().get_src():
                        dist, path = self.graph_algo.shortest_path(agent.get_src(), poke.get_edge().get_dest())
                    else:
                        dist, path = self.graph_algo.shortest_path(agent.get_src(), poke.get_edge().get_src())
                        path.append(poke.get_edge().get_dest())
                        dist += poke.get_edge().get_weight()
                    load_factor = agent.calculate_load_factor(dist)
                    if load_factor < min_load_factor and len(path) > 0:
                        min_load_factor = load_factor
                        min_path = path
                        chosen_poke = poke
                        dist_to_update = dist
            if chosen_poke is not None and len(agent.get_assigned_path()) == 0:
                agent.set_assigned_path(min_path)
                chosen_poke.set_assigned(True)
                agent.update_load_factor(dist_to_update)
                agent.set_curr_pokemon(chosen_poke)

    """
        For each pokemon we create this function adds the current edge the pokemon
        is 'sitting' on to its attributes
    """

    def set_pokemon_edge(self, pokemon):
        for edge in self.get_graph().get_parsed_edges():
            src_node, dest_node = self.get_graph().get_node(edge.get_src()), self.get_graph().get_node(edge.get_dest())
            if not pokemon.get_assigned() and pokemon.is_between(src_node, dest_node):
                min_id, max_id = min(edge.get_src(), edge.get_dest()), max(edge.get_src(), edge.get_dest())
                if pokemon.get_type() == -1:
                    chosen_edge = self.get_graph().get_edge(max_id, min_id)
                    pokemon.set_edge(chosen_edge)
                    pokemon.set_ratio(self.get_graph())
                else:
                    chosen_edge = self.get_graph().get_edge(min_id, max_id)
                    pokemon.set_edge(chosen_edge)
                    pokemon.set_ratio(self.get_graph())
                break

    """
        This function chooses the next edge the agent needs to move to.
        The next edge is taken from the path each agent has.
        It also calculates the right timing we need to move the agent to 
        catch a pokemon
    """

    def choose_next_edge(self, move_queue: list):
        payload_list = []
        for agent in self.agents.values():
            agent_path = agent.get_assigned_path()
            if agent.get_dest() == -1 and len(agent_path) > 0:
                new_dest = agent_path.pop(0)
                dist, _ = self.graph_algo.shortest_path(agent.get_src(), new_dest)
                current_time = float(self.client.time_to_end())
                time_to_pass = (dist / agent.get_speed()) * 1000
                next_move = math.floor(current_time - (time_to_pass)) if dist != float("inf") else 0
                if agent.get_src() != new_dest:
                    move_queue.append(next_move)
                    if not bool(agent_path):
                        poke = agent.get_pokemon()
                        move_queue.append(math.floor(current_time - (time_to_pass * poke.get_ratio())))
                payload = {"agent_id": agent.get_id(), "next_node_id": new_dest}
                payload_list.append(payload)

        if bool(payload_list):
            for payload in payload_list:
                self.client.choose_next_edge(json.dumps(payload))
