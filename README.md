# Biblioteca (CP-02 · Big Data)

Sistema de gerenciamento de biblioteca em Python: cadastro de livros e alunos, empréstimos e devoluções com cálculo de multa. Usa MongoDB como banco e uma interface de linha de comando (CLI) como porta de uso.

## Sumário

- [Requisitos](#requisitos)
- [Configuração](#configuração)
- [Como rodar](#como-rodar)
  - [Com Docker (recomendado)](#com-docker-recomendado)
  - [Localmente](#localmente)
- [Como rodar os testes](#como-rodar-os-testes)
- [Design do projeto](#design-do-projeto)

## Requisitos

- [Docker](https://docs.docker.com/get-docker/) e Docker Compose (para rodar tudo em containers)
- Para rodar localmente: Python 3.14 e o MongoDB acessível (o próprio compose sobe o banco)

## Configuração

Todas as configurações ficam em um único lugar: o arquivo `.env`.

```bash
cp .env.example .env
```

| Variável | Para que serve | Padrão |
|---|---|---|
| `MONGO_USER` | Usuário root do MongoDB (usado pelo compose) | `user` |
| `MONGO_PASSWORD` | Senha do usuário root | `ZHNhZGFkYWRhc2Rh` |
| `MONGO_DATABASE` | Nome do banco da aplicação | `library` |
| `MONGO_URI` | URI de conexão usada ao rodar **fora** do Docker | `mongodb://user:...@localhost:27017/?authSource=admin` |

Dentro do Docker, o `docker-compose.yml` monta a URI sozinho apontando para o host `mongo`, então a `MONGO_URI` do `.env` só importa para execução local.

O `.env` não vai para o git (já está no `.gitignore`).

## Como rodar

### Com Docker (recomendado)

1. Suba o MongoDB:

   ```bash
   docker compose up -d mongo
   ```

2. Rode a CLI em um container descartável:

   ```bash
   docker compose run --rm app
   ```

   O menu aparece no terminal. Digite o número da opção e siga os prompts. `0` encerra.

3. Para derrubar tudo, mantendo os dados do banco:

   ```bash
   docker compose down
   ```

   Para apagar também os dados do MongoDB, use `docker compose down -v`.

### Localmente

1. Crie e ative um ambiente virtual e instale as dependências:

   ```bash
   python3.14 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Suba o MongoDB (`docker compose up -d mongo`) e confira que `MONGO_URI` no `.env` aponta para `localhost`.

3. Rode a CLI a partir da raiz do projeto:

   ```bash
   python -m src.cli
   ```

## Como rodar os testes

Os testes são de integração: usam as DAOs em memória (rápidas, sem banco) e as DAOs MongoDB (que exigem o container no ar).

```bash
# local (com o venv ativo e o mongo no ar)
pytest

# com relatório de cobertura
pytest --cov=src --cov-report=term-missing

# dentro do Docker
docker compose up -d mongo
docker compose run --rm app python -m pytest
```

Os testes que usam MongoDB gravam no banco definido em `MONGO_DATABASE`. Para não misturar com seus dados, rode-os com um banco separado:

```bash
MONGO_DATABASE=library_test pytest
```

Cada teste limpa o que criou. Se um teste falhar no meio, pode sobrar documento no banco; nesse caso, apague o banco de teste (`MONGO_DATABASE=library_test`) ou os livros/alunos com os dados de teste.

## Design do projeto

### Arquitetura

O projeto segue a arquitetura hexagonal (portas e adaptadores). O núcleo da aplicação (`src/application`) reúne os casos de uso, as entidades, os erros e as **portas**, que são as interfaces das DAOs. O núcleo não conhece banco, CLI nem framework: quem se conecta a ele são os **adaptadores**, que ficam do lado de fora.

```
 CLI (src/cli)  ───▶  Núcleo (src/application)  ───▶  Portas (application/dao)
 adaptador de          casos de uso, entidades,            ▲ implementadas por
 entrada               erros                               │
                                                  infra/dao: *_memory.py, *_mongo.py
                                                  adaptadores de saída
```

### Estrutura de pastas

```
src/
├── application/
│   ├── models/        # entidades: Book, Student, Loan
│   ├── dao/           # interfaces (portas) de persistência: BookDao, StudentDao, LoanDao
│   ├── usecases/      # uma classe por operação: CreateBook, BorrowBook, ReturnBook...
│   └── errors/        # ApplicationError e erros específicos de negócio
├── infra/
│   ├── config.py      # URI e nome do banco, lidos do ambiente (.env)
│   └── dao/           # implementações: *_memory.py e *_mongo.py
└── cli/
    ├── app.py         # ponto de montagem: cria as DAOs, monta o menu, executa o loop
    ├── commands.py    # uma função por opção do menu (coleta inputs e chama o caso de uso)
    ├── prompts.py     # leitura de inputs com validação e nova tentativa
    └── error_handler.py  # handler global: transforma exceções em mensagens para o usuário
tests/
├── helpers.py         # geradores de ISBN e matrícula aleatórios
└── integration/       # testes dos casos de uso, contra memória e/ou MongoDB
docs/
└── mongodb-dao-guide.md  # guia de como as coleções e as DAOs Mongo foram montadas
```

### Entidades

| Modelo | Campos principais | Observações |
|---|---|---|
| `Book` | id, isbn, title, author, year, category, copies, available_copies | `copies` é o total; `available_copies` cai ao emprestar e volta ao devolver |
| `Student` | id, enrollment_id, name, age, major, email | `enrollment_id` (matrícula) é a chave de negócio |
| `Loan` | id, book_id, student_id, date, return_date, fine | empréstimo em aberto é aquele com `return_date` nulo |

As entidades usam UUID gerado na criação (`uuid4`) como identificador. Relações entre entidades são feitas por id (`book_id`, `student_id`), como em um banco relacional, mas sem chave estrangeira no banco: a integridade é garantida pelos casos de uso.

### Casos de uso

Cada operação do sistema é uma classe em `application/usecases/`, com:

- um construtor que recebe as **DAOs** de que precisa (injeção de dependência);
- um método `execute(input)` que recebe um objeto `Input` (dataclass) e devolve um `Output` (dataclass).

Exemplo do fluxo de empréstimo (`BorrowBook`):

1. consulta os empréstimos ativos e atrasados do aluno;
2. recusa se o aluno já tem 3 empréstimos ativos ou algum atrasado;
3. busca o livro e recusa se não houver exemplar disponível;
4. cria o `Loan`, decrementa `available_copies` e salva tudo.

Regras como validação de ISBN, de e-mail, de exemplares e de multa ficam nos casos de uso, e não na CLI nem no banco. Assim a mesma regra vale para qualquer interface que venha a usar o sistema.

### Portas e adaptadores (DAOs)

As interfaces em `application/dao/` (`BookDao`, `StudentDao`, `LoanDao`) são **portas**: definem o que a aplicação precisa do armazenamento, sem dizer como. Há dois adaptadores para cada uma:

- **`*_memory.py`**: listas em memória. Usadas nos testes, por serem rápidas e isoladas.
- **`*_mongo.py`**: coleções `books`, `students` e `loans` no MongoDB. O `id` da entidade é gravado como `_id`, e as conversões modelo ↔ documento ficam dentro da própria DAO (`_to_document` e `_to_model`).

Trocar de banco significa escrever um novo adaptador, sem tocar nos casos de uso. Essa troca é exatamente o que os testes fazem ao rodar os mesmos cenários nas duas implementações.

### Tratamento de erros

- Todos os erros de negócio herdam de `ApplicationError` e carregam uma `message` pronta para o usuário.
- O núcleo (casos de uso) lança esses erros; ele não imprime nada.
- `cli/error_handler.py` tem o decorador `handle_errors`, que envolve cada ação do menu:
  - `ApplicationError` → mostra a mensagem do erro;
  - falha de conexão do PyMongo → orienta a subir o container;
  - qualquer outra exceção → mostra "Erro inesperado", sem derrubar o programa.

### CLI

- `app.py` é o **ponto de composição**: é o único lugar que escolhe as implementações concretas (hoje, as DAOs Mongo) e monta o menu. Para usar outro banco, a mudança fica aqui.
- `commands.py` faz a ponte entre o usuário e os casos de uso: coleta os inputs com `prompts.py` (que repete a pergunta quando o valor é inválido), chama o caso de uso e mostra o resultado.
- Empréstimo e devolução listam antes os livros e os empréstimos em aberto, para o usuário escolher o item certo sem precisar decorar ISBN ou ID.

### Configuração

`infra/config.py` é a única fonte da URI e do nome do banco. Ele lê as variáveis de ambiente e carrega o `.env` automaticamente (via `python-dotenv`). As DAOs importam daqui; nenhuma URI fica espalhada pelo código.

### Docker

- `Dockerfile`: imagem Python 3.14 slim, instala as dependências e copia `src/` e `tests/`. O comando padrão roda a CLI.
- `docker-compose.yml`: dois serviços. `mongo` guarda os dados em um volume nomeado; `app` roda a CLI e enxerga o banco pelo host `mongo`.
- `.dockerignore`: deixa de fora `.venv`, `.git`, `.env` e caches, para a imagem ficar pequena e sem segredos.

### Estratégia de testes

- **Casos de uso**: testados com as DAOs em memória, cobrindo sucesso e cada erro de negócio.
- **DAOs Mongo**: exercitadas pelos mesmos cenários de integração, contra um banco real.
- **CLI**: validada manualmente, executando o menu com entradas roteirizadas (`printf ... | python -m src.cli`), contra o MongoDB.
