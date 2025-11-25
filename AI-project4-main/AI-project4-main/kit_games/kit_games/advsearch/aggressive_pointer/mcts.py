import random
import math
from typing import Tuple, Optional, List

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # ---- Parâmetros do MCTS ----
    ITERATIONS = 200
    C = math.sqrt(2)  # constante de exploração

    # quick check: se há movimento terminal que vence de imediato, retorne-o.
    player = state.player
    legal_moves = list(state.legal_moves())
    for move in legal_moves:
        child = state.next_state(move)
        if child.is_terminal():
            winner = child.winner()
            if winner == player:
                return move

    # Se não houver movimentos legais, só retorna uma jogada inválida
    if not legal_moves:
        return (-1, -1)

    class Node:
        __slots__ = ("state", "parent", "move", "children", "visits", "wins", "untried_moves")

        def __init__(self, state, parent=None, move=None):
            self.state = state
            self.parent = parent
            self.move = move
            self.children = []  # type: List[Node]
            self.visits = 0
            self.wins = 0.0
            # untried moves is a list of moves we can still expand
            try:
                self.untried_moves = list(state.legal_moves())
            except Exception:
                self.untried_moves = []

        def expand(self):
            move = self.untried_moves.pop()
            child_state = self.state.next_state(move)
            child = Node(child_state, self, move)
            self.children.append(child)
            return child

        def is_fully_expanded(self):
            return len(self.untried_moves) == 0

        def best_child(self, c_param=C):
            choices_weights = []
            for child in self.children:
                if child.visits == 0:
                    # avoid division by zero; prefer unvisited
                    weight = float('inf')
                else:
                    exploitation = child.wins / child.visits
                    exploration = c_param * math.sqrt(math.log(self.visits) / child.visits)
                    weight = exploitation + exploration
                choices_weights.append((weight, child))
            return max(choices_weights, key=lambda x: x[0])[1]

    def tree_policy(node: Node) -> Node:
        # selection & expansion
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            else:
                node = node.best_child()
        return node

    def default_policy(state) -> float:
        # simulate a random playout until terminal
        current_state = state.copy()
        # safety bound to avoid infinite loops
        depth = 0
        while not current_state.is_terminal() and depth < 1000:
            moves = list(current_state.legal_moves())
            if not moves:
                # try pass_turn if exists
                if hasattr(current_state, 'pass_turn'):
                    current_state = current_state.pass_turn()
                else:
                    break
            else:
                move = random.choice(moves)
                current_state = current_state.next_state(move)
            depth += 1

        winner = current_state.winner()
        if winner is None:
            return 0.0
        return 1.0 if winner == player else 0.0

    def backup(node: Optional[Node], result: float):
        # result is 1.0 if root player won simulation, else 0.0 for loss/draw
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    # Build the tree from the root
    root = Node(state)

    for _ in range(ITERATIONS):
        # selection & expansion
        node = tree_policy(root)
        # simulation
        outcome = default_policy(node.state)
        # backup
        backup(node, outcome)

    # If there were no children (shouldn't happen if there is at least 1 legal move),
    # fallback to a random legal move
    if not root.children:
        return random.choice(legal_moves)

    best = max(root.children, key=lambda c: c.visits)
    if best.move is None:
        return random.choice(legal_moves)
    return best.move

