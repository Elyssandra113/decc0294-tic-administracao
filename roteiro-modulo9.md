# Roteiro do módulo 9

Automação de documentos e processos. Encontro 10, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

Este encontro abre o bloco da nota 3 e não tem entrega avaliada. É o encontro em que a turma sai do relatório pontual e passa para o fluxo repetível.

## Antes da aula

Material do professor: `modulo9-automacao.html`, este roteiro e `atividade_modulo9.py`.

Publicado na turma virtual: o script e o pedido de que cada aluno traga uma tarefa que ele mesmo repete, com periodicidade e tempo gasto. Sem a tarefa trazida, o aluno passa o primeiro ciclo procurando assunto.

Rode `python atividade_modulo9.py iniciar` e depois `gerar` uma vez antes da aula, com um modelo de duas variáveis e três linhas de dados. Ver o arquivo saindo pronto três vezes é o que convence a turma de que o modelo com variáveis não é firula.

Prepare uma planilha de exemplo com uma coluna faltando de propósito, para a demonstração do ciclo 9.2. O script recusa a geração quando um marcador não tem coluna, e essa recusa é conteúdo, não defeito.

Separe também um caso local de automação que deu errado. Sistema que emitiu ofício com nome trocado, boleto duplicado, e-mail em massa com campo não preenchido. O ciclo 9.3 depende de um exemplo concreto de erro em escala.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 9.1 | 45 min | 3 a 8 |
| Ciclo 9.2 | 55 min | 9 a 14 |
| Intervalo | 15 min | |
| Ciclo 9.3 | 45 min | 15 a 20 |
| Intervalo | 10 min | |
| Ciclo 9.4 | 55 min | 21 a 25 |
| Fechamento | 15 min | 26 a 29 |

## Ciclo 9.1 — O que é automatizável de verdade

Teoria, 15 min. A separação entre tarefa e decisão. Os quatro sinais de tarefa automatizável: entrada previsível, regra escrita, saída conferível, repetição com frequência conhecida.

Demonstração, 10 min. O relatório mensal decomposto na projeção, passo a passo, com a turma dizendo o que é coleta, o que é cálculo, o que é redação e o que é julgamento.

Prática, 15 min. Cada aluno decompõe a tarefa que trouxe.

Entrega, 5 min. `entregas/modulo9-ciclo1-decomposicao.md`.

O erro comum é decompor em três passos genéricos ("coletar, analisar, escrever"). Peça grão fino: de onde vem cada número, quem abre qual arquivo, qual é a ordem. Um aluno que escreve oito passos aprendeu mais do que um que escreveu três.

O julgamento não sai da lista. Ele é marcado como julgamento e continua com o humano. Essa marcação é o que separa automação de terceirização de responsabilidade.

## Ciclo 9.2 — Modelos de instrução com variáveis

Teoria, 20 min. O modelo com `[VARIAVEIS]` e as quatro regras: variável com nome de campo real, valor ausente declarado e não inventado, formato de saída fixo, exemplo de saída correta junto do modelo.

Demonstração, 15 min. Um modelo executado três vezes com dados diferentes, na projeção, incluindo a execução com a coluna faltando, para que a turma veja o script recusar e depois preencher com `NAO INFORMADO` e o aviso no topo.

Prática, 15 min. Cada aluno escreve o próprio modelo e roda `gerar` sobre a base que trouxe.

Entrega, 5 min. `entregas/modulo9-ciclo2-modelo.md` e os três documentos gerados.

O aviso de valor ausente é o ponto do ciclo. Documento gerado com buraco silencioso é pior que documento não gerado, porque circula com aparência de completo. Diga isso enquanto o banner aparece na tela.

Este é o ciclo mais longo do encontro e o que mais consome cota do modelo gratuito. Duas requisições longas por aluno bastam. O restante é o script, que não usa modelo nenhum.

## Ciclo 9.3 — Automação de processos e seus limites

Teoria, 25 min. O que é automação robótica de processos e por que ela quebra quando a tela muda. O ponto de conferência humana: onde ele fica, quem assina, o que ele olha.

Prática, 15 min. Cada aluno declara o ponto de conferência do fluxo que está montando e escreve o que a pessoa confere ali, em uma frase verificável.

Entrega, 5 min. `entregas/modulo9-ciclo3-conferencia.md`.

"O gestor revisa" não é ponto de conferência. "O coordenador confere se o total do relatório bate com o extrato do mês" é. Exija o segundo formato.

O caso local de erro em escala entra aqui. A pergunta para a turma é onde estaria o ponto de conferência que teria pegado aquele erro, e por que ele não existia.

## Ciclo 9.4 — Um fluxo repetível, medido

Teoria, 15 min. O que documentar para o fluxo sobreviver a quem o criou. A conta do ponto de equilíbrio: tempo de construção dividido pela economia por execução.

Prática, 30 min. Cada aluno preenche a ficha do fluxo e roda `conferir`. O script calcula em quantas execuções a automação se paga e recusa a entrega se o responsável for "a equipe".

Entrega, 10 min. `entregas/modulo9-ciclo4-fluxo.md`.

O ponto de equilíbrio é a defesa do aluno diante de uma chefia. Quatro horas de construção, vinte minutos economizados por semana, doze execuções para pagar, três meses. Esse cálculo cabe em um e-mail e é o que aprova ou reprova a ideia.

Nome e cargo de responsável são obrigatórios porque fluxo sem dono para de funcionar no primeiro mês em que ninguém roda. O script recusa "a equipe" de propósito.

## O que sai deste encontro

Uma tarefa decomposta em passos com marcação de julgamento. Um modelo de instrução com variáveis, testado em três casos. Um ponto de conferência humana declarado. Um fluxo documentado com ganho medido e ponto de equilíbrio calculado.

Esses quatro arquivos são a matéria-prima do módulo 14 e do projeto integrador. Quem sai daqui sem eles chega ao encontro 15 sem processo para transformar em produto.

## Avisos no fechamento

O encontro 11 fecha a entrega B2, que vale 40% da nota 2. Cada aluno precisa trazer um documento longo do próprio setor, com no mínimo dez páginas, e um arquivo com respostas abertas, se tiver. Sem os dois, o encontro 11 roda com material de reserva e o aluno perde o vínculo com o trabalho dele.

Quem ficou pendente na B1 tem até o encontro 11 para regularizar. Diga isso com a lista na mão.
