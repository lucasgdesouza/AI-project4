import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.

    max_depth = 4

    return minimax_move(state, max_depth, evaluate_custom)

# Funções auxiliares devem ser definidas fora ou dentro do módulo.

def get_mobility_score(state, player, opponent) -> int:
    # O estado já está com o player correto.
    mobility_player = len(state.legal_moves())

    board_copy = state.board.copy()
    
    # Cria um estado para o oponente ter o turno, usando o board_copy.
    opponent_state = GameState(board_copy, opponent)
    
    mobility_opponent = len(opponent_state.legal_moves())

    return float(mobility_player - mobility_opponent)

def get_corner_score(board, player, opponent) -> int:
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    score = 0
    
    for y, x in corners: # Usando y, x para corresponder à indexação da matriz tiles[y][x]
        piece = board.tiles[y][x]
        
        if piece == player:
            score += 1
        elif piece == opponent:
            score -= 1
            
    return score



def evaluate_custom(state, player: str) -> float:
    # --- Configurações de Pesos ---
    # Estes pesos devem ser ajustados (tuning)
    W_MOBILITY = 10.0
    W_CORNER = 100.0
    W_COUNT = 1.0 
    
    board = state.board
    opponent = Board.opponent(player) # Usando Board.opponent para segurança

    if state.is_terminal():
        # Mesmo que você remova o bloco de inf/0.0 para os testes unitários,
        # você PRECISA desta checagem para evitar que a heurística seja calculada
        # quando o estado é terminal e state.player pode ser None.
        
        winner = state.winner() 
        if winner == player:
            return float('inf')
        elif winner is None:
            # Retorne o score numérico ou 0.0, dependendo da sua convenção de empate/fim de jogo
            return 0.0 
        else:
            return float('-inf')

    # 2. MOBILIDADE
    mobility_score = get_mobility_score(state, player, opponent)

    # 3. ESTABILIDADE DE CANTO
    corner_score = get_corner_score(board, player, opponent)

    # 4. CONTADOR DE PEÇAS (Útil para a fase final)
    count_score = board.num_pieces(player) - board.num_pieces(opponent)

    # 5. CÁLCULO FINAL PONDERADO
    final_score = (
        (W_MOBILITY * mobility_score) + 
        (W_CORNER * corner_score) + 
        (W_COUNT * count_score)
    )

    return final_score
