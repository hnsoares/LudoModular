# Projeto Ludo - Grupo 6 - INF1301
Daniel Guimarães    
Henrique Soares    
João Vitor Santana    
Marcos Vinicius

## Build 3 - 16/11
### Entrega estabelecida
* Jogo funcional
* Parte da interface gráfica

### Conteudos da Build
* Jogo funcional
* Salvamento automático, e recuperação de partida em andamento
* Interface básica do menu
* Interface básica do jogo

### Requerimentos
* [**Python 3**](https://python.org) 
* [**Pygame**](https://www.pygame.org/wiki/GettingStarted): Se já tiver o python instalado, é possivel instalar rodando o comando
`pip install pygame`
* [**MySQL**](https://dev.mysql.com/downloads/installer/) e [**Connector**](https://dev.mysql.com/downloads/connector/python/):
Siga as instruções do instalador. Anote a sua conta/senha ao instalar. Será necessário para configurar o banco de dados, para o jogo conseguir armazenar os dados do jogo.


Os outros módulos já estão instalados no python: **xml**, **json**, **os**, **tkinter**, **random**, **datetime** e **unittest**.

### Como jogar
Antes de jogar, primeiro você precisa criar um arquivo `dados/arquivos/credenciais.txt`, contendo as credenciais anotadas nas instalação do MySQL, da seguinte maneira:
    
    host (localhost)
    usuario
    senha

Mais informações no arquivo `dados/arquivos/exemplo_credenciais.txt`

Após isso, execute o arquivo `main.py`. Abrirá uma tela contendo algumas opções. Você pode criar um novo jogo escolhendo uma quantidade
de jogadores, ou carregar alguma partida anterior, se houver.

No jogo, o dado por é rodado automaticamente (seu valor, por enquanto, é exibido no `stdin`, não na tela). Os peões que você
pode escolher se destacarão, e ao clicar em um deles, ele será movimentado. Se não houver, a vez será passada automaticamente.

Você pode sair do jogo em qualquer momento que ele será guardado.

Se quiser parar a música, clique `F3`. Se quiser continuar a música, clique `F4`.

### Testes
O arquivo de testes está em `testes/teste.py`. Ao executar, ele fará todos os testes dos jogos automaticamente.