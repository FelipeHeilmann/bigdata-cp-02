# Guia: colecoes MongoDB e DAO Mongo

Este guia descreve, passo a passo, como criar as colecoes no MongoDB para os modelos do projeto (`Book`, `Student`, `Loan`) e como implementar uma DAO Mongo que respeita as interfaces que ja existem em `src/application/dao/`.

Nenhum codigo esta incluido aqui: o objetivo e entender as decisoes antes de implementar.

---

## 1. Entender o que ja existe

Antes de comecar, revise estes pontos no projeto:

| Camada | Arquivo | Papel |
|---|---|---|
| Modelo | `src/application/models/book.py` | Entidade `Book` |
| Modelo | `src/application/models/student.py` | Entidade `Student` |
| Modelo | `src/application/models/loan.py` | Entidade `Loan` |
| Interface (porta) | `src/application/dao/book_dao.py` | Contrato `BookDao` |
| Interface (porta) | `src/application/dao/student_dao.py` | Contrato `StudentDao` |
| Interface (porta) | `src/application/dao/loan_dao.py` | Contrato `LoanDao` |
| Implementacao em memoria | `src/infra/dao/*_memory.py` | Usada hoje pelos testes |

A regra de ouro: **a camada de aplicacao depende apenas das interfaces**. A DAO Mongo sera uma nova implementacao dessas interfaces, dentro de `src/infra/dao/`, e nao deve vazar detalhes do MongoDB para os casos de uso.

---

## 2. Mapear cada modelo para uma colecao

Cada modelo vira uma colecao, com um documento por instancia.

| Colecao | Modelo | Campos |
|---|---|---|
| `books` | `Book` | id, isbn, title, author, year, category, copies, available_copies |
| `students` | `Student` | id, name, age, major, email, enrollment_id |
| `loans` | `Loan` | id, book_id, student_id, date, return_date, fine |

Pontos de atencao para cada campo:

- **Identificador (`id`)**: os modelos usam `id` como string (UUID gerado com `uuid4`). Voce pode:
  - (a) guardar esse UUID como `_id` do documento, mantendo o mesmo valor que o dominio ja usa; ou
  - (b) deixar o Mongo gerar um `ObjectId` e converter para string na ida e na volta.
  
  A opcao (a) e mais simples, porque evita conversoes e mantem o dominio identico ao que os testes ja esperam. Recomendado para este projeto.

- **Datas (`date`, `return_date`)**: o Python usa `datetime`, e o Mongo armazena datas em formato proprio (BSON Date), que e sempre em UTC e com precisao de milissegundos. Decida se o projeto trabalha com datas *naive* ou *timezone-aware* e seja consistente. Valores `None` (como `return_date` de um emprestimo ainda aberto) devem ser salvos como `null`.

- **Valores monetarios (`fine`)**: e um `float`. Para multas, tenha em mente que floats tem imprecisao binaria. Se o trabalho exigir precisao exata de centavos, considere guardar em centavos (inteiro) ou usar `Decimal` com conversao. Para um trabalho academico, `float` costuma bastar, mas vale registrar a escolha.

- **Chaves estrangeiras (`book_id`, `student_id` em `Loan`)**: no Mongo nao existe chave estrangeira. O vinculo e apenas por valor. Quem garante a integridade e a camada de aplicacao (ex.: `BorrowBook` so cria emprestimo para um livro e um aluno que existem).

---

## 3. Definir as regras de unicidade e os indices

Indices sao o que faz as consultas funcionarem bem e o que impede dados duplicados. Defina-os junto com a criacao das colecoes:

1. **`books`**
   - Indice unico em `isbn`: dois livros nao podem ter o mesmo ISBN (o `BookDao` ja expõe `get_by_isbn`).
   - O `_id` ja e indexado automaticamente.

2. **`students`**
   - Indice unico em `enrollment_id` (o `StudentDao` expõe `get_by_enrollment_id`).

3. **`loans`**
   - Indice composto em `student_id` + `return_date`, para acelerar `get_active_loans_by_student_id` (emprestimos sem data de devolucao) e `get_overdue_loans_by_student_id`.
   - Considere tambem indice em `book_id`, caso voce consulte emprestimos por livro.

Observacao: indices unicos falham em caso de duplicidade. Se o seu codigo hoje permite salvar dois livros com o mesmo ISBN, o Mongo vai rejeitar a segunda insercao. Trate esse erro na DAO e traduza para uma excecao de dominio.

---

## 4. Preparar o ambiente

1. **Adicionar a dependencia**: inclua o driver oficial do Python (`pymongo`) no `requirements.txt` e reinstale o ambiente virtual.
2. **Configurar a conexao por variavel de ambiente**: a URI de conexao deve vir de uma variavel (ex.: `MONGO_URI`), nunca fixa no codigo.
   - A URI que voce usa no VS Code (`mongodb://user:...@localhost:27017/?authSource=admin`) tem a senha em texto puro. Nao a versione no git. Use um arquivo `.env` e adicione `.env` ao `.gitignore`.
3. **Escolher o nome do banco**: defina um nome unico para o banco da aplicacao (ex.: `library`). As colecoes ficam dentro dele.
4. **Confirmar que o container esta de pe**: o compose ja publica a porta 27017. Antes de testar a DAO, rode `docker compose up -d` e verifique com `docker ps`.

---

## 5. Criar as colecoes

O MongoDB cria uma colecao automaticamente na primeira insercao, entao nao e obrigatorio cria-las na mao. Mesmo assim, recomenda-se criar explicitamente, para que os indices e as regras fiquem em um unico lugar:

1. Conecte-se ao banco pelo VS Code (ou pelo `mongosh`).
2. Crie as colecoes `books`, `students` e `loans` dentro do banco escolhido.
3. Crie os indices definidos na secao 3.
4. Confirme no VS Code que as colecoes e os indices aparecem.

Alternativa: deixar essa etapa no proprio codigo, em uma rotina de inicializacao que roda uma vez quando a aplicacao sobe. Essa rotina deve ser idempotente (rodar duas vezes nao pode quebrar nada).

---

## 6. Definir a conversao entre modelo e documento

Os modelos sao objetos Python; o Mongo guarda documentos (dicionarios). A DAO precisa de duas conversoes simetricas:

- **Modelo para documento** (ao salvar ou atualizar): converte cada atributo para um campo do documento, renomeia `id` para `_id` e converte datas e valores nulos.
- **Documento para modelo** (ao ler): faz o caminho inverso e **reconstroi o objeto de dominio**.

Atencao com um detalhe do projeto: os modelos `Book` e `Student` possuem um `__init__` customizado que gera um novo UUID. Na reconstrucao a partir do banco, **nao** use o construtor padrao que geraria um novo `id`: o `id` salvo precisa ser preservado. Verifique como os modelos aceitam o `id` antes de implementar.

Mantenha essas conversoes **dentro da DAO** (ou em funcoes auxiliares na propria camada de infraestrutura). Os modelos e os casos de uso nao devem conhecer o formato do Mongo.

---

## 7. Implementar uma DAO por interface

Crie uma classe por interface, na pasta `src/infra/dao/`, por exemplo:

- Uma DAO Mongo para livros, implementando `BookDao`
- Uma DAO Mongo para alunos, implementando `StudentDao`
- Uma DAO Mongo para emprestimos, implementando `LoanDao`

Cada metodo abstrato deve ser implementado com a consulta correspondente:

| Interface | Metodo | Equivalente no Mongo (conceito) |
|---|---|---|
| `BookDao` | `list_books` | buscar todos os documentos da colecao |
| `BookDao` | `get_by_isbn` | buscar por `isbn` (retorna `None` se nao achar) |
| `BookDao` | `get_by_id` | buscar por `_id` |
| `BookDao` | `save` | inserir um documento |
| `BookDao` | `update` | substituir ou atualizar o documento pelo identificador |
| `BookDao` | `remove` | remover o documento pelo identificador |
| `StudentDao` | `get_by_enrollment_id` | buscar por `enrollment_id` |
| `LoanDao` | `get_active_loans_by_student_id` | `student_id` igual e `return_date` nulo, com a data de referencia |
| `LoanDao` | `get_overdue_loans_by_student_id` | `student_id` igual, `return_date` nulo e data de vencimento anterior a referencia |

Pontos de atencao:

- **Retorno de "nao encontrado"**: as interfaces usam `Model | None`. Quando o Mongo nao achar o documento (`find_one` retorna nulo), devolva `None` em vez de lancar excecao.
- **Inconsistencia atual a resolver**: `BookDao.remove` recebe um `Book`, mas `BookDaoMemory.remove` recebe um `id`. Escolha uma assinatura (recomendado: `id`, que e mais simples) e ajuste a interface e as implementacoes para que sejam iguais. Isso evita bugs quando a DAO Mongo for trocada.
- **Atualizacao**: `BookDaoMemory.update` localiza o livro pelo `isbn`, enquanto o identificador natural de uma entidade e o `id`. Defina qual chave identifica o registro na atualizacao e use a mesma logica na DAO Mongo.
- **Datas na consulta**: a comparacao de datas em `get_overdue_loans_by_student_id` deve usar o mesmo tipo e fuso que foram gravados.

---

## 8. Escolher como trocar a implementacao

Hoje os casos de uso recebem a DAO por construtor (injecao de dependencia). Isso permite trocar a implementacao sem mexer na logica:

- Nos **testes de integracao**, continue usando as DAOs em memoria por padrao, pois sao rapidas e nao dependem de container.
- Crie uma **suite separada** para a DAO Mongo, que roda contra o container (ou um banco de teste dedicado). Assim voce valida a implementacao real sem misturar com os testes rapidos.
- Quando a aplicacao rodar de verdade, escolha a DAO Mongo na montagem (ponto de entrada da aplicacao) e nao dentro dos casos de uso.

Uma boa pratica: use um banco de teste separado (outro nome de banco) e limpe as colecoes antes de cada teste, para que os testes sejam independentes entre si.

---

## 9. Validar

Checklist para considerar a DAO Mongo pronta:

- [ ] `pymongo` esta no `requirements.txt` e instalado no `.venv`.
- [ ] A URI de conexao vem de variavel de ambiente, e a senha nao esta versionada no git.
- [ ] As colecoes `books`, `students` e `loans` existem no banco.
- [ ] Os indices unicos (`isbn`, `enrollment_id`) e o indice de emprestimos estao criados.
- [ ] Cada metodo das tres interfaces esta implementado na DAO Mongo.
- [ ] Ao salvar e depois ler um modelo, todos os campos voltam iguais, incluindo o `id` e as datas.
- [ ] Ler um identificador inexistente retorna `None`.
- [ ] Os testes existentes continuam passando com as DAOs em memoria.
- [ ] Os testes da DAO Mongo passam contra o container.
- [ ] Verificou-se no VS Code que os documentos aparecem com a estrutura esperada.

---

## Resumo do caminho

1. Entender as interfaces e os modelos existentes.
2. Mapear cada modelo para uma colecao e definir os campos.
3. Definir indices e regras de unicidade.
4. Preparar o ambiente (`pymongo`, variavel de ambiente, container).
5. Criar as colecoes e os indices.
6. Definir a conversao entre modelo e documento.
7. Implementar uma DAO por interface.
8. Trocar a implementacao na montagem da aplicacao, mantendo os testes em memoria.
9. Validar com o checklist.
