# Roteiro do módulo 11

Aprendizado de máquina e analytics para a decisão. Encontro 12, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

Este encontro abre o bloco da nota 3 e não tem entrega avaliada. Ele existe para que a turma saiba o que um modelo preditivo faz, o que ele não faz e quando a resposta certa é não usar modelo nenhum.

## Antes da aula

Material do professor: `modulo11-aprendizado-de-maquina.html`, este roteiro e `atividade_modulo11.py`.

Publicado na turma virtual: o script e o pedido de base própria em CSV, com pelo menos 30 linhas e três colunas de número, uma delas sendo algo que faça sentido prever.

Base de reserva, obrigatória: um CSV com cerca de 40 linhas, uma coluna alvo e duas ou três preditoras com relação real, para quem chegar sem base. Dados públicos de município servem: população, receita, despesa, número de servidores.

Rode `python atividade_modulo11.py prever <base> <alvo>` antes da aula, com a base de reserva, e guarde a saída. O ciclo 11.4 fica mais curto se a turma já viu o formato do relatório.

Prepare também um caso em que o modelo perde para o palpite simples. Basta rodar `prever` usando uma coluna que não tem relação com o alvo. Esse caso é o mais importante da aula e não pode faltar: é ele que separa a turma que entendeu da que decorou.

Este encontro usa pouco ou nenhum modelo de linguagem. O script faz a conta sozinho, sem biblioteca externa. Diga isso à turma no início, porque quem está com cota estourada da semana costuma chegar preocupado.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 11.1 | 45 min | 3 a 8 |
| Ciclo 11.2 | 50 min | 9 a 13 |
| Intervalo | 15 min | |
| Ciclo 11.3 | 45 min | 14 a 18 |
| Intervalo | 10 min | |
| Ciclo 11.4 | 60 min | 19 a 23 |
| Fechamento | 15 min | 24 a 27 |

## Ciclo 11.1 — Descritiva, preditiva e prescritiva

Teoria, 20 min. As três perguntas sobre os mesmos dados: o que aconteceu, o que tende a acontecer, o que fazer. As quatro perguntas que o gestor faz antes de aceitar um número previsto: comparado com quê, com que dados o modelo aprendeu, quanto custa o erro, quem responde pela decisão.

Demonstração, 8 min. A mesma base do encontro 9 lida das três formas, na projeção.

Prática, 12 min. Cada aluno classifica cinco perguntas do próprio setor nas três categorias.

Entrega, 5 min. `entregas/modulo11-ciclo1-classificacao.md`.

Quase toda pergunta que a turma traz como preditiva é descritiva mal formulada. "Quantos atendimentos vamos ter" costuma ser "quantos tivemos e a série está subindo". Aponte isso, porque a maior parte das decisões de gestão se resolve na camada descritiva e não precisa de modelo.

A pergunta "comparado com quê" volta no ciclo 11.4 como o palpite simples. Plante ela aqui.

## Ciclo 11.2 — Os três tipos de aprendizado

Teoria, 30 min. Supervisionado, não supervisionado e por reforço, cada um com um exemplo administrativo. Depois, o que dá errado com mais frequência: rótulo que não existe, viés do passado que vira regra do futuro, variável que é consequência do alvo e não causa, e avaliação feita nos mesmos dados que o modelo já viu.

Prática, 15 min. Cada aluno escolhe a abordagem para o problema que trouxe e justifica em duas frases.

Entrega, 5 min. `entregas/modulo11-ciclo2-abordagem.md`.

A variável que é consequência do alvo é o erro mais silencioso e o mais fácil de demonstrar. Prever faturamento usando comissão paga dá um modelo quase perfeito e inútil, porque a comissão só existe depois da venda. Peça à turma para procurar uma dessas na base própria.

O viés do passado merece um exemplo de seleção de pessoal ou de concessão de benefício, porque volta no módulo 12 junto com a LGPD.

## Ciclo 11.3 — Aprendizado profundo e IA generativa

Teoria, 25 min. O que o aprendizado profundo mudou e por que ele explica o modelo que a turma usa desde o encontro 4. Depois, explicabilidade: quando ela é exigível, o artigo 20 da Lei 13.709 e a motivação obrigatória em compra pública.

Prática, 15 min. Cada aluno analisa um caso do próprio setor e responde se ali um modelo não explicável seria aceitável, e por quê.

Entrega, 5 min. `entregas/modulo11-ciclo3-caso.md`.

A distinção útil é entre decisão que afeta uma pessoa identificada e decisão que afeta um agregado. Prever demanda de estoque não pede explicação individual; negar um benefício pede.

O direito à revisão do artigo 20 é sobre decisão automatizada que afeta interesses do titular. Leia o texto na tela em vez de parafrasear, porque a paráfrase costuma ampliar o alcance do artigo.

## Ciclo 11.4 — Um modelo simples sobre a sua base

Teoria, 12 min. O palpite simples como régua: prever sempre a média. A separação treino e teste e por que avaliar no que o modelo já viu não vale.

Demonstração, 10 min. `prever` sobre a base de reserva na projeção, incluindo o caso em que o modelo perde para o palpite simples.

Prática, 30 min. Cada aluno preenche `modelo/ficha-modelo.md`, roda `prever` sobre a base própria, escreve a seção Leitura do resultado e roda `conferir`.

Entrega, 8 min. `modelo/ficha-modelo.md` e `modelo/resultado.md`.

O script recusa a conferência se o custo de errar para mais e o de errar para menos estiverem com a mesma resposta, e se o aluno declarar que usaria o modelo depois de ele ter perdido do palpite simples sem escrever a ressalva. As duas recusas são o conteúdo do ciclo.

Modelo que perde para a média é resultado válido e deve ser dito assim em voz alta, várias vezes. Aluno que troca de coluna até "dar certo" está aprendendo o hábito errado.

A leitura do coeficiente descreve a base e não prova causa. Repita isso ao ver o primeiro aluno escrever "cada vendedor a mais gera tantos reais".

## O que sai deste encontro

Cinco perguntas classificadas nas três camadas de análise. Uma abordagem de aprendizado escolhida e justificada. Um caso do setor analisado quanto à exigência de explicação. Um modelo treinado sobre base própria, comparado com o palpite simples e lido em duas frases.

## Avisos no fechamento

O encontro 13 trata de governança de dados, LGPD e cibersegurança. Cada aluno precisa levantar, antes da aula, quais dados pessoais passam pelas mãos dele no trabalho ou no estágio, e por onde eles circulam. Basta uma lista, sem nenhum dado real anotado.

Deixe claro que ninguém deve trazer arquivo com dado pessoal de terceiro para a sala. A lista é de tipos de dado e de caminhos, não de conteúdo.
