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

Deck `modulo2-ambiente-de-trabalho-digital.pptx`, este roteiro e o arquivo `atividade_modulo2.py`, publicado na turma virtual antes da aula.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 2.1 | 45 min | 3 a 8 |
| Ciclo 2.2 | 45 min | 9 a 15 |
| Intervalo | 15 min | |
| Ciclo 2.3 | 65 min | 16 a 23 |
| Intervalo | 10 min | |
| Ciclo 2.4 | 65 min | 24 a 30 |
| Fechamento | 15 min | 31 a 34 |

## Ciclo 2.1 — Infraestrutura de TI: o que roda onde

Teoria, 20 min. Os três lugares. As quatro parcelas do custo total.

Demonstração, 5 min. A própria ferramenta da disciplina submetida à pergunta: o programa roda na máquina, o modelo roda na nuvem, a conta é gratuita com cota.

Prática, 15 min. Cada aluno escolhe um sistema que usa e responde às três perguntas.

Entrega, 5 min. Ficha de infraestrutura, salva depois que a pasta existir.

Este ciclo é o mais compressível do encontro. Se o teste de sanidade indicou instalação demorada, reduza a teoria para 12 minutos e a prática para 10.

## Ciclo 2.2 — A pasta do projeto

Teoria, 20 min. Conversa, pasta e repositório. A estrutura padrão. Os formatos.

Demonstração, 8 min. O professor executa `atividade_modulo2.py criar` na projeção.

Prática, 12 min. Cada aluno cria a pasta, roda o script e preenche o README.

Entrega, 5 min. Estrutura criada e README preenchido.

Ponto de atenção: nome de pasta com espaço e acento causa problema o semestre inteiro. Insista no padrão minúsculas com hífen no momento em que a turma criar a pasta.

## Ciclo 2.3 — opencode desktop: instalação e primeiro uso

Teoria, 15 min. O que o agente faz sobre a pasta. Cota, limite e o que fazer quando acabar.

Demonstração e instalação assistida, 25 min. Os seis passos do slide 19, com toda a turma acompanhando na própria máquina. Monitor circulando. Ninguém avança sozinho.

Demonstração da primeira instrução, 5 min. O pedido do slide 20, que lê um arquivo da pasta e grava outro.

Prática, 15 min. Cada aluno preenche o AGENTS.md e testa com três pedidos.

Entrega, 5 min. AGENTS.md preenchido e três testes salvos em `prompts/`.

Resultado esperado, se a cota do modelo falhar em parte da turma: os alunos afetados escrevem o AGENTS.md mesmo assim e fazem os três testes na aula seguinte. Registram a indisponibilidade na entrega. A instalação e a autenticação são o que não pode ficar pendente.

## Ciclo 2.4 — GitHub Desktop e a entrega A1

Teoria, 15 min. Os três problemas que o versionamento resolve. Os quatro gestos. O que nunca vai para o repositório.

Demonstração e execução assistida, 30 min. Os seis passos do slide 27, com a turma acompanhando. Este é o trecho em que o encontro trava ou não trava.

Conferência, 15 min. Cada aluno roda `atividade_modulo2.py conferir` e corrige o que o script apontar. O script verifica nove itens e escreve `entregas/A1-relatorio.md`.

Entrega, 5 min. Endereço do repositório enviado na turma virtual, ainda em sala.

Ordem de resolução quando alguém trava: primeiro o que impede publicar, depois o preenchimento de arquivos. Um aluno com AGENTS.md incompleto resolve em casa. Um aluno sem conta no GitHub não resolve.

## Os nove itens que o script confere

Estrutura de pastas, README preenchido, AGENTS.md com as quatro seções, as quatro entregas do módulo 1 na pasta certa, ficha do ciclo 2.1, .gitignore presente, pasta sob controle de versão, ao menos duas versões gravadas e repositório publicado.

O script lê o estado do repositório direto dos arquivos internos do git, sem depender de comando. Funciona mesmo sem git instalado no caminho do sistema.

## Problemas conhecidos

Antivírus bloqueia o instalador. Não autorizar por conta própria: chamar o professor, que resolve com o técnico.

E-mail de confirmação não chega. Verificar spam, esperar cinco minutos, trocar de endereço e seguir.

Agente diz que não encontra o arquivo. Quase sempre a pasta aberta não é a do projeto.

GitHub Desktop não deixa publicar. Faltou autenticar, ou não há nenhuma versão gravada ainda.

Cota do modelo esgotada. Registrar na entrega e seguir com o roteiro.

## Depois da aula

Confira os repositórios recebidos antes do encontro 4 e identifique quem ficou pendente. Quem não publicou precisa resolver na semana, com atendimento fora de aula. Não deixe passar para o encontro 5: o módulo 3 já grava trabalho na pasta.
