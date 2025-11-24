# AI-project4

Nome: Lucas Fraga Balbinot (00585249)
implementação de busca com adversários em jogo da velha invertido e Othello

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
