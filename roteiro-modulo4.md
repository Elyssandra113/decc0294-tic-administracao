# Roteiro do módulo 4

Do prompt ao artefato: arquivos, agentes e configuração. Encontro 5, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

## Antes da aula

Material do professor: `modulo4-do-prompt-ao-artefato.html`, este roteiro e `atividade_modulo4.py`.

Publicado na turma virtual: o script e o lembrete de trazer um documento da própria área, em PDF ou Word, sem dado pessoal de terceiro.

Prepare um documento de reserva, com dez a quinze páginas, para quem esquecer. Um edital de pregão publicado no Portal de Compras serve bem: é público, tem obrigações claras e rende os três estágios da cadeia do ciclo 4.4.

Teste obrigatório numa máquina do laboratório, na semana da aula. O ciclo 4.3 depende de rede, e a rede é o que mais varia:

1. Instale o MCP colando o bloco de configuração e confirme que as quinze ferramentas aparecem. Isso exige Node instalado e acesso ao registro de pacotes.
2. Rode `python atividade_modulo4.py apis testar` e anote quais das oito fontes a rede do CCET alcança.
3. Anote o caminho exato do arquivo de configuração de MCP no opencode desktop, para dizer à turma no slide 23.

Se o laboratório bloquear a instalação do MCP ou os domínios das APIs, o ciclo continua funcionando: a atividade foi desenhada para que o diagnóstico de bloqueio seja parte da entrega. Mas você precisa saber disso antes da aula, não durante.

Confira antes da aula quais alunos ainda não têm o AGENTS.md preenchido do encontro 3. Sem ele, o ciclo 4.2 não funciona, e a correção é rápida se feita antes.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 4.1 | 48 min | 3 a 10 |
| Ciclo 4.2 | 45 min | 11 a 16 |
| Intervalo | 15 min | |
| Ciclo 4.3 | 75 min | 17 a 28 |
| Intervalo | 10 min | |
| Ciclo 4.4 | 40 min | 29 a 34 |
| Fechamento e vocabulário | 15 min | 35 a 40 |

O deck foi refeito para uma turma sem contato anterior com o tema. Entraram cinco slides de conceito, com a tarja CONCEITO, que definem cada termo antes do primeiro uso: artefato, HTML, API, JSON e MCP. Dois slides de vocabulário fecham o encontro.

O ciclo 4.3 concentra quatro desses conceitos e é o mais pesado do encontro em vocabulário novo. A ordem é deliberada: primeiro a API, que é o que existe de fato; depois o JSON, que é o formato em que o dado chega; só então o MCP, que é o embrulho por cima. Quem inverte essa ordem ensina a sigla e não o conceito, e a turma sai achando que MCP é uma fonte de dados.

A analogia do balcão dos fundos, no slide da API, resolve o conceito para a maior parte da turma. A do funcionário novo que ganha acesso a mais um sistema, no slide do MCP, evita a confusão entre dar ferramenta e ficar mais inteligente.

## Ciclo 4.1 — Gerar documentos na pasta do projeto

Conceito, 6 min. O que é um artefato, slide 4. A frase que resume o ciclo está ali: uma tarde de conversa com o modelo pode terminar sem nenhum artefato, e é assim que o trabalho se perde.

Teoria, 12 min. Resposta na tela e arquivo na pasta, slide 5. Os quatro artefatos e quando cada um serve, slide 6. O que é HTML, slide 7, antes da demonstração que gera um arquivo desses.

Demonstração, 7 min. O glossário em HTML, aberto no navegador ali mesmo. Peça um ajuste de coluna sem refazer, para mostrar que o arquivo é editado e não recriado.

Prática, 18 min. Cada aluno gera o glossário da própria área e revisa as doze definições.

Entrega, 5 min. `entregas/glossario.html`.

A instrução da demonstração proíbe o autor de referência de propósito. Explique por quê: é exatamente onde a alucinação apareceria, e o aluno acrescenta depois, conferindo. Três conceitos com autor conferido bastam.

## Ciclo 4.2 — AGENTS.md: configurar o comportamento

Teoria, 15 min. A instrução que não precisa ser repetida. Como se escreve uma regra que funciona.

Demonstração, 6 min. O script `iniciar`, que guarda a cópia da versão 1 e prepara as três tarefas.

Prática, 19 min. Duas rodadas de três tarefas, com correção do arquivo entre elas.

Entrega, 5 min. `AGENTS.md`, `entregas/modulo4-registro.csv` e o relatório gerado.

O critério de que uma regra precisa poder ser violada é o conteúdo central do ciclo. Peça em voz alta que alguém leia uma regra sua e pergunte à turma como ela seria violada. Regra que ninguém consegue violar é intenção, não regra.

O script compara o AGENTS.md com a cópia da versão 1 e aponta se o arquivo não mudou. Quem defender que a versão 1 já estava perfeita precisa escrever isso no relatório, com as notas da rodada 1 sustentando o argumento.

Resultado esperado, se a cota acabar: a rodada 1 é a prioridade. Quem não conseguir rodar a segunda completa em casa e registra a indisponibilidade.

## Ciclo 4.3 — Estender o agente: um MCP e as APIs públicas

Conceito, 12 min. O que é uma API, slide 18, com a analogia do balcão dos fundos. Depois o JSON, slide 19, lendo em voz alta o par nome e valor do exemplo de São Luís. Só então as três formas de estender, slide 20, e o que é um MCP, slide 21, com a analogia do funcionário novo que ganha acesso a mais um sistema.

Teoria, 5 min. A síntese do slide 22, que junta os dois: sem API embaixo, não há MCP em cima. É a frase que o aluno leva para a reunião com fornecedor.

Demonstração da instalação, 12 min. Cole o bloco de configuração na projeção, reinicie e confirme que as quinze ferramentas apareceram. Faça a primeira consulta: o CNPJ da UFMA.

Teoria, 8 min. As cinco linhas de fontes públicas brasileiras. Diga em voz alta que as quatro primeiras abrem sem cadastro e que as duas últimas ficam fora da aula porque cada aluno precisaria da própria chave.

Demonstração do que está por baixo, 8 min. Rode `apis testar` e depois `apis municipios MA`. O ponto do ciclo está aqui: a URL que o script imprime é a mesma que a ferramenta do MCP executaria. Escreva a URL no quadro.

Teoria, 5 min. Os quatro critérios de decisão.

Prática, 20 min. Instalação, diagnóstico, consulta pelas duas vias e ficha de decisão.

Entrega, 5 min. `entregas/modulo4-ciclo3-decisao.md`, `dados/api-diagnostico.md` e os arquivos de resposta.

Três coisas para conduzir bem.

A ordem importa: MCP primeiro, API depois. O aluno vê a mágica, e então descobre que embaixo dela havia um endereço que ele mesmo poderia ter chamado. Invertendo a ordem, a aula vira introdução a protocolo HTTP e perde a turma.

A instalação vai falhar em algumas máquinas. Isso é normal e está previsto: a entrega aceita o registro da falha, e o script funciona sem o MCP. Não pare a turma para resolver caso individual, e não deixe ninguém parado esperando: quem travou segue pelo script.

A pergunta sobre quem responde pelo acesso costuma ser ignorada. Insista: é a que separa um administrador de um entusiasta. Conectar um agente ao sistema da organização é decisão de segurança da informação, e o aluno vai ser o gestor que assina ou não assina essa decisão.

Ressalva sobre o material: os endereços das oito fontes foram tirados da documentação oficial de cada uma, mas não puderam ser executados durante a produção deste material. O teste na máquina do laboratório, descrito em Antes da aula, é o que confirma que funcionam.

## Ciclo 4.4 — Tarefas encadeadas e subagentes

Teoria, 15 min. Por que quebrar em etapas. As quatro regras de uma cadeia.

Demonstração, 5 min. As três instruções em sequência sobre o documento do professor.

Prática, 15 min. Cada aluno roda a cadeia no próprio documento.

Entrega, 5 min. `entregas/modulo4-cadeia.md` e o procedimento no caderno.

Exija que os três critérios de aceitação sejam escritos antes de rodar. Quem escrever depois produz critérios que a resposta já cumpre, e o exercício perde o sentido.

Três etapas custam três pedidos. Avise antes: a cadeia se roda uma vez, com o documento certo, e não como teste.

## O que sai deste encontro

Um glossário em HTML, um AGENTS.md testado em duas rodadas, um MCP instalado com a mesma consulta feita também pela API, um diagnóstico do que a rede do laboratório bloqueia, uma ficha de decisão sobre estender ou não a ferramenta, e uma cadeia de três etapas documentada.

## Avisos no fechamento

O encontro 6 fecha a nota 1 com a entrega A2. Liste em voz alta o que ela reúne: mapa de tarefas do módulo 1, diário e par de prompts do módulo 3, AGENTS.md do módulo 4, e o mapa de dados que será feito no próprio encontro 6.

A organização do projeto precisa estar definida. Depois do encontro 6, mudar custa refazer o mapa de dados.

Trazer uma planilha ou base da organização escolhida, com pelo menos vinte linhas e sem dado pessoal identificável. Quem não tiver, traz o endereço de uma base pública.
