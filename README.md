Trabalho 4 - Busca com Adversário

Nomes: (turma A)
Lucas Fraga Balbinot - 00585249
Lucas Gomes de Souza - 00580466

Implementação de busca com adversários em jogo da velha invertido e Othello

Jogo da velha invertido:

i) O minimax sempre ganha ou empata jogando contra o randomplayer?
  Sim, foram feitos 50 testes alternando 25 numa configuração de cores e os outros 25 na outra configuração. Em todos os 50 testes, o minimax ganhou ou empatou com o randomplayer. Seguem os dados coletados:
minimax (B) x randomplayer (W) = 11 wins a favor do minimax e 14 draws.
minimax (W) x randomplayer (B) = 25 wins do minimax.

ii) O minimax sempre empata consigo mesmo?
Sim, foram feitos 25 testes e em todos houve empate do minimax consigo mesmo.

iii) O minimax não perde para você quando você usa a sua melhor estratégia?
  Sim, o minimax ganhou a maioria e empatou alguns, mesmo eu utilizando a melhor estratégia que consegui. Seguem os dados dos testes:
minimax (B) x humanplayer (W) = 1 win do minimax e 3 draws.
minimax (W) x humanplayer (B) = 4 wins do minimax.

Othello:

Heurística Custom: A ideia por trás da Heurística foi criar algo mais agressivo e que foque em conquistar pontos e manter na ofensiva. Ele faz cálculos relativos ao que pode providenciar mais pontuação a curto prazo. Também é um sistema que foca em tentar tomar controle dos cantos, devido ao fato de serem um dos únicos pontos em que as peças são impossíveis de serem roubadas, garantindo pontos. Tal sistema foi desenvolvido com o auxílio do Google Gemini.

Seus critérios de parada são dois: chegar a uma profundidade de 4 ou o fim do jogo de Othello como um todo.

Resultados de testes entre os algoritmos:
Condições de teste: D = 5 e Pace = 0.3 segundos.

Count vs Mask - 20 x 44.
Mask vs Count - 45 x 19.
Count vs Custom - 15 x 49.
Custom vs Count - 17 x 47.
Mask vs Custom - 13 x 51.
Custom vs Mask - 49 x 15.

No geral, Custom > Mask > Count.

Implementado: O desempenho de custom foi notável o bastante que ele foi selecionado para servir como nosso agente.

Foi implementado um MCTS em mcts.py como extra.
