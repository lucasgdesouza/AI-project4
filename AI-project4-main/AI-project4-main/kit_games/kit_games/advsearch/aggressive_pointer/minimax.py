import math
from typing import Tuple, Callable


def minimax_move(state, max_depth: int, eval_func: Callable) -> Tuple[int, int]:

    player = state.player  # jogador atual

    def minimax(node, depth, alpha, beta, maximizing):

        # condição de parada
        if node.is_terminal() or depth == 0:
            return eval_func(node, player), None

        moves = node.legal_moves()

        # se não há movimentos → passar turno
        if not moves:
            passed = node.pass_turn()
            return minimax(passed, depth - 1, alpha, beta, not maximizing)

        best_move = None

        if maximizing:
            value = -math.inf
            for move in moves:
                child = node.next_state(move)
                new_value, _ = minimax(child, depth - 1, alpha, beta, False)

                if new_value > value:
                    value = new_value
                    best_move = move

                alpha = max(alpha, value)
                if beta <= alpha:
                    break   # poda beta

            return value, best_move

        else:
            value = math.inf
            for move in moves:
                child = node.next_state(move)
                new_value, _ = minimax(child, depth - 1, alpha, beta, True)

                if new_value < value:
                    value = new_value
                    best_move = move

                beta = min(beta, value)
                if beta <= alpha:
                    break   # poda alfa

            return value, best_move

    search_depth = max_depth if max_depth >= 0 else 60

    _, best = minimax(state, search_depth, -math.inf, math.inf, True)
    return best
