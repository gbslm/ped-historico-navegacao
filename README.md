# Histórico de Navegação em Websites

Projeto desenvolvido para a disciplina de **Programação e Estrutura de Dados**, do curso de Redes de Computadores do IFPB.

O objetivo é simular um navegador web por meio de uma aplicação em Python, permitindo acessar URLs previamente cadastradas, registrar o histórico de navegação e retornar à página anteriormente visitada.

## Objetivos do Checkpoint 1

- Criar uma interface de interação com o navegador.
- Carregar URLs válidas a partir de um arquivo de texto.
- Validar o formato e verificar o cadastro das URLs.
- Permitir o cadastro de novas URLs.
- Implementar uma estrutura de dados para armazenar o histórico de navegação em memória.

## Estrutura do Projeto

```text
ped-historico-navegacao/
├── main.py
├── src/
│   ├── navegador.py
│   ├── historico.py
│   ├── urls.py
│   └── cadastro.py
├── dados/
│   └── urls.txt
├── tests/
├── README.md
└── .gitignore
```

## Tecnologias

- Python 3
- Git e GitHub

## Como executar

1. Instale o Python 3.
2. Clone este repositório.
3. Entre na pasta do projeto.
4. Execute o programa pelo terminal:

```bash
python main.py
```

Caso seu sistema utilize o comando `python3`, execute:

```bash
python3 main.py
```

## Comandos

| Comando | Descrição |
|---|---|
| `#add <url>` | Solicita o cadastro de uma nova URL. |
| `#back` | Retorna à última página visitada, quando disponível. |
| `#showhist` | Exibe o histórico atual de navegação. |
| `#sair` | Encerra a execução do programa. |

## Equipe

- Gabriel Salomão
- Arthur Dantas
- João Henrique Quaresma
- Pedro Henrique da Silva

## Disciplina

Programação e Estrutura de Dados — IFPB

Professor: Wallennon Germano