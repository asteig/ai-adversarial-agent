from sample_players import DataPlayer
import math

_WIDTH = 11
_HEIGHT = 9
_SIZE = (_WIDTH + 2) * _HEIGHT - 2

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def score(self, state):

        """
        STRATEGY:
        - Player 1 mirrors the opponent's actions.
        - Player 2 steals liberties from Player 1
        - Against Greedy: steal a liberty
        """

        score = 0

        own_loc = state.locs[self.player_id]
        own_liberties = set(state.liberties(own_loc))
        own_x, own_y = self.ind2xy(own_loc)

        opp_loc = state.locs[1 - self.player_id]
        opp_liberties = set(state.liberties(opp_loc))

        shared_actions = own_liberties & opp_liberties
        actions = own_liberties - (opp_liberties - own_liberties)

        steal_liberties = own_liberties & opp_liberties

        # Mirror
        # if self.player_id == 0:
        #     if own_loc == 57 and opp_loc == None:
        #         return float('inf')

        #     if opp_loc and self.player_id == 0: 
        #         mirrors = self.get_mirrors(opp_loc)
        #         if own_loc in mirrors:
        #             return float('inf')


        # Always works for Greedy
        if len(shared_actions) > 0:
            score = score + len(shared_actions)
        else:
            score = score + len(actions) 
                    
        return score
        

    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        self.queue.put(max(state.actions(), key=lambda x: self.score(state.result(x))))

    
    def alpha_beta_search(self, state):
        """ Return the move along a branch of the game tree that
        has the best possible value.  A move is a pair of coordinates
        in (column, row) order corresponding to a legal move for
        the searching player.
        
        You can ignore the special case of calling this function
        from a terminal state.
        """
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        for a in state.actions():
            v = self.min_value(state.result(a), alpha, beta)
            alpha = max(alpha, v)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move

    def min_value(self, state, alpha, beta):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if state.terminal_test():
            return state.utility(0)
        
        v = float("inf")
        for a in state.actions():
            v = min(v, self.max_value(state.result(a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, state, alpha, beta):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if state.terminal_test():
            return state.utility(0)
        
        v = float("-inf")
        for a in state.actions():
            v = max(v, self.min_value(state.result(a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def ind2xy(self, index):
        return (index % (_WIDTH + 2), index // (_WIDTH + 2))

    def xy2ind(self, x, y): 
        return (y * (_WIDTH + 2) + x)

    def get_mirrors(self, ind):

        mirrors = []

        board_center_x = math.ceil(_WIDTH / 2)
        board_center_x = math.ceil(_WIDTH / 2)

        x, y = self.ind2xy(ind)

        mirror_x = _WIDTH - x - 1

        mirrors.append(self.xy2ind(mirror_x, y))

        mirror_y = _HEIGHT - y - 1

        mirrors.append(self.xy2ind(x, mirror_y))
        mirrors.append(self.xy2ind(mirror_x, mirror_y))

        return mirrors

    def distance_to_bounds(self, ind):

        x, y = (ind % (_WIDTH + 2), ind // (_WIDTH + 2))

        # Pythagorean theorem
        return math.sqrt(x**2 + y**2)


        

