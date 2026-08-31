# Roteiro do módulo 3

Inteligência artificial, modelos de linguagem e engenharia de prompt. Encontro 4, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

## Antes da aula

Material do professor: `modulo3-ia-e-engenharia-de-prompt.html`, este roteiro e `atividade_modulo3.py`.

Publicado na turma virtual com uma semana de antecedência: o capítulo 1 de Taulli, o script e o aviso de que cada aluno precisa trazer uma referência bibliográfica que use em algum trabalho seu.

Antes do encontro, confira quem ficou pendente na entrega A1 do encontro 3. Aluno sem repositório não consegue gravar nada hoje, e o problema se agrava a cada semana.

Teste o roteiro na semana da aula, não no início do semestre: o provedor gratuito muda de modelo e de limite sem aviso.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 3.1 | 50 min | 3 a 9 |
| Ciclo 3.2 | 50 min | 10 a 15 |
| Intervalo | 15 min | |
| Ciclo 3.3 | 55 min | 16 a 22 |
| Intervalo | 10 min | |
| Ciclo 3.4 | 45 min | 23 a 30 |
| Fechamento | 15 min | 31 a 34 |

## Ciclo 3.1 — O que é IA e o que é um modelo de linguagem

Teoria, 25 min. As três coisas chamadas de IA. O que um modelo de linguagem faz. O que isso explica no uso diário.

Demonstração, 8 min. A mesma instrução rodada duas vezes, em sessões separadas, com as duas respostas gravadas em arquivo.

Prática, 12 min. Cada aluno repete com um conceito da própria área.

Entrega, 5 min. `entregas/modulo3-ciclo1-variacao.md`.

Ponto de atenção: alguém vai concluir que a variação torna a ferramenta inútil. A resposta é que variação de redação não é o problema; variação de fato é. O exercício serve para separar as duas.

## Ciclo 3.2 — Alucinação e verificação

Teoria, 18 min. Os quatro tipos de erro. Por que acontece e o que reduz.

Demonstração, 7 min. A instrução com e sem a autorização do NÃO SEI, sobre a referência que o aluno trouxe. Vale rodar as duas versões na projeção: a diferença costuma ser visível.

Prática, 20 min. Cinco casos no diário, com o script.

Entrega, 5 min. `entregas/modulo3-diario-de-alucinacao.csv` e o `.md` gerado.

O script exige pelo menos três tipos diferentes de erro entre os cinco casos e recusa a coluna de conferência preenchida com "pesquisei". Isso gera reclamação e é o ponto do exercício: a conferência é o produto, não o erro.

Resultado esperado, caso a cota acabe: o aluno registra os casos que conseguiu, anota a indisponibilidade e completa os demais em casa. O mínimo de três tipos continua valendo.

## Ciclo 3.3 — Os quatro elementos de um prompt

Teoria, 22 min. Papel, contexto, instrução e formato. O prompt fraco e o forte lado a lado. Os quatro erros que estragam um prompt bom.

Demonstração, 13 min. A turma dita um prompt fraco e o professor reescreve na projeção, preenchendo a estrutura do slide. Rode as duas versões e compare.

Prática, 15 min. Cada aluno faz o próprio par.

Entrega, 5 min. `prompts/modulo3-par-de-prompts.md`.

Este é o ciclo mais produtivo do módulo e o que mais rende em qualidade de trabalho no resto do semestre. Se algum ciclo precisar ceder tempo, não seja este.

## Ciclo 3.4 — Técnicas e quando cada uma vale

Teoria, 18 min. Exemplos, passo a passo, do simples ao complexo. Verificação em cadeia e consistência. Depois, dois slides de fecho: escolher a técnica pelo erro que ela evita, e a pergunta entre trocar de técnica ou trocar de modelo.

Demonstração, 6 min. A mesma classificação com e sem exemplos.

Prática, 16 min. Três técnicas registradas no caderno de prompts, e uma delas repetida em outro modelo por quem tiver acesso.

Entrega, 5 min. Três arquivos em `prompts/`.

O critério de escolha é o tipo de erro, não o custo. Isso foi decidido assim porque o aluno pode trocar de provedor durante o semestre, e um critério ancorado em cota deixaria de valer no dia em que ele mudasse. O tipo de erro que cada técnica evita continua valendo em qualquer modelo.

O slide sobre trocar de modelo é o mais importante do ciclo. A ordem que ele fixa é instrução, técnica, modelo. Aluno que troca de modelo antes de corrigir a instrução nunca descobre onde estava o problema, e leva esse hábito para a organização onde vai trabalhar.

Se parte da turma estiver em provedores diferentes, aproveite: peça que dois alunos com modelos distintos leiam em voz alta o resultado da mesma instrução. A comparação em sala rende mais que qualquer slide.

## O que sai deste encontro

Uma comparação de variação, um diário de alucinação com cinco casos, um par de prompts e o início do caderno de prompts. Os três primeiros compõem a entrega A2, avaliada no encontro 6.

## Avisos no fechamento

Gravar e publicar antes de sair da sala, com a mensagem "entregas do modulo 3".

Trazer um documento da própria área para o encontro 5: edital, contrato, relatório ou regulamento, em PDF ou Word, sem dado pessoal de terceiro.

A escolha da organização do projeto precisa estar fechada até o encontro 6.
