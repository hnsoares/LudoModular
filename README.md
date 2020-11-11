# Projeto Ludo - Grupo 1
Este é o repositório para o código do jogo Ludo, 
feito pelo grupo 1 da disciplina INF1301, 2020.2.

## Build 1 - 19/10
### Entrega estabelecida
* Lançamento do dado pronto
* Movimentação das peças
* Múltiplas jogadas em série

### Conteudos da Build
* Lançamento automático do dado
* Rodada (lançamento do dado, escolha da peça, movimentação da peça)
* Detecção da vitória

Para observar a build, basta rodar o arquivo `main.py`. Ao rodar, uma partida será
automaticamente criada. Ela consiste em uma partida de Ludo com 4 jogadores.

Ela é dividida em rodadas. Em cada _rodada, o dado é jogado automaticamente, e é detectado
quais são os peões que podem ser movidos. Se não houver peão, a _rodada é passada automaticamente.
Se houver peão, o usuário pode interagir por meio do stdin digitando o número do peão a ser movido
(seguindo as instruções indicadas), e então é indicado para qual posição o peão foi movido, e se
este capturou algum outro peão. A partida acaba quando um dos jogadores chega com todos os (4) peões na casa final.

### Testes
O arquivo de testes está na pasta `testes`, no arquivo `teste.py`. Ao rodar, ele automaticamente
roda vários testes para detectar se a funcionalidade atual do jogo está correta.
