# Roteiro do módulo 13

Decisão apoiada por IA: contratos, editais e devolutivas. Encontro 14, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

Este encontro fecha a entrega C1, que vale 40% da nota 3 e reúne os encontros 12, 13 e 14.

## Antes da aula

Material do professor: `modulo13-decisao-apoiada-por-ia.html`, este roteiro e `atividade_modulo13.py`.

Publicado na turma virtual, com uma semana de antecedência: o script, o pedido do documento de decisão (dez páginas ou mais, sem dado pessoal) e o pedido do critério de decisão escrito antes da aula, em três linhas. Esse critério escrito em casa é o que torna o ciclo 13.1 uma comparação em vez de um exercício.

Material de reserva: um edital ou contrato público completo, com anexo técnico, e três propostas fictícias construídas por você. As propostas precisam ser desenhadas para que a vencedora mude no teste de sensibilidade, porque esse é o resultado que ensina.

Rode `matriz` e `avaliar` antes da aula com a matriz de reserva. Confira que o teste de sensibilidade vira a vencedora quando o peso do preço sobe. Se não virar, ajuste as notas até virar.

Confira quem tem pendência dos encontros 12 e 13. A C1 conferida pelo script aponta arquivo por arquivo, e é melhor que a lista apareça no início do encontro do que nos últimos dez minutos.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 13.1 | 45 min | 3 a 8 |
| Ciclo 13.2 | 50 min | 9 a 13 |
| Intervalo | 15 min | |
| Ciclo 13.3 | 45 min | 14 a 19 |
| Intervalo | 10 min | |
| Ciclo 13.4 | 60 min | 20 a 23 |
| Fechamento e C1 | 15 min | 24 a 26 |

## Ciclo 13.1 — O critério vem antes da alternativa

Teoria, 15 min. Por que a ordem importa, a exigência de motivação do artigo 50 da Lei 9.784, e a matriz com critério, peso, nota e sensibilidade.

Demonstração, 10 min. A matriz de reserva montada na projeção, com `matriz` e `avaliar`.

Prática, 15 min. Cada aluno escreve os critérios e pesos do próprio caso.

Entrega, 5 min. `entregas/matriz-decisao.csv`.

Peça que ninguém dê nota nenhuma antes de os pesos estarem escritos e justificados. Quem inverte a ordem produz uma planilha que confirma a escolha que já tinha feito, e isso é o oposto do exercício.

A comparação com o critério trazido de casa costuma render a melhor discussão do encontro. Pergunte quantos mudaram de critério depois de ler o documento, e o que os fez mudar.

Critério com nome de qualidade ("boa proposta", "confiabilidade") precisa ser convertido em algo verificável no documento. Faça duas ou três dessas conversões em voz alta.

## Ciclo 13.2 — Leitura crítica de documento de decisão

Teoria, 15 min. As cinco categorias: obrigações com prazo, pagamento e reajuste, penalidades e rescisão, escopo e exclusões, fiscalização e aceite.

Demonstração, 10 min. A extração com trecho de origem, na projeção, com a instrução completa mostrada no slide.

Prática, 20 min. Cada aluno mapeia o documento que trouxe, por seção.

Entrega, 5 min. `entregas/mapa-documento.md`.

A frase "não preencha com o que costuma constar" precisa ser lida em voz alta e explicada. Sem ela, o modelo completa o documento com o edital médio que viu no treino, e o aluno acredita ter encontrado cláusulas que não existem.

O NAO CONSTA é o achado mais valioso do ciclo. Em quase todo contrato falta a lista de exclusões de escopo, e é dali que sai o aditivo. Peça exemplos da turma.

A conferência dos três trechos é obrigatória e alguém sempre encontra uma citação inventada. Quando aparecer, mostre para a turma inteira, sem constranger o aluno: é a demonstração mais convincente da disciplina.

## Ciclo 13.3 — A devolutiva escrita e assinada

Teoria, 20 min. As quatro seções da devolutiva. Depois, o que o modelo escreve bem e o que ele não pode escrever.

Prática, 20 min. Cada aluno escreve a devolutiva do próprio caso.

Entrega, 5 min. `entregas/devolutiva.md`.

"Escreva a conclusão antes de pedir redação" é a instrução do ciclo. O modelo redige em volta da conclusão do aluno, não no lugar dela. Quem pedir a conclusão ao modelo vai receber uma que soa bem e não é dele, e isso aparece na leitura.

O campo `norma_conferida_em` é obrigatório e o script cobra. Artigo trocado em parecer é o erro mais frequente do uso de IA no serviço público, e o mais difícil de perceber, porque o texto errado é sempre plausível.

A declaração de uso da ferramenta é regra da disciplina e está no programa. Uma linha basta, e ela precisa dizer o que a ferramenta fez, não que ela foi usada.

## Ciclo 13.4 — Entrega C1

Teoria, 10 min. O teste de sensibilidade e os quatro resultados possíveis, incluindo o empate técnico.

Prática, 40 min. Notas com razão e fonte, `avaliar`, recomendação escrita na devolutiva, `conferir` e depois `c1`.

Entrega, 10 min. A pasta inteira, conferida pelo script.

Quando a vencedora muda no teste, o aluno costuma querer mexer nos pesos até ela parar de mudar. Interrompa. A decisão frágil é uma informação sobre a decisão, e escondê-la é o que a auditoria procura.

O empate técnico abaixo de cinco por cento aparece em uma parte da turma e é resultado legítimo. A saída é um critério novo declarado, e não a terceira casa decimal.

Reserve os últimos dez minutos para a rodada `c1` de cada aluno. O script lista os onze arquivos dos três encontros e diz qual falta.

## O que sai deste encontro

Uma matriz com critérios, pesos justificados e notas com fonte no documento. O resultado com ranking e teste de sensibilidade. O mapa do documento nas cinco categorias, com trechos de origem e ausências marcadas. Uma devolutiva fundamentada, com norma conferida e uso de ferramenta declarado.

Com a C1 fechada, resta 60% da nota 3, na C2 do encontro 16.

## Avisos no fechamento

O encontro 15 trata de produto digital e gestão ágil. Cada aluno precisa escolher, antes da aula, o processo que vai virar produto no projeto integrador, e anotar quem é o usuário: cargo, o que ele faz hoje, quantas vezes por semana, quanto tempo leva.

Quem ficou com pendência na C1 tem o encontro 15 como última janela antes do fechamento da nota. Diga isso com a lista do script na mão.
