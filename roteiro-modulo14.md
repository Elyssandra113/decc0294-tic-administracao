# Roteiro do módulo 14

Produto digital e gestão ágil. Encontro 15, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

Encontro sem entrega avaliada isolada. Tudo que sai daqui entra na C2 do encontro 16, que vale 60% da nota 3. É também a última janela para regularizar pendências da C1.

## Antes da aula

Material do professor: `modulo14-produto-digital-e-agil.html`, este roteiro e `atividade_modulo14.py`.

Publicado na turma virtual, com uma semana de antecedência: o script e o pedido de que cada aluno escolha o processo que vai virar produto e anote quem é o usuário, pelo cargo, o que ele faz hoje, quantas vezes por semana e quanto tempo leva. Quem chega sem isso passa o primeiro ciclo escolhendo tema.

Monte um backlog de exemplo antes da aula e rode `priorizar`. Escolha valores e esforços em que a ordem calculada discorde da marcação de versão 1, para mostrar a mensagem sobre dependência entre histórias.

Prepare a lista de pendências da C1, aluno por aluno, tirada da rodada `c1` do encontro anterior. Entregue no início do encontro, por escrito.

O ciclo 14.3 é o mais longo de construção do semestre e depende da cota do modelo. Avise na semana anterior que quem chegar com a cota do dia gasta vai construir com menos ajuda.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 14.1 | 45 min | 3 a 8 |
| Ciclo 14.2 | 50 min | 9 a 13 |
| Intervalo | 15 min | |
| Ciclo 14.3 | 50 min | 14 a 17 |
| Intervalo | 10 min | |
| Ciclo 14.4 | 55 min | 18 a 21 |
| Fechamento | 15 min | 22 a 25 |

## Ciclo 14.1 — De processo a produto

Teoria, 15 min. A diferença entre processo e produto. As quatro perguntas: quem é o usuário pelo cargo, o que ele faz hoje e quanto custa, o que ele deixa de fazer, como se saberá que funcionou.

Demonstração, 10 min. A ficha na projeção, com o corte de escopo feito ao vivo sobre um caso da turma.

Prática, 15 min. Cada aluno preenche a ficha.

Entrega, 5 min. `entregas/ficha-produto.md`.

O usuário descrito como "os gestores" é o erro previsível e o script recusa. Insista no cargo: é ele que define o que precisa estar escrito no produto e quem vai testar no ciclo 14.4.

A medida do caminho atual é o que permite dizer depois se o produto ajudou. Quem não mediu no encontro 10 mede por estimativa agora, e registra que é estimativa.

O corte de escopo é a decisão de produto do encontro. Uma tarefa completa vale mais que três pela metade, e o que sai não é apagado, vai para o backlog.

## Ciclo 14.2 — Backlog e critério de aceite

Teoria, 20 min. O que a gestão ágil resolve, segundo Sutherland: requisito que muda, ciclo curto, lista priorizada, retrospectiva. Depois, o formato da história e o critério de aceite.

Prática, 25 min. Cada aluno escreve de cinco a dez histórias com critério de aceite e roda `priorizar`.

Entrega, 5 min. `entregas/backlog.csv`.

A parte "para [resultado]" é a que a turma esquece e a única que justifica construir. O script recusa a história sem ela, e vale ler duas ou três em voz alta para mostrar a diferença entre pedir solução e descrever necessidade.

"Funcionar bem" como critério de aceite aparece em quase todo backlog na primeira rodada. Pergunte quem verificaria isso, e como, sem o aluno por perto.

A ordem por valor sobre esforço é sugestão, e não decisão. Quando a marcação do aluno discorda da ordem calculada, a resposta certa costuma ser dependência entre histórias, e isso se escreve no backlog em vez de se mudar o número.

## Ciclo 14.3 — A primeira versão, construída

Teoria, 10 min. Como conduzir o agente numa construção: uma história por vez com o critério de aceite junto, commit ao fim de cada uma, teste com dado errado, instrução de uso dentro do produto.

Prática, 40 min. Construção.

Entrega, incluída na prática. O produto rodando e os commits.

Circule pela sala olhando as instruções que os alunos escrevem ao agente. A que produz resultado ruim quase sempre omitiu o critério de aceite.

O teste com dado errado é o que separa exercício de produto. Peça a cada aluno que rode uma vez com campo vazio, número com vírgula e arquivo com acento no nome, antes de dizer que a história está pronta.

O commit por história é a regra. Quem faz um commit só no fim perde a capacidade de voltar, e é o que mais atrapalha no encontro 16.

Alunos que ficarem sem cota continuam: o que falta é ajuste, e o roteiro de cada passo já traz o resultado esperado.

## Ciclo 14.4 — Teste com usuário e iteração

Teoria, 12 min. Como conduzir um teste com uma pessoa só: tarefa concreta, silêncio, observação. O que registrar e como priorizar bloqueio antes de incômodo.

Prática, 38 min. Em duplas, cada um usa o produto do outro. Depois, individual, o registro e a atualização do backlog.

Entrega, 5 min. `entregas/registro-teste.md`.

A instrução mais difícil de cumprir é ficar calado. Circule e interrompa quem estiver explicando o próprio produto ao colega. Cada ajuda apaga um problema que vai reaparecer com o próximo usuário.

Teste em que nada travou significa quase sempre tarefa fácil demais ou ajuda dada. O script recusa registro sem achado, e a saída certa é refazer com tarefa mais difícil, não escrever um achado inventado.

A retrospectiva fecha o ciclo. A pergunta é o que atrapalhou a construção, e a resposta mais comum, começar pela formatação antes de a leitura do dado estar pronta, é útil para a turma inteira ouvir.

## O que sai deste encontro

A ficha do produto com usuário pelo cargo e caminho atual medido. O backlog com histórias no formato e critérios de aceite verificáveis, priorizado. A versão 1 funcionando, com commits por história. O registro do teste com achados classificados e a próxima versão definida.

## Avisos no fechamento

O encontro 16 é o projeto integrador e fecha a C2, 60% da nota 3. Antes dele, cada aluno precisa fechar a versão 2 com pelo menos os bloqueios do teste resolvidos, montar a apresentação de dez minutos (problema, o que existe hoje, o que construiu, o que ainda não funciona) e preparar a demonstração ao vivo, incluindo o caso com dado errado.

Diga que a demonstração do produto recusando entrada inválida vale mais na avaliação que a tela bonita, porque é isso que se avalia.

Quem ainda tem pendência da C1 entrega até o encontro 16. Depois disso a nota 3 fecha com o que estiver na pasta.
