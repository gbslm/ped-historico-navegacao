# Histórico de Navegação em Websites

Projeto da disciplina Programação e Estrutura de Dados (IFPB, 2026.2) — Equipe Amebas.
Simulador de navegador em Python (sem HTTP real): mantém histórico de páginas, navega
por URLs cadastradas e por páginas internas.

## Como executar
    python main.py
    python -m unittest discover -s tests -v

## Estrutura
| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Interface de texto, comandos `#` e navegação |
| `historico.py` | Histórico de visitas (PILHA) |
| `arvore.py` | URLs e páginas internas (ÁRVORE, máx. 2 links por página) |
| `catalogo.py` | Carrega/cadastra URLs (`data/urls.txt`) e liga árvore + arquivos |
| `conteudo.py` | Leitura/criação dos `.txt` de cada página (`data/paginas/`) |
| `tests/` | Testes com `unittest` |

## Comandos
`<url>`, `/<pasta>`, `#back`, `#showhist`, `#add <url>`, `#help`, `#sair`

## Estruturas de dados
- **Histórico:** pilha (LIFO) — `#back` desfaz a última visita; push/pop O(1).
- **URLs:** árvore com dicionários por nível — buscar uma URL é O(profundidade).
- **Arquivo da página:** `www.ifpb.edu.br/tsi` → `data/paginas/www.ifpb.edu.br_tsi.txt`.
