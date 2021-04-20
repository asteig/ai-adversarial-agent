# Adversarial Game Playing Agent

![Example game of isolation on a square board](viz.gif)

I created a custom player class that plays a version of Knight's isolation. During the completion of the project, I learned about advanced heuristics and opening book techniques that can be used to give the agent an advantage over its opponents. 

In this project, I experimented with different adversarial search techniques by building an agent to play knights Isolation. Unlike classic Isolation where players control tokens that move like chess queens, this version of Isolation gives each agent control over a single token that moves in L-shaped movements--like a knight in chess.

# My Custom Player
I created a custom player class to create an agent that can complete a game against itself and the agents provided as a baseline by the assignment. In the score function, I use a combination of techniques covered by the lectures to predict the best move for the agent to play next. Each method returns a value used to rank all possible moves against each other. With experimentation, I was able to find which methods worked well and which methods didn't work well at all.

## Remaining Liberties
```python
own_loc = state.locs[self.player_id]
own_liberties = set(state.liberties(own_loc))
own_x, own_y = self.ind2xy(own_loc)

opp_loc = state.locs[1 - self.player_id]
opp_liberties = set(state.liberties(opp_loc))

shared_actions = own_liberties & opp_liberties
actions = own_liberties - (opp_liberties - own_liberties)

steal_liberties = own_liberties & opp_liberties
```

## Mirroring
```python
if self.player_id == 0:
    if own_loc == 57 and opp_loc == None:
        return float('inf')

if opp_loc and self.player_id == 0: 
    mirrors = self.get_mirrors(opp_loc)
    
if own_loc in mirrors:
    return float('inf')
```
## Greedy 

```python
if len(shared_actions) > 0:
  score = score + len(shared_actions)
else:
  score = score + len(actions) 

return score
```

## Alpha Beta Search
Return the move along a branch of the game tree that has 
the best possible value.  A move is a pair of coordinates
in (column, row) order corresponding to a legal move for
the searching player.

```python    
def alpha_beta_search(self, state):
    
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
```

## min_value
Return the value for a win (+1) if the game is over,
otherwise return the minimum value over all legal child
nodes.

```python
def min_value(self, state, alpha, beta):

    if state.terminal_test():
        return state.utility(0)
    
    v = float("inf")
    for a in state.actions():
        v = min(v, self.max_value(state.result(a), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
```

## max_value
Return the value for a loss (-1) if the game is over,
otherwise return the maximum value over all legal child nodes.

```python
def max_value(self, state, alpha, beta):

    if state.terminal_test():
        return state.utility(0)
    
    v = float("-inf")
    for a in state.actions():
        v = max(v, self.min_value(state.result(a), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v
```

## Experiment Results

Part of my assignment was to test the effectiveness of my search techniques against the provided agents. Each agent uses a strategy covered in class to try and win the game. My task was to find additional strategies that would ultimately win the game, or determine why those strategies are ineffective.

Below is a table showing the average % win after 1000 games played, once as Player 1 and once as Player 2. My agent was particularly effective when playing against the GREEDY algorithm by choosing moves that reduce the amount of moves available to the opponent. My solution also did well playing against the agent using random moves, winning 82.6% as Player 1 and 79.3% as Player 2.

|               | Player 1      | Player 2  |
| ------------- |:-------------:| -----:|
| MINIMAX       | 39.5%         | 24.1% |
| GREEDY        | 100%          | 100%  |
| SELF          | 50%           | 50%   |
| RANDOM        | 82.6%         | 79.3% |
