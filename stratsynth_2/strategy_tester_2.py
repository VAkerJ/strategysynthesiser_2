from .graph import *
from copy import deepcopy
from numpy import array
from itertools import product
from .Agent_strat_synth import *

class Coalition_strat_synth():

    def __init__(self, gamename, win_nodes=[("win", "win")], lose_nodes=[("lose", "lose")], start_nodes=[("start", "start")], goal="find_one", nr_of_strats=1, method = "backwards"):
        """
        param gamename: the name of the .dot file from which the game should be taken.
        param win_nodes: a list of all the nodes in the coaltion games which should be considered a win, where these nodes are tuples of the agents states in that game-state.
        param lose_nodes: a list of all the nodes in the coaltion games which should be considered a loss, where these nodes are tuples of the agents states in that game-state.
        param start_nodes: a list of all the nodes in the coaltion games from which the game may start, where these nodes are tuples of the agents states in that game-state.
        param goal: what task the class should strive to complete
        param nr_of_strats: how many strategies the class should attempt to find if using the 'find_n' goal
        param method: what algorithm the class should use to find strategies for in the agents games
        """
        self.game = None
        self.agent_graphs = None
        self.filename = gamename
        self.win_nodes = win_nodes
        self.lose_nodes = lose_nodes
        self.start_nodes = start_nodes
        self.agents = []
        self.strats = {}

        self.goals = ["find_one", "find_one_sw", "find_all", "find_n"]
        nr_of_strats = int(nr_of_strats)
        try:
            nr_of_strats = int(nr_of_strats)
        except:
            nr_of_strats = 0

        if goal not in self.goals or nr_of_strats < 1:
            print("Invalid goal, using 'find_one'\n")
            goal = "find_one"
            nr_of_strats = 1 
        self.nr_of_strats = nr_of_strats
        self.goal = goal

        self.nr_of_agents = None
        self.done = False
        self.nr_of_w = 0
        self.nr_of_sw = 0

        if method.lower() == "b":
            self.Agent_strat_synth = Backwards_strat_synth
        elif method.lower() == "f":
            self.Agent_strat_synth = Forwards_strat_synth
        elif method.lower() == "bp":
            self.Agent_strat_synth = Backwards_partial_synth
        elif method.lower() == "fp":
            self.Agent_strat_synth = Forwards_partial_synth
        else:
            print("Invalid method, using default")
            self.Agent_strat_synth = Backwards_strat_synth


    def start_test(self):
        """
        Starts by testing if the win lose and start nodes are valid, then attempts to find achieve the goal and prints the synthesied strategies when finished.
        """

        test = Game_graph(self.filename)
        test.deltaDic()
        
        self.game = test.get_int_graph()
        self.agent_graphs = test.get_agents()
        self.to_str = test.get_to_str_dict()
        self.nr_of_agents = len(test.agents)

        temp = test.get_to_int_locdict()

        self.win_nodes = self.test_nodes(temp, self.win_nodes, "win_nodes")
        self.lose_nodes = self.test_nodes(temp, self.lose_nodes, "lose_nodes")
        self.start_nodes = self.test_nodes(temp, self.start_nodes, "start_nodes")

        if not(self.win_nodes) or not(self.start_nodes):
            if not(self.win_nodes): print("Insufficient win_nodes")
            if not(self.start_nodes): print("Insufficient start_nodes")
            print("Terminating")
        else:
            self.find_strategy()
            self.print_strats()

    def test_nodes(self, dic, nodes, name):
        """
        tests the given nodes to see if they are valid, and if so, converts them to integers, if note, removes them from the set
        param dic: dictionary that converts nodes from string to integers
        param nodes: the nodes to be tested
        param name: the type of nodes given
        
        return: the set of valid nodes in integer form
        """
        remove = []
        for node in nodes:
            for idn, n in enumerate(node):
                if n not in dic[idn]:
                    remove.append(node)

        remove = set(remove)
        if remove: print(str(remove) + " are invalid nodes, removing from '" + name + "'\n")
        nodes = [tuple([dic[idn][n] for idn, n in enumerate(node)]) for node in nodes if node not in remove]
        return nodes


    def find_strategy(self):
        """
        Generates an initial strategy for each agent and then tests this profile of strategies on the coalition game.
        If the task/goal is no complete new strategeis are generated and tested incrementally until it is, or no new strategies can be generated.
        The winning strategies are then printed
        """

        win_n = array(self.win_nodes).T
        lose_n = array(self.lose_nodes).T
        start_n = array(self.start_nodes).T
        if len(lose_n) == 0: lose_n = [[None]]*self.nr_of_agents

        for n in range(self.nr_of_agents):
        
            if self.Agent_strat_synth.is_inv(): graph = self.agent_graphs[n].get_int_inv_graph()
            else: graph = self.agent_graphs[n].get_int_graph()

            new_agent = self.Agent_strat_synth(graph, set(win_n[n]), set(lose_n[n]), set(start_n[n]), n)
            new_agent.generate_main_partial()
            self.agents.append(new_agent)

        if self.goal == self.goals[2]: self.find_all_strats(self.agents) # find all
        else:
            self.test_strats(self.agents[0].partials, 0) #testing strats for agent[0] against all others
            self.find_some_strats(self.agents)
        

    def find_some_strats(self, agents):
        """
        Takes the already generated strategeis for an agent and generates new ones, then tests these new ones in combinations with the other agents
        previously excisting strategies.
        
        param agents: The objects containing the agents and their already generated strategies.
        """
        while not self.done:
            for agent in agents:
                partials, empty = agent.generate_new_partials()

                if partials: self.test_strats(partials, agent.id)

                if empty:
                    agents = [a for a in agents if a is not agent]
                    if not(agents): self.done = True
                
                if self.done: break

    def find_all_strats(self, agents):
        """
        Generates all possible strategies for alla agents, and then tests all of them att the same time.
        
        param agents: The objects containing the agents and their already generated strategies.
        """
        for agent in agents:
            empty = agent.is_empty()
            while not empty :
                empty = agent.generate_new_partials()[1]

        self.test_strats()


    def test_strats(self, partials=[], agent_id=-1):
        """
        Tests all possible new profiles of strategies on the coalition game
        
        param partials: the newly generated strategies for one agent
        param agent_id: the ID of the agent for which the newly generated strategies belong
        """
        p_list = [[]]*self.nr_of_agents

        if partials: p_list[agent_id] = partials

        for ida, agent in enumerate(self.agents):
                if ida != agent_id: p_list[ida] = agent.partials

        strats = product(*p_list)
        for strat in strats: self.test_strat(strat)

        return 

    def test_strat(self, strat):
        """
        Traverses the coalition game using the given strategy and saves it as having won if it can reach a win_node and saves it as having lost if it can reach
        a lose_node or possibly loop.
        
        NOTE: The algorithm does not consider splitting paths as different paths in the game. So it wrongly classifies games as having lost if a path splits and
        the joins a different path.
        
        param strat: the agents profile of strategies that is to be tested
        """
        for start in self.start_nodes:
            won = False
            lost = False

            action = tuple([strat[ids][state] for ids, state in enumerate(start)])
            adjacent = self.game[start].get_adjacent_vert()

            node_queue = [node for node in adjacent if action in self.game[start].get_actions(node)]
            checked = deepcopy(node_queue)
            
            while node_queue:
                node = node_queue.pop().get_id()
                
                if node in self.win_nodes:
                    won = True
                    continue

                try:
                    action = tuple([strat[ids][state] for ids, state in enumerate(node)])
                except:
                    lost = True
                    continue

                if node in self.lose_nodes:
                    lost = True
                    continue

                
                adjacent = [a for a in self.game[node].get_adjacent_vert() if action in self.game[node].get_actions(a)]

                new_adj = [a for a in adjacent if a not in checked]

                if new_adj != adjacent:
                    lost = True

                for n in new_adj:
                    node_queue.append(n)
                    checked.append(n)
            
            if won:
                self.add_strat(start, strat, lost)
                if self.check_criterion(): return
        return

    def add_strat(self, start, strat, lost):
        """
        Adds a strategy to the list of winning strategies.
        
        param start: What node the strategy starts from
        param strat: the strategy
        param lost: if the strategy may lose
        """
        strat, start = self.translate_strat(strat, start)
        if start not in self.strats: self.strats.update({start : {"surely winning" : [], "winning" : []}})

        if lost:
            self.strats[start]["winning"].append(strat)
            self.nr_of_w += 1

        else:
            self.strats[start]["surely winning"].append(strat)
            self.nr_of_sw += 1


    def translate_strat(self, strat, start):
        """
        Converts the strat from being in the integer fromat to being represented by strings
        
        param strat: the strategy to be converted
        param start: the starting node in the strategy
        
        return: the converted strategy and start node
        """
        strat = tuple([{self.to_str[0][ida][state]:self.to_str[1][ida][action] for state, action in S.items()} for ida, S in enumerate(strat)])
        start = tuple([self.to_str[0][ida][state] for ida, state in enumerate(start)])
        return strat, start


    def print_strats(self):
        """
        An uggly but simple way of printing the winning strategies.
        """
        
        print("\nNumber of strategies found")
        print("Winning: " + str(self.nr_of_w) + ", Surely Winning: " + str(self.nr_of_sw))
        print("Total: " + str(self.nr_of_w + self.nr_of_sw))
        print("\nFor starting state")
        for start in self.strats.keys():
            print(str(start) + ":")
            categories = self.strats[start].keys()
            for cat in categories:
                cs = self.strats[start][cat]
                if cs != []:
                    print("\n" + cat + ":")
                    for ids, s in enumerate(cs):
                        S = ""
                        for ida, a in enumerate(s):
                            S += "Agent" + str(ida) + ": " + str(a) + " | "
                        print("strat" + str(ids) + ": " + str(S))
            print("-"*200)

    def check_criterion(self):
        """
        check if the goal has been achieved
        return: if the goal is achieved
        """
        if self.goal == self.goals[0] or self.goal == self.goals[3]: #find one or n
            self.done = bool(self.nr_of_w + self.nr_of_sw >= self.nr_of_strats)

        elif self.goal == self.goals[1]: #find one surely winning
            if self.nr_of_sw > 0: self.done = True

        return self.done
