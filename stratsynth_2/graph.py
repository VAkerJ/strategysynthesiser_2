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

        #nya
        #locdict går efter agent sedan state
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
        new_vert = Vertex(vert)
        self.int_vert_dict[vert] = new_vert
        self.int_invert_dict[vert] = Vertex(vert)

    def add_edge(self, current_vert, next_vert, action):
        """
        Creates an action-labeled transition between two nodes.

        :param current_vert: current node
        :param next_vert: node to connect to
        :param action: action that transitions to connected node
        :return:
        """
        self.vert_dict[current_vert].add_adjacent_vert(self.vert_dict[next_vert], action)
        self.invert_dict[next_vert].add_adjacent_vert(self.invert_dict[current_vert], action)

    def add_int_edge(self, current_vert, next_vert, action):
        self.int_vert_dict[current_vert].add_adjacent_vert(self.int_vert_dict[next_vert], action)
        self.int_invert_dict[next_vert].add_adjacent_vert(self.int_invert_dict[current_vert], action)

    def get_graph(self):
        """
        :return: the game graph as a dictionary.
        """
        return self.vert_dict

    def get_int_graph(self):
        return self.int_vert_dict

    def get_inv_graph(self):
        """
        :return: the inverted game graph as a dictionary.
        """
        return self.invert_dict

    def get_int_inv_graph(self):
        return self.int_invert_dict

    def get_loc(self):
        return self.locdict.values()

    def get_locdict(self):
        return self.locdict
    
    def get_to_int_locdict(self):
        return self.to_int_locdict

    def get_agents(self):
        return self.agents

    def get_to_str_dict(self):
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

        :return: returns a dictionary with the locations and their relevant number in the .dot file.
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
                        if ids not in self.to_int_locdict:
                            self.to_int_locdict[ids] = {}
                            self.to_str_locdict[ids] = {}
                            self.agents.append(Graph(self.filename))
                        if s not in self.to_int_locdict[ids]:
                            self.to_int_locdict[ids][s] = len(self.to_int_locdict[ids])
                            self.to_str_locdict[ids][self.to_int_locdict[ids][s]] = s
                            self.agents[ids].add_int_vert(self.to_int_locdict[ids][s])
                        
                        xs.append(self.to_int_locdict[ids][s])
                    xs = tuple(xs)



                    self.locdict[int(x[0])] = x[1]
                    self.int_locdict[int(x[0])] = xs
                    self.add_vert(x[1])
                    self.add_int_vert(xs)

                else:
                    break

            except Exception as e:
                print("hssasasa")
                print(e)
                break

        return i, strfile

    def deltaDic(self):
        """
        Uses the location dictionary to parse the .dot file into the action-labeled transitions for the coalition game

        :return: Returns the action-labeled transitions as a dictionary
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
                        rawAction = re.findall('label=\"\(*\((.*)\)', line)[0]
                        actions = re.split('\), \(', rawAction)
                        actions = [tuple(re.split(', ', a)) for a in actions]

                        rawAction_complete = re.findall('action=\"\(*\(\'([^\"]*)\'\)', line)[0] #ifall man vill ignorera '-'
                        actions_complete = re.split('\'\), \(\'', rawAction_complete)
                        actions_complete = [tuple(re.split('\', \'', a)) for a in actions_complete]
                        
                        if len(actions[0]) == 1: actions[0] = actions[0]*len(self.agents)
                        if len(actions_complete[0]) == 1: actions_complete[0] = actions_complete[0]*len(self.agents)

                    except:
                        actions = re.search('label=\"\((\-)', line).group(1)[0]
                        actions_complete = re.search('action=\"\((\-)', line).group(1)[0]

                    nr_of_actions = len(actions)
                    actions.extend(actions_complete)
                    int_actions = []
                    agent_actions = [[] for a in self.agents]
                    print(actions)
                    for idc, action in enumerate(actions):
                        for ida, act in enumerate(action):
                            if ida not in self.to_int_actdict:
                                self.to_int_actdict[ida] = {}
                                self.to_str_actdict[ida] = {}
                            if act not in self.to_int_actdict[ida]:
                                self.to_int_actdict[ida][act] = len(self.to_int_actdict[ida])
                                self.to_str_actdict[ida][self.to_int_actdict[ida][act]] = act

                            if idc < nr_of_actions:
                                print(act)
                                agent_actions[ida].append(self.to_int_actdict[ida][act])
                        
                        int_actions.append(tuple([self.to_int_actdict[ida][a] for ida, a in enumerate(action)]))
                    
                    for ida, a in enumerate(agent_actions):
                        if self.int_locdict[nodes[0]][ida] != self.int_locdict[nodes[1]][ida]:
                            self.agents[ida].add_int_edge(self.int_locdict[nodes[0]][ida], self.int_locdict[nodes[1]][ida], list(set(a)))

                    actions = list(set(actions))
                    self.add_edge(self.locdict[nodes[0]], self.locdict[nodes[1]], actions)
                    self.add_int_edge(self.int_locdict[nodes[0]], self.int_locdict[nodes[1]], int_actions)

            except Exception as e:
                pass