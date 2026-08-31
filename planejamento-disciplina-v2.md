# Planejamento revisado

DECC0294, Tecnologia da Informação e Comunicação Aplicada à Administração, turma 2026.2 T01. Dezesseis encontros de cerca de quatro horas, em laboratório, com opencode desktop e GitHub Desktop.

## 1. O que foi lido

O programa vigente no SIGAA tem doze tópicos: transformação digital, inteligência artificial, infraestrutura de TI e linguagens de programação, engenharia de prompt, introdução à análise de dados, atividade prática nota 1, visualização de dados, cibersegurança, MVP e produtos digitais com IA, gestão ágil com Scrum, prova substitutiva e prova final.

A pasta tem dezessete arquivos. Quatro são os módulos novos, com estrutura de ciclo (teoria, demonstração, prática, entrega), quatro ciclos por módulo, entre 40 e 65 minutos cada. Os outros são decks temáticos antigos, de 2022 a 2026, em formato expositivo.

Os quatro módulos somam dezesseis ciclos e cobrem: o que é um LLM, alucinação, engenharia de prompt, artifacts, agentes e skills, tipos de dados, análise exploratória, geração de planilha e slide, automação de documentos, leitura de documentos longos, benchmarking, análise qualitativa, legislação, análise contratual, skill personalizada, ética e LGPD, e um projeto integrador de fechamento.

## 2. A decisão estrutural

Os módulos deixam de ser um curso de quatro dias dentro da disciplina e passam a ser a unidade de todos os encontros. Cada encontro é um módulo de quatro ciclos. O encontro 1 já ocorreu como abertura, então a disciplina passa a ter quinze módulos, dos encontros 2 a 16.

Os quatro módulos existentes se redistribuem por seis módulos novos, porque o conteúdo deles foi comprimido para um formato de curso rápido e agora cabe com mais folga. Os decks antigos que sobrevivem viram módulos no mesmo formato. Três temas que não existem em nenhum material entram do zero: ambiente de trabalho digital, dados estruturados e consulta, produto digital.

As ferramentas de trabalho são o opencode desktop e o GitHub Desktop, ambos com interface gráfica. Não há linha de comando na disciplina. Quando um script precisa rodar, quem executa é o agente, e o aluno confere a saída. Isso preserva o objetivo de formar administrador que sabe pedir, verificar e decidir, sem transformar o semestre em curso de terminal.

Um problema herdado precisa de correção: o projeto integrador fecha o módulo 4 atual, com trinta minutos de execução. Como projeto de disciplina semestral ele é curto demais e cai cedo demais. Ele passa para o encontro 16 e ganha as entregas de bloco como etapas.

## 3. Os quinze módulos

| Enc. | Módulo | Origem | Ciclos |
|---|---|---|---|
| 1 | Abertura da disciplina | Realizado | Programa, avaliação, diagnóstico da turma |
| 2 | 1. Transformação digital e o trabalho do administrador | Refazer a partir de 1.Transformação digital.pptx | Quarta revolução industrial · Sociedade informacional e a empresa brasileira · Automação do trabalho: quais tarefas · Mapa de tarefas automatizáveis |
| 3 | 2. Ambiente de trabalho digital | Refazer Infraestrutura de TI + conteúdo novo | O que roda onde: local, servidor, nuvem, custo · Arquivos, pastas e formatos do projeto · Instalação e primeiro uso do opencode desktop · Versionamento com GitHub Desktop |
| 4 | 3. IA, LLM e engenharia de prompt | Módulo 1 atual, ciclos 1.1 e 1.2, expandidos | O que é IA e o que é um LLM · Alucinação e verificação · Os quatro elementos do prompt · Few-shot, chain-of-thought, chain-of-verification, self-consistency |
| 5 | 4. Do prompt ao artefato: arquivos, agentes e configuração | Módulo 1 atual, ciclos 1.3 e 1.4, portados | Gerar documentos na pasta do projeto · AGENTS.md no repositório · Skills e MCPs · Subagentes e tarefas encadeadas |
| 6 | 5. Dados na Administração | Módulo 2 ciclo 2.1 + corte de Governança de Dados | Tipos de dados e fontes · Onde os dados moram · Qualidade e governança · Mapa de dados da organização |
| 7 | 6. Análise exploratória de dados | Módulo 2 ciclo 2.2, expandido | O que a EDA responde · Do CSV ao relatório no opencode desktop · Ausentes, outliers e o que não confiar · Conferir o número que a IA produziu |
| 8 | 7. Dados estruturados e consulta | Novo | Da planilha à tabela · Modelo relacional em linguagem de gestor · SQL assistido · Juntar fontes: a base do projeto |
| 9 | 8. Visualização de dados e painéis | Refazer Visualização de Dados.pptx + ciclo 2.3 | Por que a maioria dos gráficos falha · Forma, escala e cor · Do dado ao painel HTML · Painel do projeto |
| 10 | 9. Automação de documentos e processos | Módulo 2 ciclo 2.4 + Taulli cap. 5 | O que é automatizável no trabalho recorrente · Prompt-templates com variáveis · RPA e automação de processos · Um fluxo repetível que o agente executa |
| 11 | 10. Pesquisa, documentos longos e análise qualitativa | Módulo 3 atual | Leitura em camadas · Benchmarking com fontes verificadas · Análise de conteúdo · Legislação e teste de alucinação |
| 12 | 11. Machine learning e analytics para a decisão | Refazer Potencial das Técnicas de Data Science.pptx | Descritiva, preditiva, prescritiva · Supervisionado, não supervisionado, por reforço · Deep learning e IA generativa · Um modelo simples sobre a base do projeto |
| 13 | 12. Governança de dados, LGPD e cibersegurança | Refazer Cibersegurança + Governança + ciclo 4.3 | LGPD para quem trabalha com dados · Papéis, políticas e metadados · Ataques e defesas com IA · Protocolo de uso seguro |
| 14 | 13. Decisão apoiada por IA: contratos, editais e devolutivas | Módulo 4 atual, ciclos 4.1 e 4.2 | Análise contratual em camadas · Editais e compra pública · Devolutiva ao gestor · Skill da área, versão final |
| 15 | 14. Produto digital e gestão ágil | Novo + XP-Extreme Programming.pptx + Scrum | O que é um MVP · Do problema à user story · Construir e publicar um protótipo · Scrum e XP |
| 16 | 15. Projeto integrador | Fecho do módulo 4, expandido | Consolidação do repositório e do caderno de prompts · Execução final · Apresentação · Balanço |

## 4. O que muda ao portar para o opencode desktop

Os quatro módulos existentes instruem o aluno a colar prompts no Claude.ai, anexar arquivo pelo ícone de clipe e visualizar o Artifact no painel lateral. A mudança de fundo não é de interface, é de unidade de trabalho: sai a conversa avulsa, entra a pasta do projeto. Tudo que o aluno faz passa a deixar rastro em arquivo.

| No deck atual | No opencode desktop |
|---|---|
| "Copie e cole no Claude.ai" | Sessão com a pasta do projeto aberta |
| Anexo pelo ícone de clipe | Arquivo já na pasta do projeto, citado pelo nome no prompt |
| Artifact no painel lateral | Arquivo gravado na pasta e aberto no navegador |
| Skill colada no início da conversa | AGENTS.md na raiz do projeto |
| Caderno de prompts em .txt | Pasta prompts, um arquivo por técnica |
| Entrega enviada por e-mail | Commit pelo GitHub Desktop |

O ganho pedagógico é a rastreabilidade. Com o repositório, a correção enxerga o que o aluno pediu, o que o modelo devolveu e o que o aluno corrigiu. É exatamente o que os decks já dizem que importa e que a interface de chat não registrava.

O módulo 2 passa a existir por causa disso. Sem uma sessão dedicada a organização de pastas, instalação do opencode desktop e primeiro uso do GitHub Desktop, o restante do semestre trava no encontro seguinte. O ciclo 2.4 é o mais arriscado: commit, push e resolução de conflito por interface gráfica levam tempo com turma grande, e é onde o roteiro precisa ser mais detalhado.

Quando um script Python precisa rodar, quem executa é o agente dentro da sessão. O aluno não digita comando. O que se cobra dele é a pergunta, a conferência do resultado contra a fonte e o registro do que precisou de correção.

## 5. Diagnóstico dos arquivos da pasta

| Arquivo | Situação | O que fazer |
|---|---|---|
| modulo1_UFMA_Administracao_v3 (1).pptx | Adaptar | Vira os módulos 3 e 4. Portar as quatro demonstrações para o opencode desktop. Ciclo 1.4 precisa trocar "skill colada na conversa" por AGENTS.md |
| modulo2_UFMA_Administracao.pptx | Adaptar | Vira os módulos 5, 6, 7 e 9. O ciclo 2.3 (Excel e PowerPoint por copiar e colar) perde sentido com a pasta aberta e vira geração direta de arquivo |
| modulo3_UFMA_Administracao.pptx | Adaptar | Vira o módulo 10 quase intacto. Remover a logística de encontro remoto e breakout rooms, que era de outro formato |
| modulo4_UFMA_Administracao.pptx | Dividir | Ciclos 4.1 e 4.2 viram o módulo 13. Ciclo 4.3 migra para o módulo 12. O projeto integrador vira o módulo 15 inteiro |
| 1.Transformação digital.pptx | Refazer | Conteúdo de Schwab permanece. Os seis slides que mandam consultar o Perplexity viram uma demonstração única no opencode desktop. Dados de automação do trabalho precisam de atualização |
| Infraestrutura de TI_ hardware e software.pptx | Refazer | Tipos de computador, sistemas operacionais e TCO ocupam metade do deck e rendem um ciclo. O resto do módulo 2 é conteúdo novo |
| Engenharia-de-Prompt.pptx | Absorver | As técnicas (few-shot, chain-of-thought, least-to-most, chain-of-verification, self-consistency) entram nos ciclos 3.3 e 3.4. Os exemplos de marketing e finanças ficam, refeitos sobre arquivos da pasta do projeto |
| Visualização de Dados.pptx | Refazer | Os fundamentos (Nussbaumer, escolha de gráfico, saturação, paleta) sustentam dois ciclos. A parte de Power BI e extração do YouTube sai. O bloco de ETL migra para o módulo 6 |
| Potencial das Técnicas de Data Science.pptx | Refazer | Base do módulo 11. Conteúdo de ML ainda válido. As questões do ENADE 2022 são material de avaliação e ficam. A EDA com dados da ANTAQ vira exemplo, não centro |
| O Que é Governança de Dados.pptx | Cortar | 108 slides para um ciclo. Sobrevivem qualidade de dados, papéis, metadados e LGPD. Apache Atlas e MDM saem, fora do escopo de Administração |
| Cibersegurança.pptx | Atualizar | Estrutura boa e o caso da ADM Solutions funciona. Falta o que mudou com IA: phishing gerado, deepfake em fraude, injeção de prompt |
| XP-Extreme Programming.pptx | Absorver | Dezoito slides, fragmento. Entra no ciclo 14.4 junto com Scrum |
| Técnicas de Data Science-Portos.pptx | Arquivar | Variante setorial do deck de Data Science. Fora do escopo desta turma. Serve como exemplo de aplicação em um ciclo |
| Temas em Segurança Pública e Direitos Humanos.pptx | Retirar | Não pertence à disciplina |
| Atividade Dinâmica Avaliativa.docx | Reaproveitar | A dinâmica de grupos por tema com pergunta cruzada funciona. Vira a entrega do módulo 1 |
| Cibersegurança.pdf | Descartar | Cópia em PDF do pptx |
| programa atual.pdf | Substituir | Base para o programa novo |

Onze arquivos de apresentação viram quinze módulos. Quatro estão prontos em estrutura e precisam de porte. Os outros onze são produção nova ou refação profunda, cerca de 330 slides no formato de ciclo.

## 6. Avaliação

Três notas, cada uma cobrindo cinco encontros. Cada nota tem duas entregas, todas etapas do mesmo projeto, versionadas no repositório individual do aluno.

Nota 1, módulos 1 a 5, encontros 2 a 6.

A1, no encontro 3, peso 40. Repositório individual no GitHub criado e funcionando, com a estrutura de pastas da disciplina e o primeiro commit feito pelo GitHub Desktop.

A2, no encontro 6, peso 60. Mapa de tarefas automatizáveis do próprio trabalho ou estágio, diário de alucinação, par de prompts documentado, AGENTS.md da área e mapa de dados da organização escolhida.

Nota 2, módulos 6 a 10, encontros 7 a 11.

B1, no encontro 9, peso 60. Base povoada, consultas que respondem perguntas de gestão e painel com três indicadores.

B2, no encontro 11, peso 40. Fluxo de automação documentado e síntese de pesquisa com fontes verificadas.

Nota 3, módulos 11 a 15, encontros 12 a 16.

C1, no encontro 14, peso 40. Protocolo de uso seguro de IA e análise de documento com tabela de riscos e devolutiva ao gestor.

C2, no encontro 16, peso 60. Projeto integrador, caderno de prompts consolidado e apresentação.

Média das três notas. Prova final conforme o regimento, sobre todo o conteúdo.

Critério comum às seis entregas: o problema é real e específico, o resultado foi conferido contra a fonte, o que a IA errou está registrado, o prompt está documentado e reproduzível, e o repositório abre.

A entrega A1 vale nota de propósito. Ela é barata de fazer e cara de deixar para depois: quem sair do encontro 3 sem repositório funcionando não acompanha o resto do semestre. Cobrar cedo transforma o problema de infraestrutura em problema do aluno enquanto ainda dá tempo de resolver.

## 6a. Modelos gratuitos: o que isso impõe ao planejamento

Os alunos usam os modelos gratuitos do opencode e do GitHub. O custo some, mas três restrições entram no lugar e precisam estar no roteiro de cada módulo.

Cota diária. As camadas gratuitas limitam requisições por dia e por minuto. Vinte e poucos alunos disparando pedidos ao mesmo tempo numa aula de quatro horas esgotam cota no meio do encontro. Mitigação: cada ciclo prático tem no máximo dois pedidos longos, os conjuntos de dados são pequenos (poucos milhares de linhas), e o roteiro traz o resultado esperado por escrito, para que quem ficar sem cota consiga continuar a análise e a discussão sem o modelo.

Qualidade menor. Os modelos gratuitos erram mais em geração de código e em cálculo. Nos módulos 3 e 12 isso ajuda, porque alucinação e verificação ficam visíveis com pouco esforço. Nos módulos 6 a 9 atrapalha, e a correção precisa avaliar a conferência do aluno, não o acerto do modelo.

Instabilidade. Provedor gratuito muda de modelo e de limite sem aviso. Os roteiros não devem nomear um modelo específico como obrigatório, e o professor precisa testar o roteiro na semana da aula, não no início do semestre.

## 7. Bibliografia

Laudon sai. A edição brasileira é de 2014 e o eixo da disciplina passou para tecnologias que o livro não cobre.

Básica:

TAULLI, Tom. Introdução à inteligência artificial: uma abordagem não técnica. São Paulo: Novatec, 2020.

SHARDA, Ramesh; DELEN, Dursun; TURBAN, Efraim. Business intelligence e análise de dados para gestão do negócio. 4. ed. Porto Alegre: Bookman, 2019.

SCHWAB, Klaus. A quarta revolução industrial. São Paulo: Edipro, 2016.

Complementar:

DELEN, Dursun; SHARDA, Ramesh; TURBAN, Efraim. Analytics, data science, and artificial intelligence: systems for decision support. 11. ed. Harlow: Pearson, 2020.

SUTHERLAND, Jeff. Scrum: a arte de fazer o dobro do trabalho na metade do tempo. Rio de Janeiro: Leya, 2014.

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais.

Documentação técnica de apoio, para os módulos 2 a 9: documentação do opencode, guias de prompting da Anthropic e da OpenAI, guia do GitHub Desktop.

Correspondência com os módulos: Taulli caps. 1, 3 e 4 nos módulos 3 e 11, cap. 2 no módulo 5, cap. 5 no módulo 9, cap. 8 nos módulos 13 e 14. Sharda, Delen e Turban cap. 1 no módulo 11, cap. 3 nos módulos 6 e 8, caps. 4 a 6 no módulo 11, cap. 9 no módulo 5. Schwab no módulo 1.

## 8. Ordem de produção

O calendário manda. Os módulos 1 e 2 precisam existir antes de tudo, e o módulo 2 é produção do zero.

Primeiro, o programa da disciplina em docx padrão UFMA, com o cronograma dos quinze módulos. Trava o resto e vai ao SIGAA.

Segundo, módulos 1 e 2, para os encontros 2 e 3. O módulo 2 inclui o roteiro de instalação do opencode desktop e do GitHub Desktop, que precisa ser testado numa máquina do laboratório antes, com as restrições de instalação que o CCET aplica.

Terceiro, porte dos módulos 3, 4, 5, 6, 7 e 9 a partir dos módulos 1 e 2 atuais, na ordem do calendário.

Quarto, módulos 8, 10 e 11.

Quinto, módulos 12, 13, 14 e 15.

Além dos decks, cada módulo precisa de um roteiro em markdown no repositório da disciplina, com o enunciado dos quatro ciclos, os arquivos de entrada e o resultado esperado de cada entrega. Os decks atuais já trazem esse conteúdo nos slides de prática e entrega, então o roteiro sai do próprio deck.

## 9. Decisões fechadas

O laboratório permite instalar programas. O opencode desktop e o GitHub Desktop entram nas máquinas do CCET.

Os alunos usam modelos gratuitos no opencode e no GitHub. Sem custo para a turma e sem chave institucional. As consequências estão na seção 6a.

Contas individuais por aluno, tanto no GitHub quanto no provedor de modelo. Cada aluno tem seu repositório, e a nota não depende de quem clicou em commit. O cadastro entra no ciclo 2.4, com a entrega A1 como comprovação.

Três notas ao longo do semestre, compostas como na seção 6.

## 10. Pendências

O tamanho da turma. Define se o projeto integrador é individual ou em equipe de três a quatro, e se a apresentação do encontro 16 cabe em quatro horas.

Se as máquinas do laboratório são restauradas a cada uso. Em caso positivo, o roteiro do módulo 2 precisa prever reinstalação rápida ou imagem preparada, e o aluno precisa saber clonar o próprio repositório no início de cada aula.

Se a prova final continua obrigatória e se pode ser substituída por defesa do projeto.

Um teste de sanidade antes do encontro 3: instalar os dois aplicativos numa máquina do laboratório, criar conta, autenticar o modelo gratuito, fazer um commit e medir quanto tempo isso leva. É o número que define se o ciclo 2.4 cabe em quarenta e cinco minutos ou precisa de mais.
