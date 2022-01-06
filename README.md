# oop-ex5

## how to we run the code ?

The command below executes the simulation, `stage number` should be replaces with a number between 0 and 15

```shell
pip install -r requirements.txt
java -jar Ex4_Server_v0.0.jar <stage number>
python src/main.py
```

## Contributors

Eitan Kats, Adi Yafe, Ori Howard

## Game details

in this assigment we were asked to create a Pokémon game, the game is displayed on a directed graph and has 16 levels (
0- 15).   
each level has a different number of agents and Pokémons.

The algorithms that were used in this are:

[dikstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

### Each Pokémon has

value - the value of the Pokémon  
type - the type of the Pokémon indicates the direction of the edge the pokemon is 'sitting' on  
position - the position of the Pokémon on the graph

### Each agent has

id - the id of the agent  
value - the score of the agent (getting higher each Pokémon he catches)  
src - the source of the agent dest - the destination of the agent. if there is no dest then -1   
speed - the speed of the agent  
position - representing the position of the agent

### The main goal of the game

The main goal is to navigate the agents in the directed graph in the fastest way to catch as many Pokémons as they
can.  
Each Pokémon has a different value and each agent that catches a Pokémon gaining that value.  
every level contains a specific graph, number of agents and Pokémons.

## Game Design

The 'brain' of the game is the `GameHanlder` which decorates the client module that communicates with the server.  
The first thing we do is fetching the information about the current level from the server.

1) We parse the Pokémon
    1) we send a request to the server to get the json that represents the Pokémon and we assign each Pokémon to the
       corresponding edge.
    2) after we find the edge we calculate the estimated location of the Pokémon on the edge (ratio)
2) We take the amount of agents that participate in the current level, and we assign each Pokémon by its value.

The `GameUI` class is responsible for drawing all the objects and scaling them.

1) We create the game proportions using the nodes of the graph.
2) Each object that we draw is being sent to a scaling function which scales it according to the proportions.

### The Game Loop

While the game is still running we are fetching information about the agents and Pokémon. The algorithm is trying to
find the optimal Pokémon for each agent with respect to the agent's speed and the amount of load on that agent. We only
assign Pokémon that are not already being chased by other agents. Each iteration of the game loop we tell the agents
that are free and have a task to perform to add the call time for the next `move` call which means pushing a timestamp
to the render queue, This is being calculated using the agent's speed at the current time and with respect to the
current game time.

For Example:

if we are currently in T1 and it takes 2 seconds for the agent to pass the current edge according to its parameters,
then the next render time will be T1-2.

on the last "hop" that the agent performs we are pushing 2 time stamps to the render queue one is the timestamp to catch
Pokémon and the 2nd one is to hop to the next node. the calculation of the render time for the Pokémon catch is with
respect to the ratio of the Pokémon on the edge

## Idea of Implementation

#### We choose to represent the graph:

1. nodeMap - this is a hashmap which contains all the nodes of the graph, the key is the id of the node and the value is
   the node itself
2. parsedEdges - this is a list of the edges that are in the graph

#### Each node comprises the following:

1. pos - location of the graph node
2. id - the id of the node
3. weight - the weight of the node
4. destMap - a hashmap that maps between the nodes that this node can reach and the edges that reach them
5. sourceMap - a hashmap that maps between a node and the sources that can each is

#### Each edge comprises the following:

1. source - the id of the source node
2. dest - the id of the dest node
3. weight - the weight of the edge

## Class overview

### DiGraph

The DiGraph is used to hold the graph that is that represents the current scenario.

This graph is a directed weighted graph

### GraphAlgo

Graph Algo contains the implementation of Dijkstra (from ex-3) and additional code that loads the graph from a given
file

### GraphEdge

An object representing an edge in the graph.

### GraphNode

An object representing a node in the graph.

### Agent

This is a class that represents the agents that need to chase the Pokémon that spawn on the graph

### Pokémon

This is a class that represents the Pokémon that are spread out on the graph

### Position

An object representing the location of the an object that we draw on the screen.

This class also knows how to scale the object according to given proportions

### GameHandler

The `GameHandler` is an implementation of the Decorator Design pattern, we Decorate the client and use the GameHandler
to communicate with the server.

The GameHandler also has the main algorithms that are being executed in the game loop

### GameUI

The `GameUI` class is used to draw objects that participate in the game onto the screen.

The game proportions are being calculated here using the proportions of the graph, objects that are being drawn onto the
screen are scaled here aswell

### Drawable

This is an abstract class that represents a drawable object that has a positions and an icon, mainly used to draw the
agents and Pokémon

## Detailed Execution Details of the Algorithms

## UML

![](./misc/UML.png)

Icons were taken from : https://flaticon.com