# Material didático — DECC0294, 2026.2

Tecnologia da Informação e Comunicação Aplicada à Administração
UFMA, Curso de Administração. Turma T01.

Quinze módulos para os encontros 2 a 16. O encontro 1 é a apresentação da disciplina, já dada.

Cada módulo tem três arquivos: o deck em HTML (abre no navegador, sem instalar nada), o script autoinstrucional das atividades (Python, biblioteca padrão apenas) e o roteiro do professor.

## Os quinze módulos

| Mód. | Enc. | Título | Entrega |
|---|---|---|---|
| 1 | 2 | Transformação digital e o trabalho do administrador | |
| 2 | 3 | Ambiente de trabalho digital | A1, 40% da nota 1 |
| 3 | 4 | IA, modelos de linguagem e engenharia de prompt | |
| 4 | 5 | Do prompt ao artefato | |
| 5 | 6 | Dados na Administração | A2, 60% da nota 1 |
| 6 | 7 | Análise exploratória de dados | |
| 7 | 8 | Dados estruturados e consulta | |
| 8 | 9 | Visualização de dados e painéis | B1, 60% da nota 2 |
| 9 | 10 | Automação de documentos e processos | |
| 10 | 11 | Pesquisa, documentos longos e análise qualitativa | B2, 40% da nota 2 |
| 11 | 12 | Aprendizado de máquina e analytics para a decisão | |
| 12 | 13 | Governança de dados, LGPD e cibersegurança | |
| 13 | 14 | Decisão apoiada por IA: contratos, editais e devolutivas | C1, 40% da nota 3 |
| 14 | 15 | Produto digital e gestão ágil | |
| 15 | 16 | Projeto integrador | C2, 60% da nota 3 |

## Os scripts das atividades

Todos rodam com o Python instalado, sem `pip install`, sem rede e sem modelo de linguagem. O aluno não digita comando: o agente do opencode executa. Todos recusam entrega incompleta e dizem o que falta, item por item.

| Script | Comandos |
|---|---|
| `atividade_modulo1.py` | iniciar, conferir |
| `atividade_modulo2.py` | criar, conferir |
| `atividade_modulo3.py` | iniciar, conferir |
| `atividade_modulo4.py` | iniciar, conferir, apis, apis testar, apis \<fonte\> |
| `atividade_modulo5.py` | iniciar, conferir, a2 |
| `atividade_modulo6.py` | perfil, atipicos, log, conferir |
| `atividade_modulo7.py` | banco, esquema, sql, juntar, registrar, conferir |
| `atividade_modulo8.py` | iniciar, painel, conferir, b1 |
| `atividade_modulo9.py` | iniciar, gerar, conferir |
| `atividade_modulo10.py` | fontes, codificar, concordancia, conferir, b2 |
| `atividade_modulo11.py` | iniciar, prever, conferir |
| `atividade_modulo12.py` | varrer, inventario, incidente, conferir |
| `atividade_modulo13.py` | matriz, avaliar, devolutiva, conferir, c1 |
| `atividade_modulo14.py` | produto, backlog, priorizar, teste, conferir |
| `atividade_modulo15.py` | c2, apresentacao, pares, portfolio |

Rodar qualquer um deles sem argumento imprime as instruções de uso.

## As três notas

Nota 1: A1 no encontro 3 (40%) e A2 no encontro 6 (60%).
Nota 2: B1 no encontro 9 (60%) e B2 no encontro 11 (40%).
Nota 3: C1 no encontro 14 (40%) e C2 no encontro 16 (60%).

Cada entrega é conferida pelo script antes de ser recebida. As rodadas `a2`, `b1`, `b2`, `c1` e `c2` listam os arquivos de todos os encontros que compõem a nota.

## Os decks

HTML de arquivo único, abrem com duplo clique no navegador. Setas ou clique avançam; a barra de navegação aparece ao mover o mouse. Não dependem de rede, de fonte instalada nem de PowerPoint.

Paleta clara da identidade visual da UFMA: fundo branco, barra e títulos em vinho, filete dourado no rodapé. Capas, divisores e slides de encerramento em vinho sólido.

Para editar um deck, altere o `build_moduloN.js` correspondente e rode `node build_moduloN.js`. O gerador é o `tema_ufma.js`.

## O que ainda depende de você

Bases de reserva para os encontros 7, 11, 12 e 14, para os alunos que chegarem sem material próprio. Cada roteiro diz qual base o encontro precisa.

O endereço das oito fontes públicas usadas no módulo 4 veio da documentação oficial de cada uma, mas nenhuma chamada pôde ser executada durante a produção do material. Rode `python atividade_modulo4.py apis testar` na máquina do laboratório antes do encontro 5.

A carga horária no programa foi preenchida como 60 h e a unidade como Centro de Ciências Sociais, Curso de Administração. Confirme no SIGAA e corrija o `.docx` se divergir.

O número de alunos define se o projeto integrador do encontro 16 é individual ou em dupla, e se as apresentações cabem em dez minutos cada. O roteiro do módulo 15 traz a conta.
