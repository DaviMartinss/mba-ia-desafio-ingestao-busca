# Desafio MBA Engenharia de Software com IA - Full Cycle

Bem-vindo! Este é um projeto de **Ingestão e Busca de Documentos (PDF) com Inteligência Artificial**.

## O que este projeto faz?

1. **Ingesta**: Lê um arquivo PDF, divide o texto em pequenos pedaços (chunks) e gera embeddings (representações numéricas de texto).
2. **Armazenamento**: Persiste esses embeddings em um banco de dados vetorial PostgreSQL.
3. **Busca e Chat**: Permite fazer perguntas sobre o documento via um chatbot que utiliza busca vetorial para encontrar respostas.

## Estrutura do projeto

```
.
├── docker-compose.yml      # Configuração dos serviços (banco de dados PostgreSQL com PGVector)
├── requirements.txt        # Dependências Python do projeto
├── .env                    # Arquivo de variáveis de ambiente (você vai criar este)
├── README.md               # Este arquivo
└── src/
    ├── chat.py             # Interface de chat para fazer perguntas
    ├── ingest.py           # Script para processar PDF e gerar embeddings
    └── search.py           # Utilitários de busca (quando aplicável)
```

## Pré-requisitos

### 1. **Python 3.10 ou superior**
   - Verificar versão: `python --version`
   - Baixar em: https://www.python.org/downloads/

### 2. **Docker e Docker Compose**
   - Verificar instalação: `docker --version` e `docker compose --version`
   - Baixar em: https://www.docker.com/products/docker-desktop

### 3. **Um arquivo PDF** (para ingestar)
   - Pode ser qualquer PDF com texto

## Passo 1: Configurar as Variáveis de Ambiente

### 1.1 Criar arquivo `.env`
Na raiz do projeto (mesmo local do `docker-compose.yml`), crie um arquivo chamado `.env` com o seguinte conteúdo:

```
GOOGLE_API_KEY=your_google_api_key_here
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5434/rag
PG_VECTOR_COLLECTION_NAME=desafio01
PDF_PATH=document.pdf
```

### 1.2 Explicação das variáveis:
- **GOOGLE_API_KEY**: Sua chave da API Google (necessária para embeddings). Obter em: https://ai.google.dev/
- **DATABASE_URL**: URL de conexão com o banco PostgreSQL (não mude se estiver usando Docker Compose)
- **PG_VECTOR_COLLECTION_NAME**: Nome da coleção onde os embeddings serão armazenados
- **PDF_PATH**: Caminho do arquivo PDF (coloque o PDF na raiz do projeto ou use caminho absoluto)

## Passo 2: Configurar o Ambiente Python

### 2.1 Abra o terminal na raiz do projeto

No Windows (PowerShell):
```powershell
cd "C:\caminho\para\o\projeto"
```

No macOS/Linux:
```bash
cd /caminho/para/o/projeto
```

### 2.2 Criar um ambiente virtual
Um ambiente virtual isola as dependências do projeto.

No Windows (PowerShell):
```powershell
python -m venv venv
```

No macOS/Linux:
```bash
python3 -m venv venv
```

### 2.3 Ativar o ambiente virtual

No Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

Se receber um erro de permissão, execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

No macOS/Linux:
```bash
source venv/bin/activate
```

**Você saberá que funcionou quando ver `(venv)` no início da linha do terminal.**

### 2.4 Instalar as dependências
```bash
pip install -r requirements.txt
```

Isso pode levar alguns minutos. Aguarde até ver `Successfully installed...`.

## Passo 3: Subir o Banco de Dados

Abra um **novo terminal** (mantendo o primeiro ativo) na raiz do projeto:

```bash
docker compose up -d
```

**O que acontece:**
- `-d` = rodar em background (seu terminal fica livre)
- Cria um contêiner PostgreSQL com extensão PGVector
- Pode levar alguns minutos na primeira vez

**Verificar se funcionou:**
```bash
docker ps
```

Você deve ver um contêiner `postgres` listado.

## Passo 4: Ingestar o PDF

No terminal do Python ativo (com venv), execute:

```bash
python src/ingest.py
```

**O que esperar:**
- O script lê o PDF definido em `PDF_PATH`
- Divide o texto em chunks
- Gera embeddings (pode levar alguns minutos)
- Armazena no banco PostgreSQL
- Mensagem de sucesso no final

**Se deu erro?** Veja a seção "Solução de problemas comuns" abaixo.

## Passo 5: Usar o Chat

No mesmo terminal, execute:

```bash
python src/chat.py
```

**Como usar:**
- Faça perguntas sobre o documento (em linguagem natural)
- Pressione ENTER sem digitar nada para encerrar

**Exemplo:**
```
Você: Qual é o assunto principal do documento?
Bot: [Resposta baseada no PDF]

Você: Fale mais sobre...
Bot: [Resposta]

```

## Solução de problemas comuns

### Erro: "No module named 'langchain'"
- **Causa**: Dependências não instaladas
- **Solução**: 
  1. Ative o ambiente virtual: `.\venv\Scripts\Activate.ps1` (Windows) ou `source venv/bin/activate` (Mac/Linux)
  2. Instale novamente: `pip install -r requirements.txt`

### Erro: "PDF_PATH is not set" ou "arquivo não encontrado"
- **Causa**: Variável `PDF_PATH` não definida ou caminho incorreto
- **Solução**:
  1. Verifique se `.env` existe na raiz do projeto
  2. Verifique se `PDF_PATH` aponta para um arquivo que existe
  3. Use caminho absoluto: `C:\caminho\completo\documento.pdf`

### Erro: "Connection refused" ao conectar no banco
- **Causa**: PostgreSQL não está rodando
- **Solução**:
  1. Verifique: `docker ps` deve listar um contêiner PostgreSQL
  2. Se não aparecer, execute: `docker compose up -d`

### Erro: "docker: command not found"
- **Causa**: Docker não está instalado
- **Solução**: Baixe Docker Desktop em https://www.docker.com/products/docker-desktop

### ImportError ou ModuleNotFoundError
- **Causa**: Ambiente virtual não está ativado
- **Solução**: Execute `.\venv\Scripts\Activate.ps1` (Windows) ou `source venv/bin/activate` (Mac/Linux)

## Dicas úteis

- **Verificar ambiente virtual ativo**: Deve ter `(venv)` no prompt
- **Desativar ambiente virtual**: Digite `deactivate`
- **Parar o Docker**: `docker compose down`
- **Ver logs do Docker**: `docker compose logs`
- **Limpar cache Python**: `pip cache purge`

## Próximos passos

1. Teste com um PDF pequeno primeiro
2. Se tiver sucesso, experimente com documentos maiores
3. Customize o prompt do chat em `src/chat.py` conforme necessário
4. Explore a busca vetorial em `src/search.py`

## Precisa de ajuda?

- Verifique se o arquivo `.env` existe na raiz
- Certifique-se de que Python, Docker e pip estão instalados
- Consulte os links dos pré-requisitos acima
- Verifique os logs: `docker compose logs`
