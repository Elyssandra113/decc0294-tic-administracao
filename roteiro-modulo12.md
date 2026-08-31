# Roteiro do módulo 12

Governança de dados, LGPD e cibersegurança. Encontro 13, cerca de 4 horas.
DECC0294, UFMA, Curso de Administração, 2026.2.

Encontro do bloco da nota 3, sem entrega avaliada isolada. As três entregas daqui entram na C1 do encontro 14.

## Antes da aula

Material do professor: `modulo12-governanca-lgpd-ciberseguranca.html`, este roteiro e `atividade_modulo12.py`.

Publicado na turma virtual, com uma semana de antecedência: o script, o texto vigente da Lei 13.709 (artigos 5, 6, 7 e 48) e o pedido de que cada aluno levante quais dados pessoais passam pelas mãos dele no trabalho ou no estágio. Deixe explícito, por escrito, que ninguém deve trazer arquivo com dado pessoal de terceiro. A lista é de tipos e caminhos.

Rode `python atividade_modulo12.py varrer .` numa pasta de teste antes da aula. Monte a pasta com um arquivo que tenha CPF gerado por gerador de teste, e-mail e telefone, para a demonstração do ciclo 12.1. Não use dado real de ninguém, nem seu.

Confira que o script recusa o CPF com dígito inválido. Isso é o que evita a varredura acusar toda sequência de onze números, e vale mostrar na projeção.

Prepare um caso de incidente noticiado, de preferência do Maranhão ou do setor público federal, para abrir o ciclo 12.4. Vazamento de folha, sequestro de dados em prefeitura e envio de lista a destinatário errado são os três formatos mais comuns.

## Distribuição do tempo

| Bloco | Duração | Slides |
|---|---|---|
| Abertura e visão geral | 10 min | 1 a 2 |
| Ciclo 12.1 | 45 min | 3 a 8 |
| Ciclo 12.2 | 50 min | 9 a 13 |
| Intervalo | 15 min | |
| Ciclo 12.3 | 45 min | 14 a 19 |
| Intervalo | 10 min | |
| Ciclo 12.4 | 60 min | 20 a 24 |
| Fechamento | 15 min | 25 a 27 |

## Ciclo 12.1 — Que dado pessoal passa por você

Teoria, 15 min. Os quatro termos do artigo 5: dado pessoal, dado sensível, titular, controlador e operador. Depois, o dado que ninguém sabe que tem.

Demonstração, 10 min. A varredura na projeção, sobre a pasta de teste.

Prática, 15 min. Cada aluno roda a varredura na própria pasta do projeto e começa o inventário.

Entrega, 5 min. `entregas/inventario-dados.csv` e `saidas/varredura-dados-pessoais.md`.

O ponto do ciclo é que dado pessoal não é só CPF. Peça à turma exemplos de combinação que identifica sem nome: cargo mais unidade mais ano de admissão costuma bastar em setor pequeno, e alguém sempre reconhece a situação.

A varredura encontrar zero é comum e precisa ser dito como resultado válido, junto com o limite: o script não lê PDF, imagem nem planilha binária, e não reconhece nome de pessoa. Quem interpretar zero como "está limpo" entendeu errado.

Vigie o inventário enquanto a turma escreve. Todo semestre alguém copia um CPF real "para ilustrar". O script recusa, mas é melhor interromper antes.

## Ciclo 12.2 — Base legal, finalidade e retenção

Teoria, 20 min. As dez bases do artigo 7, com foco nas quatro que cobrem quase tudo no serviço público. Depois os princípios do artigo 6: finalidade, necessidade, prazo, transparência.

Prática, 25 min. Cada aluno completa o inventário com base legal, finalidade e prazo em cada linha.

Entrega, 5 min. `entregas/inventario-dados.csv`.

O erro previsível é marcar consentimento em tudo. Consentimento pressupõe que o titular pode dizer não sem prejuízo, e isso quase nunca é verdade entre servidor e chefia, ou entre cidadão e serviço do qual ele depende. Faça essa correção com um caso da própria turma.

A finalidade escrita como substantivo é o segundo erro. "Cadastro" não é finalidade; "conceder o auxílio transporte" é. O script recusa finalidade com menos de três palavras exatamente por isso.

A coluna de eliminação por desnecessidade é a que gera a discussão mais útil. Peça que cada aluno diga em voz alta um campo que a organização coleta e não usa. Sempre aparece um.

## Ciclo 12.3 — IA e dado pessoal: o que não vai no prompt

Teoria, 20 min. O que acontece com o texto colado no prompt e por que isso é compartilhamento de dado. Anonimização e pseudonimização, e onde cada uma falha.

Prática, 20 min. Cada aluno escreve a seção de uso seguro no AGENTS.md, cria a pasta restrita, põe no .gitignore e monta um exemplo de tarefa com identificadores trocados.

Entrega, 5 min. `AGENTS.md`, `.gitignore` e `entregas/modulo12-ciclo3-exemplo.md`.

A conferência de que a pasta restrita não subiu é feita olhando a lista de arquivos do commit no GitHub Desktop, não confiando na configuração. Faça essa verificação na projeção uma vez, devagar.

O caso da tabela de correspondência guardada ao lado da base pseudonimizada merece dez segundos de silêncio depois de dito. É o erro mais comum e o que anula todo o resto.

Retome aqui a regra que a turma escreveu no encontro 4, no AGENTS.md. Este ciclo acrescenta uma seção, não recomeça o arquivo.

## Ciclo 12.4 — Cibersegurança e resposta a incidente

Teoria, 25 min. As quatro medidas básicas: senha única por serviço em gerenciador, segundo fator, desconfiança de mensagem com urgência, cópia de segurança em três lugares. Depois, primeira hora, primeiro dia e comunicação, com o artigo 48.

Prática, 30 min. Cada aluno escreve o plano de resposta e roda a conferência final.

Entrega, 5 min. `entregas/plano-resposta-incidente.md`.

"Não apague nada antes de registrar" é a instrução que salva o caso. O primeiro impulso de quem envia a planilha errada é apagar a mensagem, e com ela vai o registro de para quem foi e o que continha.

A recusa do script a "a equipe" como responsável é conteúdo. Pergunte quem, nominalmente pelo cargo, faria a primeira ligação às duas da manhã de um sábado. Se ninguém souber responder, esse é o achado do plano.

Muitos alunos vão descobrir que a organização não tem encarregado designado. Registre isso no plano em vez de inventar um cargo.

## O que sai deste encontro

Um relatório de varredura com decisão escrita. Um inventário com base legal, finalidade e prazo por linha. Uma seção de uso seguro no AGENTS.md, com pasta restrita fora do controle de versão. Um plano de resposta a incidente em uma página, com cargos responsáveis.

## Avisos no fechamento

O encontro 14 fecha a C1, que vale 40% da nota 3. Cada aluno precisa trazer um documento de decisão do próprio setor, com dez páginas ou mais e sem dado pessoal: edital, termo de referência, contrato, parecer ou devolutiva. Se o documento tiver dado pessoal, leva a versão publicada ou substitui os identificadores, aplicando o que foi feito hoje.

Peça também o critério de decisão escrito antes da aula, em três linhas. Ele vai ser comparado com o que o modelo propõe, e quem escrever durante a aula perde a comparação.
