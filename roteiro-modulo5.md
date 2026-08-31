# Roteiro do módulo 5

Dados na Administração. Encontro 6, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

Este encontro fecha a nota 1 com a entrega A2.

## Antes da aula

Material do professor: `modulo5-dados-na-administracao.html`, este roteiro e `atividade_modulo5.py`.

Publicado na turma virtual: o script e o lembrete de trazer uma planilha ou base da organização escolhida, com pelo menos vinte linhas e sem dado pessoal identificável.

Prepare uma base de reserva para quem não trouxer, e um arquivo de reserva das bases públicas para o caso de a rede bloquear as APIs. O diagnóstico do encontro 5 já diz quais fontes o laboratório alcança: use aquele resultado.

Confira a situação de cada aluno nas entregas dos módulos 1, 3 e 4. Quem chegar hoje com pendência acumulada não fecha a A2, e o script vai apontar item por item. É melhor avisar antes do encontro do que descobrir no último ciclo.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 5.1 | 45 min | 3 a 8 |
| Ciclo 5.2 | 50 min | 9 a 14 |
| Intervalo | 15 min | |
| Ciclo 5.3 | 50 min | 15 a 21 |
| Intervalo | 10 min | |
| Ciclo 5.4 | 55 min | 22 a 25 |
| Fechamento | 15 min | 26 a 29 |

## Ciclo 5.1 — De onde nasce o dado da organização

Teoria, 18 min. As três origens e o erro típico de cada uma. As três formas do dado.

Demonstração, 7 min. Montar uma linha de inventário na projeção, com a regra do NÃO INFORMADO.

Prática, 15 min. Três fontes da organização de cada aluno.

Entrega, 5 min. `entregas/modulo5-ciclo1-inventario.csv`.

O conteúdo do ciclo é a regra do NÃO INFORMADO. Metade da turma vai deixar o agente preencher o que não sabe, e o inventário resultante parece completo e é ficção. Diga em voz alta: a lista de lacunas vale mais que a de certezas, porque é ela que vira pergunta na organização.

## Ciclo 5.2 — Onde os dados moram e como saem de lá

Teoria, 18 min. As quatro etapas do caminho do dado até a decisão. As três formas de tirar o dado do sistema.

Demonstração, 8 min. Baixar a lista de municípios e cruzar com uma base da turma. Os não encontrados são o ponto da demonstração.

Prática, 19 min. Cada aluno baixa a base pública que serve ao projeto e cruza com a sua.

Entrega, 5 min. `entregas/modulo5-ciclo2-cruzamento.md`.

O slide das quatro etapas costuma provocar reconhecimento imediato na turma que trabalha. Aproveite: peça que alguém conte um caso em que ninguém conseguiu explicar de onde veio um número. É o melhor gancho para o mapa de dados do ciclo 5.4.

Se a rede bloquear as APIs, use os arquivos de reserva. O cruzamento continua funcionando, e a limitação de rede entra no mapa como restrição declarada.

## Ciclo 5.3 — Qualidade e governança de dados

Teoria, 25 min. As cinco dimensões de qualidade. Os três papéis da governança. As três perguntas da LGPD.

Prática, 20 min. Cada aluno mede completude e unicidade na própria base e confere dois números na mão.

Entrega, 5 min. `entregas/modulo5-ciclo3-qualidade.md`.

A conferência manual de dois números é obrigatória e é onde o ciclo prova o que ensina. Sem ela o aluno aceita o percentual que o agente calculou, que é exatamente o hábito que a disciplina combate.

A parte de LGPD aqui é operacional, não jurídica. O aprofundamento vem no módulo 12. O que precisa acontecer hoje é uma coisa só: quem tiver CPF, telefone ou endereço na base apaga a coluna agora, antes de gravar no repositório.

## Ciclo 5.4 — Mapa de dados e fechamento da entrega A2

Teoria, 10 min. O que um mapa de dados resolve.

Demonstração, 8 min. Os três comandos do script, incluindo o `a2`.

Prática, 32 min. Preencher o mapa e rodar as duas conferências.

Entrega, 5 min. Repositório publicado com a mensagem "entrega A2".

Reserve os últimos vinte minutos para o comando `a2`. Ele percorre doze itens dos módulos 1, 3, 4 e 5 e imprime o que falta. É a rede de segurança do bloco, e quem rodar cedo tem tempo de corrigir.

O script recusa linha de mapa sem data de extração e sem responsável. Os dois campos são o que torna a análise refazível seis meses depois, e é essa a razão a dar quando alguém reclamar.

Aceite NÃO INFORMADO em dono e custodiante. O mapa registra a lacuna e pergunta a quem o aluno perguntaria. Descobrir quem responde pelo dado é trabalho de campo, não pré-requisito da entrega.

## O que sai deste encontro

Inventário de três fontes, uma base pública baixada e cruzada, um diagnóstico de qualidade com conferência manual, e o mapa de dados com quatro fontes. Somados às entregas dos módulos 1, 3 e 4, fecham a A2 e a nota 1.

## Avisos no fechamento

A organização do projeto está definida a partir de hoje. Trocar depois custa refazer o mapa de dados.

Deixar a base tratada em `dados/` para o encontro 7: é sobre ela que se trabalha, e não sobre outra.

Escrever três perguntas de gestão que o projeto deve responder. São o ponto de partida do próximo encontro.

Quem ficar com item pendente da A2 tem a semana seguinte para corrigir.
