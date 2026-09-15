# DECC0294 - Tecnologia da Informação e Comunicação Aplicada à Administração

Material didático completo da disciplina, oferecida no Curso de Administração da Universidade Federal do Maranhão, semestre 2026.2.

São 15 módulos, um por encontro, dos encontros 2 ao 16. O encontro 1 é a apresentação da disciplina. Cada encontro tem cerca de quatro horas e se divide em quatro ciclos de teoria, demonstração, prática e entrega.

A disciplina é dada em laboratório, com um agente de programação (opencode) e controle de versão pelo GitHub Desktop. Os alunos usam modelos gratuitos, e todo o material foi escrito para continuar funcionando quando a cota do modelo acaba.

## O que tem aqui

Cada um dos 15 módulos tem três arquivos:

- `moduloN-nome.html`, o deck de slides, que abre no navegador com duplo clique
- `atividade_moduloN.py`, o script autoinstrucional das atividades
- `roteiro-moduloN.md`, o roteiro do professor, com tempos e notas de condução

Além disso, `programa-decc0294-2026-2.docx` traz o programa oficial e `planejamento-disciplina-v2.md` registra as decisões de desenho da disciplina. `indice-material-2026-2.md` é o mapa dos arquivos com a tabela de comandos de cada script, e `index.html` é a página de entrada que lista os 15 módulos com links de Slides, Roteiro e Script.

Os arquivos `modulo1-transformacao-digital.pptx` e `modulo2-ambiente-de-trabalho-digital.pptx` são os editáveis de origem dos decks 1 e 2. As pastas `dados/`, `entregas/`, `saidas/` e `prompts/` são a estrutura de trabalho do aluno: bases de entrada, arquivos que valem nota, saídas geradas e caderno de prompts, cada uma com seu `LEIA-ME.md` ou `.manter`.

A tabela da seção Os módulos, mais abaixo, reúne o link de slides e o link de script de cada um dos quinze módulos, na ordem dos encontros.

## Os slides

Arquivo HTML único, sem dependência de rede, de fonte instalada ou de PowerPoint. Setas do teclado ou clique avançam. A barra de navegação aparece ao mover o mouse e some sozinha.

A identidade visual segue o Manual de Identidade Visual UFMA 2024, na paleta clara: fundo branco, barra e títulos em vinho, filete dourado no rodapé.

## Os scripts das atividades

Rodam com a biblioteca padrão do Python, sem `pip install`, sem acesso à rede e sem modelo de linguagem. O aluno não digita comandos: o agente do opencode executa por ele.

Cada script recusa entrega incompleta e diz, item por item, o que falta. Executar qualquer um deles sem argumento imprime as instruções de uso.

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

## Os módulos

A coluna Slides abre o deck já renderizado no navegador, via GitHub Pages. A coluna Script leva ao arquivo Python da atividade. O roteiro de cada módulo, de uso do professor, está listado no índice do material.

| Mód. | Enc. | Título | Slides | Script | Entrega |
|---|---|---|---|---|---|
| 1 | 2 | Transformação digital e o trabalho do administrador | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo1-transformacao-digital.html) | [Script](atividade_modulo1.py) | |
| 2 | 3 | Ambiente de trabalho digital | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo2-ambiente-de-trabalho-digital.html) | [Script](atividade_modulo2.py) | A1 |
| 3 | 4 | IA, modelos de linguagem e engenharia de prompt | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo3-ia-e-engenharia-de-prompt.html) | [Script](atividade_modulo3.py) | |
| 4 | 5 | Do prompt ao artefato | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo4-do-prompt-ao-artefato.html) | [Script](atividade_modulo4.py) | |
| 5 | 6 | Dados na Administração | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo5-dados-na-administracao.html) | [Script](atividade_modulo5.py) | A2 |
| 6 | 7 | Análise exploratória de dados | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo6-analise-exploratoria.html) | [Script](atividade_modulo6.py) | |
| 7 | 8 | Dados estruturados e consulta | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo7-dados-estruturados-e-consulta.html) | [Script](atividade_modulo7.py) | |
| 8 | 9 | Visualização de dados e painéis | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo8-visualizacao-e-paineis.html) | [Script](atividade_modulo8.py) | B1 |
| 9 | 10 | Automação de documentos e processos | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo9-automacao.html) | [Script](atividade_modulo9.py) | |
| 10 | 11 | Pesquisa, documentos longos e análise qualitativa | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo10-pesquisa-e-analise-qualitativa.html) | [Script](atividade_modulo10.py) | B2 |
| 11 | 12 | Aprendizado de máquina e analytics para a decisão | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo11-aprendizado-de-maquina.html) | [Script](atividade_modulo11.py) | |
| 12 | 13 | Governança de dados, LGPD e cibersegurança | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo12-governanca-lgpd-ciberseguranca.html) | [Script](atividade_modulo12.py) | |
| 13 | 14 | Decisão apoiada por IA: contratos, editais e devolutivas | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo13-decisao-apoiada-por-ia.html) | [Script](atividade_modulo13.py) | C1 |
| 14 | 15 | Produto digital e gestão ágil | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo14-produto-digital-e-agil.html) | [Script](atividade_modulo14.py) | |
| 15 | 16 | Projeto integrador | [Slides](https://tadeugomes.github.io/decc0294-tic-administracao/modulo15-projeto-integrador.html) | [Script](atividade_modulo15.py) | C2 |

A página pública da disciplina é <https://tadeugomes.github.io/decc0294-tic-administracao/>: abre `index.html` já renderizado, com os 15 decks a um clique. O GitHub nunca renderiza HTML na visualização do repositório por política de segurança: o link relativo `moduloN-nome.html` mostra o código-fonte, não o deck. Por isso a tabela acima aponta para o Pages. Fora do navegador, baixe o `.html` (botão "Raw" na página do arquivo, depois "Salvar como") e abra com duplo clique.

## Avaliação

São três notas, cada uma com duas entregas. A nota 1 reúne A1, no encontro 3, com peso 40%, e A2, no encontro 6, com peso 60%. A nota 2 reúne B1, no encontro 9, com peso 60%, e B2, no encontro 11, com peso 40%. A nota 3 reúne C1, no encontro 14, com peso 40%, e C2, no encontro 16, com peso 60%.

Cada entrega é conferida pelo script antes de ser recebida. Os comandos `a2`, `b1`, `b2`, `c1` e `c2` listam os arquivos de todos os encontros que compõem aquela nota.

## Referências principais

TAULLI, Tom. Introdução à inteligência artificial: uma abordagem não técnica. São Paulo: Novatec, 2020.

SHARDA, Ramesh; DELEN, Dursun; TURBAN, Efraim. Business intelligence e análise de dados para gestão do negócio. 4. ed. Porto Alegre: Bookman, 2019.

DELEN, Dursun; SHARDA, Ramesh; TURBAN, Efraim. Analytics, data science and artificial intelligence: systems for decision support. 11. ed. Harlow: Pearson, 2020.

SUTHERLAND, Jeff. Scrum: a arte de fazer o dobro do trabalho na metade do tempo. São Paulo: Leya, 2014.

SCHWAB, Klaus. A quarta revolução industrial. São Paulo: Edipro, 2016.

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais.

## Para adaptar a outra disciplina

Os scripts não dependem do contexto da UFMA e funcionam em qualquer turma que use Python. Os decks são gerados por um tema em JavaScript e podem ser refeitos com outra identidade visual, trocando a paleta e o logotipo.

Os roteiros pressupõem laboratório com computador por aluno, permissão para instalar programas e conta individual em cada serviço. Sem isso, os ciclos de prática precisam de outro desenho.

## Licença

Creative Commons Attribution 4.0 International. Use, adapte e redistribua, inclusive comercialmente, mantendo o crédito e indicando as mudanças.

Tadeu Gomes Teixeira, Universidade Federal do Maranhão.
