from .vertex import Vertex
import re

class Graph():
    def __init__(self, filename):
        """
        :param filename: the name of the .dot file.
        """
        self.vert_dict = {}
        self.invert_dict = {}
        self.int_vert_dict = {}
        self.int_invert_dict = {}

        self.locdict = {}
        self.int_locdict = {}

        
        self.filename = filename

        #self.agents is a list of graphs for each agent in the coalition game
        #the following dictionaries use the ID of each agent as a key to return each agents respective dictionary
        self.agents = []
        self.to_int_locdict = {}
        self.to_str_locdict = {}
        self.to_int_actdict = {}
        self.to_str_actdict = {}

    def add_vert(self, vert):
        """
        :param vert: label of node.
        :return: adds a new Vertex object to the game graphs vert_dict with the node label as key.
        """
        new_vert = Vertex(vert)
        self.vert_dict[vert] = new_vert
        self.invert_dict[vert] = Vertex(vert)

    def add_int_vert(self, vert):
        """
        :param vert: label of node.
        :return: adds a new Vertex object to the game graphs int_vert_dict with the node label in integer form as key.
        """
        new_vert = Vertex(vert)
        self.int_vert_dict[vert] = new_vert
        self.int_invert_dict[vert] = Vertex(vert)

    def add_edge(self, current_vert, next_vert, action):
        """
        Creates an action-labeled transition between two nodes using strings as labels.

        :param current_vert: current node
        :param next_vert: node to connect to
        :param action: action that transitions to connected node
        :return:
        """
        self.vert_dict[current_vert].add_adjacent_vert(self.vert_dict[next_vert], action)
        self.invert_dict[next_vert].add_adjacent_vert(self.invert_dict[current_vert], action)

    def add_int_edge(self, current_vert, next_vert, action):
        """
        Creates an action-labeled transition between two nodes using integers as labels.

        :param current_vert: current node
        :param next_vert: node to connect to
        :param action: action that transitions to connected node
        :return:
        """
        self.int_vert_dict[current_vert].add_adjacent_vert(self.int_vert_dict[next_vert], action)
        self.int_invert_dict[next_vert].add_adjacent_vert(self.int_invert_dict[current_vert], action)

    def get_graph(self):
        """
        :return: the game graph in string form as a dictionary.
        """
        return self.vert_dict

    def get_int_graph(self):
        """
        :return: the game graph in integer form as a dictionary.
        """
        return self.int_vert_dict

    def get_inv_graph(self):
        """
        :return: the inverted game graph in string form as a dictionary.
        """
        return self.invert_dict

    def get_int_inv_graph(self):
        """
        :return: the inverted game graph in integer form as a dictionary.
        """
        return self.int_invert_dict

    def get_loc(self):
        """
        return: the graphs locations in string form
        """
        return self.locdict.values()

    def get_locdict(self):
        """
        return: the locations dictionary in string form
        """
        return self.locdict
    
    def get_to_int_locdict(self):
        """
        return: the locations dictionary in integer form
        """
        return self.to_int_locdict

    def get_agents(self):
        """
        return: the graphs in integer form for the respective agents
        """
        return self.agents

    def get_to_str_dict(self):
        """
        return: the dictionaries for converting the agebts locations and actions from integer to string
        """
        return self.to_str_locdict, self.to_str_actdict

class Game_graph(Graph):
    def __init__(self, filename):
        """
        :param filename: the name of the .dot file.
        """
        super().__init__(filename)

    def locDic(self):
        """
        Parses the locations in the .dot file from numbers to their pre-set labels.
        
        Initiates the graphs and dictionaries for the agents in the game.
        
        Creates a dictionary with the locations and their relevant number in the .dot file.
        
        Extracts the locations for the agents games.
        NOTE: If the main game is the expanded coalition game, what's extracted is the agents expanded projection
        of the coalition game, not the projection of the expanded coalition game.

        :return: returns the placement in the .dot file along with the opened file
        """
        i = 5
        f = open("pictures/" + self.filename + ".dot", "r")
        strfile = f.readlines()
        f.close()

        for line in strfile[i:]:

            try:
                x = [re.search(r'[a-zA-Z\d]+', line).group(0), re.findall(r'((?<=\{)[a-zA-Z\d,\s-]+(?=\}))+', line)]

                if x[0] != "hidden":
                    x[1] = tuple(x[1])
                    xs = []
                    for ids, s in enumerate(x[1]):
                        if ids not in self.to_int_locdict: #initiates the agents graphs and dictionaries
                            self.to_int_locdict[ids] = {}
                            self.to_str_locdict[ids] = {}
                            self.agents.append(Graph(self.filename))
                        if s not in self.to_int_locdict[ids]: # adds each seperate location to the agents graphs, if not already added
                            self.to_int_locdict[ids][s] = len(self.to_int_locdict[ids])
                            self.to_str_locdict[ids][self.to_int_locdict[ids][s]] = s
                            self.agents[ids].add_int_vert(self.to_int_locdict[ids][s])
                        
                        xs.append(self.to_int_locdict[ids][s]) #presents the location as a tuple of the agents perspective of the game-state in integer form
                    xs = tuple(xs)



                    self.locdict[int(x[0])] = x[1] #adds the state to the coalition game graph
                    self.int_locdict[int(x[0])] = xs
                    self.add_vert(x[1])
                    self.add_int_vert(xs)

                else:
                    break

            except Exception as e:
                print(e)
                break

        return i, strfile

    def deltaDic(self):
        """
        Uses the location dictionary to parse the .dot file into the action-labeled transitions for the coalition game
        and the transitions for the agents graphs extracted from the coalition game
        
        NOTE: transitions in the agents extractions that go to the same node are ignored, as this was used for memoryless strategy synthesis.
        See comments for where to modify this.
        
        NOTE: "-" denotes using 'any' action and are added to the agent's action alphabet when excisting in the coalition game. If they appear in a synthesised strategy,
        then the agent's action has node made any differance to the strategies outcome.
        """
        i, strfile = self.locDic()
        

        for line in strfile[i:]:

            try:
                search = re.search('arrowhead', line) or \
                         re.search('hidden', line) or \
                         re.search('}', line)

                if search is None:
                    nodes = [int(node) for node in re.findall('[\d]+', line)]

                    try:
                        rawAction = re.findall('label=\"\(*\((.*)\)', line)[0] # the actions, when allowing use of the '-' notation
                        actions = re.split('\), \(', rawAction)
                        actions = [tuple(re.split(', ', a)) for a in actions]

                        rawAction_complete = re.findall('action=\"\(*\(\'([^\"]*)\'\)', line)[0] # the actions, without using the '-' notation
                        actions_complete = re.split('\'\), \(\'', rawAction_complete)
                        actions_complete = [tuple(re.split('\', \'', a)) for a in actions_complete]
                        
                        if len(actions[0]) == 1: actions[0] = actions[0]*len(self.agents)
                        if len(actions_complete[0]) == 1: actions_complete[0] = actions_complete[0]*len(self.agents)

                    except:
                        actions = re.search('label=\"\((\-)', line).group(1)[0]
                        actions_complete = re.search('action=\"\((\-)', line).group(1)[0]

                    nr_of_actions = len(actions)
                    actions.extend(actions_complete) # combines the actions allowing for '-' and not
                    int_actions = []
                    agent_actions = [[] for a in self.agents]

                    for idc, action in enumerate(actions): # adds the actions to the agents verticies
                        for ida, act in enumerate(action):
                            if ida not in self.to_int_actdict:
                                self.to_int_actdict[ida] = {}
                                self.to_str_actdict[ida] = {}
                            if act not in self.to_int_actdict[ida]:
                                self.to_int_actdict[ida][act] = len(self.to_int_actdict[ida])
                                self.to_str_actdict[ida][self.to_int_actdict[ida][act]] = act

                            if idc < nr_of_actions: agent_actions[ida].append(self.to_int_actdict[ida][act]) # only add the actions allowing '-' to the agents action dictionary
                        
                        int_actions.append(tuple([self.to_int_actdict[ida][a] for ida, a in enumerate(action)])) # add both '-' and the individual actions to the game graphs
                    
                    for ida, a in enumerate(agent_actions): # adds the actions and verticeis to the agents graphs
                        if self.int_locdict[nodes[0]][ida] != self.int_locdict[nodes[1]][ida]: #remove to allow for vertecies in the agents game that go to from a node to itself
                            self.agents[ida].add_int_edge(self.int_locdict[nodes[0]][ida], self.int_locdict[nodes[1]][ida], list(set(a)))

                    actions = list(set(actions)) # adds the actions and verticies to the coalition game
                    self.add_edge(self.locdict[nodes[0]], self.locdict[nodes[1]], actions)
                    self.add_int_edge(self.int_locdict[nodes[0]], self.int_locdict[nodes[1]], int_actions)

            except Exception as e:
                pass
