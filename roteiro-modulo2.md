# Roteiro do módulo 2

Ambiente de trabalho digital. Encontro 3, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

Este é o encontro crítico do semestre. Ao final dele todo aluno precisa sair com opencode desktop instalado, conta criada, pasta do projeto montada e repositório publicado. Quem não sair assim não acompanha os encontros seguintes.

## Antes da aula, obrigatoriamente

Teste de sanidade numa máquina do laboratório, com o técnico presente, cronometrando:

1. Baixar e instalar o opencode desktop. Anote se o antivírus bloqueia e o que foi preciso fazer.
2. Criar conta e autenticar o modelo gratuito. Anote o tempo e o limite de cota informado.
3. Baixar e instalar o GitHub Desktop. Criar conta, adicionar uma pasta, gravar e publicar.
4. Verificar se as máquinas são restauradas a cada uso. Se forem, providenciar imagem com os dois aplicativos ou combinar reinstalação no início da aula.

O tempo medido nesse teste decide se o ciclo 2.4 cabe nos 65 minutos previstos. Se passar de 25 minutos por máquina, reduza o ciclo 2.1 e transfira o tempo.

Providencie também: os endereços de download escritos na turma virtual, um monitor circulando pela sala e a instrução de como adicionar o professor como colaborador no repositório.

## Material

Deck `modulo2-ambiente-de-trabalho-digital.html`, este roteiro e o arquivo `atividade_modulo2.py`, publicado na turma virtual antes da aula.

O deck foi refeito para uma turma sem contato anterior com o tema. Ele agora tem sete slides de conceito, marcados com a tarja CONCEITO, que definem cada termo antes do primeiro uso: infraestrutura de TI, nuvem, arquivo e caminho, texto puro, modelo de linguagem, agente, controle de versão e a diferença entre git, GitHub e repositório. Dois slides de vocabulário fecham o encontro, com os quinze termos e a definição de cada um.

Os slides de conceito são para ler em voz alta e discutir, não para passar rápido. A frase grande no topo é a definição; os quatro pontos abaixo são o que a sustenta; a caixa dourada no pé é a analogia, que é o que a turma vai lembrar na semana seguinte. Peça um exemplo da turma em cada analogia antes de avançar.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura, visão geral e combinado | 10 min | 1 a 3 |
| Ciclo 2.1 | 45 min | 4 a 12 |
| Ciclo 2.2 | 45 min | 13 a 21 |
| Intervalo | 15 min | |
| Ciclo 2.3 | 65 min | 22 a 31 |
| Intervalo | 10 min | |
| Ciclo 2.4 | 65 min | 32 a 40 |
| Fechamento e vocabulário | 15 min | 41 a 46 |

O slide 3 é o combinado de abertura: toda palavra técnica é definida antes de ser usada, ninguém precisa saber programar e a dúvida óbvia é a mais útil. Leia os quatro pontos em voz alta. Numa turma que nunca viu o tema, esse minuto reduz a quantidade de gente que fica calada com dúvida.

## Ciclo 2.1 — Infraestrutura de TI: o que roda onde

Conceito, 12 min. O que é infraestrutura de TI, slide 5, com equipamento, programa, rede e dado. Depois a separação entre programa, arquivo e sistema, slide 6.

Teoria, 15 min. Os três lugares onde um programa roda, slide 7. O slide 8 define computação em nuvem, e é o mais importante do ciclo: a turma chega achando que nuvem é uma abstração, e sai sabendo que é o galpão de uma empresa com contrato. Depois as quatro parcelas do custo total, slide 9.

Demonstração, 5 min. A própria ferramenta da disciplina submetida à pergunta: o programa roda na máquina, o modelo roda na nuvem, a conta é gratuita com cota.

Prática, 15 min. Cada aluno escolhe um sistema que usa e responde às três perguntas.

Entrega, 5 min. Ficha de infraestrutura, salva depois que a pasta existir.

Este ciclo é o mais compressível do encontro. Se o teste de sanidade indicou instalação demorada, corte o slide 9, o do custo total, que é o único que não é pré-requisito de nada adiante. Os slides de conceito não se cortam: sem eles, o ciclo 2.3 não se sustenta.

## Ciclo 2.2 — A pasta do projeto

Conceito, 10 min. Arquivo, pasta e caminho, slide 14. É o slide mais elementar do encontro e o mais decisivo: sem ele, nenhuma instrução ao agente funciona, porque o aluno não sabe citar um arquivo. Escreva um caminho no quadro, dados/vendas-2025.csv, e peça que alguém leia em voz alta o que ele significa.

Teoria, 15 min. Conversa, pasta e repositório, slide 15. A estrutura padrão, slide 16. Texto puro e arquivo fechado, slide 17, que explica por que a disciplina trabalha em .md e .csv. Os formatos, slide 18.

Demonstração, 8 min. O professor executa `atividade_modulo2.py criar` na projeção.

Prática, 12 min. Cada aluno cria a pasta, roda o script e preenche o README.

Entrega, 5 min. Estrutura criada e README preenchido.

Ponto de atenção: nome de pasta com espaço e acento causa problema o semestre inteiro. Insista no padrão minúsculas com hífen no momento em que a turma criar a pasta.

## Ciclo 2.3 — opencode desktop: instalação e primeiro uso

Conceito, 12 min. O que é um modelo de linguagem, slide 23, na versão curta: ele prevê a continuação provável do texto e não consulta uma base de verdades. Depois, o que é um agente, slide 24, com a diferença entre ser o carregador de informação e ser o revisor.

A analogia do estagiário, no slide 23, costuma resolver o conceito para a turma inteira. Não a substitua por uma explicação técnica.

Teoria, 8 min. O que o opencode faz, slide 25. Cota, limite e o que fazer quando acabar, slide 26.

Demonstração e instalação assistida, 22 min. Os seis passos do slide 27, com toda a turma acompanhando na própria máquina. Monitor circulando. Ninguém avança sozinho.

Demonstração da primeira instrução, 5 min. O pedido do slide 28, que lê um arquivo da pasta e grava outro. Leia a instrução em voz alta apontando as três partes: o arquivo citado pelo caminho, o formato pedido e a proibição no fim.

Prática, 15 min. Cada aluno preenche o AGENTS.md e testa com três pedidos.

Entrega, 5 min. AGENTS.md preenchido e três testes salvos em `prompts/`.

Resultado esperado, se a cota do modelo falhar em parte da turma: os alunos afetados escrevem o AGENTS.md mesmo assim e fazem os três testes na aula seguinte. Registram a indisponibilidade na entrega. A instalação e a autenticação são o que não pode ficar pendente.

## Ciclo 2.4 — GitHub Desktop e a entrega A1

Conceito, 10 min. O que é versionar, slide 33, começando pela pilha de relatorio-final-v3 que todo mundo tem. Depois o slide 34, git, GitHub e repositório, que é onde a turma se perde na primeira semana: um é o programa, outro é o site, o terceiro é a sua pasta com histórico.

Teoria, 10 min. Os três problemas que o versionamento resolve, slide 35. Os quatro gestos, slide 36, com os nomes em inglês porque é assim que estão nos botões. O que nunca vai para o repositório, slide 38.

Demonstração e execução assistida, 30 min. Os seis passos do slide 37, com a turma acompanhando. Este é o trecho em que o encontro trava ou não trava.

Conferência, 15 min. Cada aluno roda `atividade_modulo2.py conferir` e corrige o que o script apontar. O script verifica nove itens e escreve `entregas/A1-relatorio.md`.

Entrega, 5 min. Endereço do repositório enviado na turma virtual, ainda em sala.

Ordem de resolução quando alguém trava: primeiro o que impede publicar, depois o preenchimento de arquivos. Um aluno com AGENTS.md incompleto resolve em casa. Um aluno sem conta no GitHub não resolve.

## Os nove itens que o script confere

Estrutura de pastas, README preenchido, AGENTS.md com as quatro seções, as quatro entregas do módulo 1 na pasta certa, ficha do ciclo 2.1, .gitignore presente, pasta sob controle de versão, ao menos duas versões gravadas e repositório publicado.

O script lê o estado do repositório direto dos arquivos internos do git, sem depender de comando. Funciona mesmo sem git instalado no caminho do sistema.

## O vocabulário do fim

Os slides 42 e 43 trazem os quinze termos do encontro com uma linha de definição em cada. Não são para explicar de novo: são para o aluno fotografar e consultar durante o semestre. Reserve dois minutos, diga isso com essas palavras e siga.

Se algum termo gerar dúvida ali, é sinal de que o slide de conceito correspondente passou rápido demais. Anote qual foi e ajuste o ritmo no próximo semestre.

## Problemas conhecidos

Antivírus bloqueia o instalador. Não autorizar por conta própria: chamar o professor, que resolve com o técnico.

E-mail de confirmação não chega. Verificar spam, esperar cinco minutos, trocar de endereço e seguir.

Agente diz que não encontra o arquivo. Quase sempre a pasta aberta não é a do projeto.

GitHub Desktop não deixa publicar. Faltou autenticar, ou não há nenhuma versão gravada ainda.

Cota do modelo esgotada. Registrar na entrega e seguir com o roteiro.

## Depois da aula

Confira os repositórios recebidos antes do encontro 4 e identifique quem ficou pendente. Quem não publicou precisa resolver na semana, com atendimento fora de aula. Não deixe passar para o encontro 5: o módulo 3 já grava trabalho na pasta.
