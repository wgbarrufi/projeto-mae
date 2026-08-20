# Sistema de Apostas

Projeto desenvolvido para simular um sistema de apostas em partidas de futebol.

O sistema permite o cadastro de usuários, realização e multiplicação de apostas,
consulta de saldo, acompanhamento do status das apostas, consulta de resultados
e visualização do ranking de apostadores.

Também possui uma área administrativa para gerenciamento de usuários, partidas
e apostas.

## Tecnologias utilizadas

- Python
- Flask
- SQLModel
- SQLAlchemy
- SQLite
- HTML
- CSS
- Jinja2
- Football-Data API
- Werkzeug
- python-dotenv

## Arquitetura

O projeto foi organizado em camadas para separar as responsabilidades do sistema.

### Models

Contém as classes que representam as entidades do sistema, como:

- Usuario
- Partida
- Aposta

Os models utilizam SQLModel para realizar o mapeamento objeto-relacional com o
banco de dados.

### Repositories

Responsáveis pelo acesso e persistência dos dados.

Os repositories realizam operações como:

- salvar;
- atualizar;
- pesquisar;
- listar.

Foi utilizado o padrão Repository para separar o acesso ao banco das regras de
negócio.

### Services

Contêm as regras de negócio da aplicação.

Entre elas:

- validação de idade;
- validação de senha;
- autenticação;
- cálculo das odds;
- controle de saldo;
- multiplicação das apostas;
- processamento dos resultados;
- atualização do ranking;
- inativação de usuários.

### API

Responsável pela comunicação com a API externa de futebol.

Os dados das partidas são obtidos da Football-Data API e posteriormente
convertidos em objetos e armazenados no banco de dados.

### Templates

Contém as páginas HTML renderizadas pelo Flask utilizando Jinja2.

### Static

Contém os arquivos estáticos utilizados pela interface, como CSS e imagens.

### Database

Responsável pela configuração da conexão, criação das tabelas e sessões com o
banco de dados.

## Banco de dados

Foi utilizado SQLite.

O banco possui as principais tabelas:

- usuarios;
- partidas;
- apostas.

As apostas possuem relacionamentos com usuários e partidas através de chaves
estrangeiras.

## API externa

O sistema utiliza a Football-Data API para obter informações de partidas de
futebol.

As informações retornadas pela API em JSON são processadas pela aplicação e
persistidas no banco de dados.

O identificador da partida fornecido pela API também é armazenado para evitar
que uma mesma partida seja cadastrada mais de uma vez.

## Funcionalidades do usuário

- Criar conta
- Fazer login
- Trocar senha
- Visualizar partidas disponíveis
- Visualizar odds
- Registrar aposta
- Multiplicar aposta
- Consultar status das apostas
- Consultar saldo
- Consultar resultados anteriores
- Visualizar ranking
- Cancelar participação

## Funcionalidades do administrador

- Listar usuários
- Pesquisar usuário por CPF
- Visualizar partidas
- Importar partidas através da API
- Consultar apostas de uma partida
- Visualizar odds e quantidade de apostadores
- Encerrar partidas e informar o resultado

## Regras das apostas

Cada usuário inicia com 100 pontos.

Uma aposta utiliza 10 pontos do saldo.

As odds são calculadas considerando a quantidade de apostadores em cada
resultado possível.

Uma aposta pode ser multiplicada para x2, x3, x4 e assim sucessivamente,
desde que o usuário possua saldo suficiente.

Quando uma partida é encerrada, as apostas são processadas automaticamente.

Caso o usuário acerte o resultado, o prêmio é calculado considerando:

valor da aposta × odd × multiplicador

Em caso de empate da partida, os pontos utilizados nas apostas são devolvidos
e o ranking de acertos não é alterado.

## Segurança

As senhas não são armazenadas diretamente no banco de dados.

O sistema utiliza funções de hash do Werkzeug para armazenar e verificar as
senhas dos usuários.

As variáveis sensíveis, como chave da API e chave secreta do Flask, são
armazenadas em um arquivo `.env`.

## Como executar

Instale as dependências necessárias:

```bash
pip install flask sqlmodel python-dotenv requests werkzeug