import random
from typing import Tuple
from ..tttm.gamestate import GameState
from ..tttm.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state: GameState) -> Tuple[int, int]:
    """
    Retorna uma jogada calculada pelo algoritmo minimax para o estado de jogo fornecido.
    :param state: estado para fazer a jogada
    :return: tupla (int, int) com as coordenadas x, y da jogada (lembre-se: 0 é a primeira linha/coluna)
    """

    import time

    # tempo limite em segundos (1 minuto conforme requisito)
    TIME_LIMIT = 60.0
    start_time = time.time()

    player_to_move = state.player

    legal = list(state.legal_moves())
    if not legal:
        # sem jogadas legais — não deveria acontecer em make_move, mas devolve algo
        return (0, 0)

    # utilidade já definida abaixo usa o player original como referência

    # exceção usada para abortar busca quando o tempo esgotar
    class TimeOut(Exception):
        pass

    def time_exceeded():
        return (time.time() - start_time) >= TIME_LIMIT

    # poda alfa-beta com exploração completa (sem limite de profundidade)
    def max_value(s: GameState, alpha: float, beta: float) -> float:
        if time_exceeded():
            raise TimeOut()
        if s.is_terminal():
            return utility(s, player_to_move)
        v = -float('inf')
        for move in s.legal_moves():
            v = max(v, min_value(s.next_state(move), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(s: GameState, alpha: float, beta: float) -> float:
        if time_exceeded():
            raise TimeOut()
        if s.is_terminal():
            return utility(s, player_to_move)
        v = float('inf')
        for move in s.legal_moves():
            v = min(v, max_value(s.next_state(move), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_move = None
    best_val = -float('inf')

    try:
        # ordenar movimentos para determinismo (opcional: could randomize)
        for move in sorted(legal):
            if time_exceeded():
                raise TimeOut()
            val = min_value(state.next_state(move), -float('inf'), float('inf'))
            if val > best_val or best_move is None:
                best_val = val
                best_move = move
    except TimeOut:
        # tempo esgotado — retorna melhor movimento encontrado até agora
        if best_move is None:
            # fallback: alguma jogada legal
            return random.choice(legal)
        return best_move

    # se nenhum timeout, retorna melhor movimento encontrado
    return best_move if best_move is not None else random.choice(legal)

def utility(state, player:str) -> float:
    """
    Retorna a utilidade de um estado (terminal) 
    """
    # Essa função assume que `state` é terminal (GameState.is_terminal() == True)
    # Retorna valor >0 se for bom para `player`, <0 se for ruim, 0 empate.

    # vencedor retornado por GameState.winner() (None se ninguém venceu)
    winner = state.winner()

    if winner is None:
        # nenhum vencedor — empate (tabuleiro cheio sem formar 3 em linha)
        return 0.0

    if winner == player:
        # jogador passado ganhou — isso significa que o outro perdeu (misère)
        return 1.0
    else:
        return -1.0
