from copy import deepcopy


class Backwards_strat_synth():
    """
    Uses a width first search from the win_nodes to a node in the start_nodes and saves the path traversed from an exhausted search as an initial strategy.
    NOTE: The actions saved to the strategy is the first action in the list of actions for the first vertex in the list of verticies for each node
    The remaining actions are w.r.t. each node, saved as values with the nodes as keys in the conflict_nodes dictionary.
    """

    def __init__(self, game_graph, win_nodes, lose_nodes, start_nodes, agent_id):
        """
        param game_graph: the graph for the agents game
        param win_nodes: the nodes wherein they agent considers the game won
        param lose_nodes: the nodes wherein they agent considers the game lost
        param start_nodes: the nodes from which the agent may start the game
        param agent_id: the id of the agent
        """
        self.win_nodes = win_nodes
        self.lose_nodes = lose_nodes
        self.start_nodes = start_nodes
        self.game = deepcopy(game_graph)
        self.id = agent_id
        self.partials = []
        self.conflict_nodes = {}

    @staticmethod
    def is_inv():
        """
        return: If the inverted graph should be used
        """
        return True

    def is_empty(self):
        """
        return: If no more strategies can be generated
        """
        return not(bool(self.conflict_nodes))

    def generate_main_partial(self):
        """
        Generates the initial strategy using the width first algorithm and saves the nodes conflicting with this strategy.
        """

        cn = self.conflict_nodes
        
        current_partial = {}
        checked = list(self.win_nodes)
        node_queue = deepcopy(checked)
        while node_queue:
            current_node = node_queue.pop()
            adjacent = self.game[current_node].get_adjacent_vert()

            for adj in adjacent:
                actions = self.game[current_node].get_actions(adj)
                act = actions.pop()
                adj = adj.get_id()

                if adj not in checked:
                    current_partial[adj] = act
                    checked.append(adj)
                    if adj not in self.start_nodes: node_queue.append(adj)
                
                elif act != current_partial[adj]:
                    if adj in cn and act not in cn[adj]: cn[adj].append(act)
                    elif adj not in cn: cn[adj] = [act]

                while actions:
                    act = actions.pop()
                    if act != current_partial[adj]:
                        if adj in cn and act not in cn[adj]: cn[adj].append(act)
                        elif adj not in cn: cn[adj] = [act]
        self.partials.append(current_partial)
        return

    def generate_new_partials(self):
        """
        Takes all excisting strategies and replaces the action in one node with one unused action from the conflict_nodes to create an equal amount of
        untested winning strategies.
        
        return: the new strategies, if no new strategies can be generated
        """
        cn = self.conflict_nodes
        try:
            node = next(iter(cn.keys()))
        except:
            return [], not(cn)

        action = cn[node].pop()

        if not(cn[node]): del cn[node]

        new_p = []
        partials = deepcopy(self.partials)
        for p in partials:
            p.update({node : action})
            new_p.append(p)

        self.partials.extend(new_p)
        return new_p, not(cn)

class Forwards_strat_synth():
    """
    Uses a width first search from the start_nodes to a node in the win_nodes and saves the path traversed from an exhausted search as an initial strategy.
    NOTE: The actions saved to the strategy is the first action in the list of actions for the first vertex in the list of verticies for each node
    The remaining actions are w.r.t. each node, saved as values with the nodes as keys in the conflict_nodes dictionary.
    """

    def __init__(self, game_graph, win_nodes, lose_nodes, start_nodes, agent_id):
        """
        param game_graph: the graph for the agents game
        param win_nodes: the nodes wherein they agent considers the game won
        param lose_nodes: the nodes wherein they agent considers the game lost
        param start_nodes: the nodes from which the agent may start the game
        param agent_id: the id of the agent
        """
        self.win_nodes = win_nodes
        self.lose_nodes = lose_nodes
        self.start_nodes = start_nodes
        self.game = deepcopy(game_graph)
        self.id = agent_id
        self.partials = []
        self.conflict_nodes = {}

    @staticmethod
    def is_inv():
        """
        return: If the inverted graph should be used
        """
        return False

    def is_empty(self):
        """
        return: If no more strategies can be generated
        """
        return not(bool(self.conflict_nodes))

    def generate_main_partial(self):
        """
        Generates the initial strategy using the width first algorithm and saves the nodes conflicting with this strategy.
        """

        cn = self.conflict_nodes
        
        current_partial = {}
        node_queue = deepcopy(list(self.start_nodes))
        checked = []
        while node_queue:
            current_node = node_queue.pop()
            checked.append(current_node)

            adjacent = self.game[current_node].get_adjacent_vert()      
            if not adjacent: continue

            adj = adjacent.pop()
            actions = deepcopy(self.game[current_node].get_actions(adj))
            
            current_act = actions.pop()
            current_partial[current_node] = current_act
            

            if adj.get_id() not in checked: node_queue.append(adj.get_id())
            if actions: cn[current_node] = deepcopy(actions)
            

            while adjacent:
                adj = adjacent.pop()
                
                actions = [a for a in self.game[current_node].get_actions(adj) if a != current_act]

                if current_node in cn and actions:
                    cn[current_node].extend([a for a in actions if a not in cn[current_node]])
                                
                elif actions: cn[current_node] = deepcopy(actions)
                if adj not in self.win_nodes:
                    if adj.get_id() not in checked: node_queue.append(adj.get_id())
        self.partials.append(current_partial)
        return

    def generate_new_partials(self):
        """
        Takes all excisting strategies and replaces the action in one node with one unused action from the conflict_nodes to create an equal amount of
        untested winning strategies.
        
        return: the new strategies, if no new strategies can be generated
        """
        cn = self.conflict_nodes
        try:
            node = next(iter(cn.keys()))
        except:
            return [], not(cn)

        action = cn[node].pop()

        if not(cn[node]): del cn[node]

        new_p = []
        partials = deepcopy(self.partials)
        for p in partials:
            p.update({node : action})
            new_p.append(p)

        self.partials.extend(new_p)
        return new_p, not(cn)

class Backwards_partial_synth():
    """
    Uses a width first search from the win_nodes to a node in the start_nodes and saves each possible path through the game as an initial strategy.
    NOTE: The actions saved to the strategy is the first action in the list of actions for the first vertex in the list of verticies for each node
    The remaining actions are w.r.t. each node and path, saved as values with the node and path as keys in the conflict_nodes dictionary.
    """

    def __init__(self, game_graph, win_nodes, lose_nodes, start_nodes, agent_id):
        """
        param game_graph: the graph for the agents game
        param win_nodes: the nodes wherein they agent considers the game won
        param lose_nodes: the nodes wherein they agent considers the game lost
        param start_nodes: the nodes from which the agent may start the game
        param agent_id: the id of the agent
        """
        self.win_nodes = win_nodes
        self.lose_nodes = lose_nodes
        self.start_nodes = start_nodes
        self.game = deepcopy(game_graph)
        self.id = agent_id
        self.partials = []
        self.conflict_nodes = {}

    @staticmethod
    def is_inv():
        """
        return: If the inverted graph should be used
        """
        return True

    def is_empty(self):
        """
        return: If no more strategies can be generated
        """
        return not(bool(self.conflict_nodes))

    def generate_main_partial(self):
        """
        Generates an initial partial strategy for each path through the game from each win_node to a node in start_nodes
        return: the partial strategies generated
        """
        
        for win_node in self.win_nodes:
            partial_id = len(self.partials)
            if partial_id == 0: self.partials.append({})
            self.traverse_game(win_node, partial_id)

        return self.partials

    def generate_new_partials(self):
        """
        Takes a partial strategy with conflict_nodes and creates all possible partial strategies from these conflict_nodes.
        
        return: the new strategies, if no new strategies can be generated
        """
        cn = self.conflict_nodes
        try:
            partial_id = next(iter(cn.keys()))
        except:
            return [], not(cn)

        conflicts = cn[partial_id]
        del cn[partial_id]

        new_p = []
        temp = []
        partials = [deepcopy(self.partials[partial_id])]

        for node, actions in conflicts:
            for act in actions:
                for p in partials:
                    p.update({node : act})
                
                temp.extend(deepcopy(partials))
            partials = [deepcopy(self.partials[partial_id])]
            new_p.extend(temp)
            partials.extend(deepcopy(new_p))
            temp = []

        self.partials.extend(new_p)
        return new_p, not(cn)

    def traverse_game(self, current_node, partial_id):
        """
        Traverses the game one step, generating a new path and id if the path through the game splits. Deleting the path if it reaches a dead end or a lose_node
        param current_node: the node from which one wishes to move
        param partial_id: the ID of the path through the game on which one is traversing
        """
        if current_node in self.start_nodes: return

        cn = self.conflict_nodes
        base_partial = deepcopy(self.partials[partial_id])
        if partial_id in cn:
            base_cn = deepcopy(cn[partial_id])
        else:
            base_cn = False
        
        adjacent = [a for a in self.game[current_node].get_adjacent_vert() if a.get_id() not in base_partial]
        if not adjacent:
            self.partials = [p for idp, p in enumerate(self.partials) if idp != partial_id]
            if partial_id in cn:  del cn[partial_id]
            return

        for ida, adj in enumerate(adjacent):
            actions = deepcopy(self.game[current_node].get_actions(adj))

            act = actions.pop()

            if ida != 0:
                partial_id = len(self.partials)
                self.partials.append(deepcopy(base_partial))
                if base_cn:
                    cn[partial_id] = deepcopy(base_cn)

            self.partials[partial_id][adj.get_id()] = act

            if partial_id not in cn and actions:
                cn[partial_id] = [(adj.get_id(), actions)]
            elif actions:
                cn[partial_id].append((adj.get_id(), actions))

            self.traverse_game(adj.get_id(), partial_id)


        return

class Forwards_partial_synth():
    """
    Uses a width first search from the start_nodes to a node in the win_nodes and saves each possible path through the game as an initial strategy.
    NOTE: The actions saved to the strategy is the first action in the list of actions for the first vertex in the list of verticies for each node
    The remaining actions are w.r.t. each node and path, saved as values with the node and path as keys in the conflict_nodes dictionary.
    """

    def __init__(self, game_graph, win_nodes, lose_nodes, start_nodes, agent_id):
        """
        param game_graph: the graph for the agents game
        param win_nodes: the nodes wherein they agent considers the game won
        param lose_nodes: the nodes wherein they agent considers the game lost
        param start_nodes: the nodes from which the agent may start the game
        param agent_id: the id of the agent
        """
        self.win_nodes = win_nodes
        self.lose_nodes = lose_nodes
        self.start_nodes = start_nodes
        self.game = deepcopy(game_graph)
        self.id = agent_id
        self.partials = []
        self.conflict_nodes = {}

    @staticmethod
    def is_inv():
        """
        return: If the inverted graph should be used
        """
        return False

    def is_empty(self):
        """
        return: If no more strategies can be generated
        """
        return not(bool(self.conflict_nodes))

    def generate_main_partial(self):
        """
        Generates an initial partial strategy for each path through the game from each win_node to a node in start_nodes
        return: the partial strategies generated
        """

        for start_node in self.start_nodes:
            partial_id = len(self.partials)
            if partial_id == 0: self.partials.append({})
            self.traverse_game(start_node, partial_id)

        return self.partials

    def generate_new_partials(self):
        """
        Takes a partial strategy with conflict_nodes and creates all possible partial strategies from these conflict_nodes.
        
        return: the new strategies, if no new strategies can be generated
        """
        cn = self.conflict_nodes
        try:
            partial_id = next(iter(cn.keys()))
        except:
            return [], not(cn)

        conflicts = cn[partial_id]
        del cn[partial_id]

        new_p = []
        temp = []
        partials = [deepcopy(self.partials[partial_id])]

        for node, actions in conflicts:
            for act in actions:
                for p in partials:
                    p.update({node : act})
                
                temp.extend(deepcopy(partials))
            partials = [deepcopy(self.partials[partial_id])]
            new_p.extend(temp)
            partials.extend(deepcopy(new_p))
            temp = []

        self.partials.extend(new_p)
        return new_p, not(cn)

    def traverse_game(self, current_node, partial_id):
        """
        Traverses the game one step, generating a new path and id if the path through the game splits. Deleting the path if it reaches a dead end or a lose_node
        param current_node: the node from which one wishes to move
        param partial_id: the ID of the path through the game on which one is traversing
        """
        if current_node in self.win_nodes: return

        cn = self.conflict_nodes
        base_partial = deepcopy(self.partials[partial_id])
        if partial_id in cn:
            base_cn = deepcopy(cn[partial_id])
        else:
            base_cn = False

        
        adjacent = [a for a in self.game[current_node].get_adjacent_vert() if a.get_id() not in base_partial]
        if not adjacent:
            self.partials = [p for idp, p in enumerate(self.partials) if idp != partial_id]
            if partial_id in cn:  del cn[partial_id]
            return


        for ida, adj in enumerate(adjacent):
            actions = deepcopy(self.game[current_node].get_actions(adj))

            act = actions.pop()

            if ida != 0:
                partial_id = len(self.partials)
                self.partials.append(deepcopy(base_partial))
                if base_cn:
                    cn[partial_id] = deepcopy(base_cn)

            self.partials[partial_id][current_node] = act

            if partial_id not in cn and actions:
                cn[partial_id] = [(current_node, actions)]
            elif actions:
                cn[partial_id].append((current_node, actions))

            self.traverse_game(adj.get_id(), partial_id)


        return
