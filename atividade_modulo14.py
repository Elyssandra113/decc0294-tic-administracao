"""
Atividade do modulo 14 - Produto digital e gestao agil
DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
UFMA - Curso de Administracao

O QUE ESTE SCRIPT FAZ

Ele cria a ficha do produto, o backlog e o registro do teste com usuario,
ordena as historias por valor sobre esforco, diz o que cabe na versao 1 e
confere se a entrega do encontro esta completa.

Nao usa biblioteca externa, nao acessa a rede e nao usa modelo de linguagem.

COMO USAR (peca ao agente do opencode que execute cada comando)

  python atividade_modulo14.py produto
      Cria entregas/ficha-produto.md com as quatro perguntas do ciclo 14.1.

  python atividade_modulo14.py backlog
      Cria entregas/backlog.csv com as colunas exigidas.

  python atividade_modulo14.py priorizar
      Confere o formato das historias e dos criterios de aceite, ordena por
      valor sobre esforco e diz o que cabe na versao 1.
      Grava saidas/backlog-priorizado.md.

  python atividade_modulo14.py teste
      Cria entregas/registro-teste.md para o teste com usuario do ciclo 14.4.

  python atividade_modulo14.py conferir
      Confere as tres entregas do encontro.

ORDEM: produto -> backlog -> priorizar -> construir -> teste -> conferir.

A REGRA DO CRITERIO DE ACEITE

Ele precisa poder ser verificado por outra pessoa, sem voce por perto.
"Funcionar bem" nao e criterio. "O arquivo gerado abre com as cinco colunas
na ordem definida" e.
"""

import csv
import os
import sys

PASTA_SAIDAS = "saidas"
PASTA_ENTREGAS = "entregas"
FICHA = os.path.join(PASTA_ENTREGAS, "ficha-produto.md")
BACKLOG = os.path.join(PASTA_ENTREGAS, "backlog.csv")
TESTE = os.path.join(PASTA_ENTREGAS, "registro-teste.md")
PRIORIZADO = os.path.join(PASTA_SAIDAS, "backlog-priorizado.md")

MIN_HISTORIAS = 5
MAX_HISTORIAS = 10
ESFORCO_DA_VERSAO_1 = 8

USUARIOS_VAGOS = ["os gestores", "gestores", "a equipe", "equipe", "o setor", "setor",
                  "os servidores", "servidores", "todos", "a organizacao", "a empresa",
                  "os funcionarios", "funcionarios", "os usuarios", "usuarios", "o publico"]

CRITERIOS_VAGOS = ["funcionar bem", "funcionar", "ficar bom", "ficar bonito", "estar rapido",
                   "ser facil", "ser intuitivo", "ficar pronto", "estar ok", "rodar",
                   "ficar legal", "atender o usuario", "ser util"]

CABECALHO_BACKLOG = ["id", "historia", "criterio_de_aceite", "valor", "esforco", "na_versao_1"]

EXEMPLO_BACKLOG = [
    ["EXEMPLO - apague esta linha",
     "Como assistente da divisao de pessoal, quero gerar a escala do mes a partir da planilha de plantoes, para nao redigitar 40 linhas por mes",
     "O arquivo escala.csv e gerado com uma linha por servidor e as colunas nome, data e turno, na ordem definida",
     "5", "3", "sim"],
]

TEXTO_FICHA = """# Ficha do produto

## 1. O usuario
usuario_cargo: (o cargo de quem vai usar. Nao vale "os gestores" nem "a equipe")
quem_mais_ocuparia_esse_lugar: (quem faria isso na sua ausencia)

## 2. O caminho atual
passos_hoje: (o que a pessoa faz hoje, em passos, separados por ponto e virgula)
tempo_por_execucao_minutos: (quanto tempo leva hoje, em minutos)
frequencia: (quantas vezes por semana ou por mes)

## 3. O que muda
o_que_a_pessoa_deixa_de_fazer: (o que sai do trabalho dela com o produto)
sinal_de_que_funcionou: (o que voce vai observar para saber que ajudou. Com numero, se possivel)

## 4. O escopo da versao 1
o_que_entra: (o que a versao 1 resolve, do comeco ao fim de um caso)
o_que_fica_de_fora: (o que foi cortado para caber. Nada se perde: vai para o backlog)
"""

TEXTO_TESTE = """# Registro do teste com usuario

## A tarefa
quem_testou: (cargo ou "colega da turma")
tarefa_dada: (a tarefa concreta, escrita, que a pessoa recebeu)
tempo_ate_concluir_minutos: (ou NAO CONCLUIU)

## O que aconteceu
Escreva uma linha por achado, no formato: descricao | bloqueio ou incomodo

achado_1: (onde a pessoa travou e o que ela tentou) | (bloqueio ou incomodo)
achado_2: | ()
achado_3: | ()

## O que a pessoa esperava
expectativa_frustrada: (o que ela achou que ia acontecer e nao aconteceu)

## A proxima versao
historias_criadas: (os ids das historias novas que voce colocou no backlog)
o_que_entra_na_versao_2: (o que vem primeiro, e por que)

## Retrospectiva
o_que_atrapalhou_a_construcao: (o que voce faria diferente na proxima)
"""


def normalizar(t):
    t = (t or "").strip().lower()
    for de, para in (("á", "a"), ("à", "a"), ("ã", "a"), ("â", "a"), ("é", "e"),
                     ("ê", "e"), ("í", "i"), ("ó", "o"), ("õ", "o"), ("ô", "o"),
                     ("ú", "u"), ("ç", "c")):
        t = t.replace(de, para)
    return t


def vazio(valor):
    if not valor:
        return True
    t = str(valor)
    while "(" in t and ")" in t:
        i, j = t.index("("), t.index(")")
        if j < i:
            break
        t = t[:i] + t[j + 1:]
    return t.replace("|", " ").strip() == ""


def num(valor):
    t = str(valor or "").strip().replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def ler_campos(caminho):
    campos = {}
    if not os.path.exists(caminho):
        return campos
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            bruta = linha.strip()
            if not bruta or bruta.startswith("#") or bruta.startswith("|"):
                continue
            if ":" in bruta:
                chave, valor = bruta.split(":", 1)
                chave = chave.strip().lower().replace(" ", "_")
                if chave and " " not in chave:
                    campos[chave] = valor.strip()
    return campos


# ---------------------------------------------------------------- comandos

def cmd_produto():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if os.path.exists(FICHA):
        print("A ficha ja existe em", FICHA)
        return
    with open(FICHA, "w", encoding="utf-8") as f:
        f.write(TEXTO_FICHA)
    print("Ficha criada em", FICHA)
    print()
    print("O usuario precisa ser um cargo. O script recusa 'os gestores', 'a equipe'")
    print("e qualquer grupo, porque produto sem usuario definido nao tem como ser testado.")


def cmd_backlog():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if os.path.exists(BACKLOG):
        print("O backlog ja existe em", BACKLOG)
        return
    with open(BACKLOG, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(CABECALHO_BACKLOG)
        for linha in EXEMPLO_BACKLOG:
            w.writerow(linha)
    print("Backlog criado em", BACKLOG)
    print()
    print("Formato da historia: Como [cargo], quero [acao], para [resultado].")
    print("valor e esforco: numeros de 1 a 8. A versao 1 comporta esforco somado de %d." % ESFORCO_DA_VERSAO_1)
    print("Escreva de %d a %d historias." % (MIN_HISTORIAS, MAX_HISTORIAS))


def cmd_teste():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if os.path.exists(TESTE):
        print("O registro ja existe em", TESTE)
        return
    with open(TESTE, "w", encoding="utf-8") as f:
        f.write(TEXTO_TESTE)
    print("Registro criado em", TESTE)
    print()
    print("Fique calado enquanto a pessoa tenta. Cada ajuda sua apaga um problema")
    print("que o produto tem, e que vai aparecer de novo com o proximo usuario.")


def ler_backlog(problemas):
    if not os.path.exists(BACKLOG):
        print("O backlog nao existe. Rode: python atividade_modulo14.py backlog")
        sys.exit(1)
    with open(BACKLOG, "r", encoding="utf-8-sig", newline="") as f:
        linhas = [dict(l) for l in csv.DictReader(f, delimiter=";")]
    linhas = [l for l in linhas if not normalizar(l.get("id")).startswith("exemplo")]

    validas = []
    for i, l in enumerate(linhas, 2):
        ident = (l.get("id") or ("linha %d" % i)).strip()
        historia = normalizar(l.get("historia"))
        if vazio(l.get("historia")):
            problemas.append("%s: historia vazia." % ident)
        else:
            if "como " not in historia:
                problemas.append("%s: a historia nao comeca por 'Como [cargo]'." % ident)
            if "quero " not in historia:
                problemas.append("%s: a historia nao tem a parte 'quero [acao]'." % ident)
            if "para " not in historia:
                problemas.append("%s: a historia nao tem a parte 'para [resultado]'. "
                                 "E a parte que justifica construir." % ident)

        criterio = (l.get("criterio_de_aceite") or "").strip()
        cn = normalizar(criterio)
        if vazio(criterio):
            problemas.append("%s: criterio de aceite vazio." % ident)
        elif any(cn == v or cn.startswith(v) for v in CRITERIOS_VAGOS):
            problemas.append("%s: o criterio '%s' nao permite dizer que ficou pronto. "
                             "Escreva o que outra pessoa verificaria sem voce por perto."
                             % (ident, criterio))
        elif len(criterio.split()) < 6:
            problemas.append("%s: o criterio de aceite tem %d palavras. Escreva a condicao "
                             "observavel inteira." % (ident, len(criterio.split())))

        valor = num(l.get("valor"))
        esforco = num(l.get("esforco"))
        if valor is None or not (1 <= valor <= 8):
            problemas.append("%s: valor precisa ser um numero de 1 a 8." % ident)
        if esforco is None or not (1 <= esforco <= 8):
            problemas.append("%s: esforco precisa ser um numero de 1 a 8." % ident)
        if valor is not None and esforco is not None and 1 <= valor <= 8 and 1 <= esforco <= 8:
            validas.append((ident, l, valor, esforco))

    if len(linhas) < MIN_HISTORIAS:
        problemas.append("ha %d historias. O minimo e %d." % (len(linhas), MIN_HISTORIAS))
    if len(linhas) > MAX_HISTORIAS:
        problemas.append("ha %d historias. O maximo e %d: backlog longo demais nesta altura "
                         "detalha o que ainda vai mudar." % (len(linhas), MAX_HISTORIAS))
    return linhas, validas


def cmd_priorizar():
    problemas = []
    linhas, validas = ler_backlog(problemas)

    if problemas:
        print("=" * 62)
        print("O BACKLOG AINDA NAO PODE SER PRIORIZADO")
        print("=" * 62)
        for i, p in enumerate(problemas, 1):
            print(" %d. %s" % (i, p))
        sys.exit(1)

    ordenado = sorted(validas, key=lambda x: (-(x[2] / x[3]), x[3]))

    acumulado = 0.0
    cabem = []
    for ident, l, valor, esforco in ordenado:
        if acumulado + esforco <= ESFORCO_DA_VERSAO_1:
            acumulado += esforco
            cabem.append(ident)

    marcadas = [l.get("id", "").strip() for _, l, _, _ in validas
                if normalizar(l.get("na_versao_1")).startswith("s")]

    print("=" * 62)
    print("BACKLOG PRIORIZADO")
    print("=" * 62)
    print("historias:", len(validas))
    print()
    print("  %-22s %6s %8s %8s" % ("id", "valor", "esforco", "razao"))
    for ident, l, valor, esforco in ordenado:
        print("  %-22s %6s %8s %8s" % (ident[:22], int(valor), int(esforco),
                                       ("%.2f" % (valor / esforco)).replace(".", ",")))
    print()
    print("Cabe na versao 1 (esforco somado ate %d): %s" % (ESFORCO_DA_VERSAO_1, ", ".join(cabem) or "nenhuma"))
    print("Esforco acumulado:", int(acumulado))
    print()

    if marcadas:
        fora = [m for m in marcadas if m not in cabem]
        if fora:
            print("Voce marcou como versao 1: %s" % ", ".join(marcadas))
            print("Destas, %s ficam fora do que cabe pela ordem de valor sobre esforco."
                  % ", ".join(fora))
            print("Isso pode estar certo, se houver dependencia entre historias. Se for o caso,")
            print("escreva a dependencia no backlog. Se nao for, refaca o corte.")
        else:
            print("A sua marcacao de versao 1 coincide com a ordem calculada.")
    else:
        print("Nenhuma historia marcada na coluna na_versao_1. Marque as que voce vai construir.")

    print()
    print("A ordem por valor sobre esforco e sugestao, e nao decisao. Dependencia entre")
    print("historias e obrigacao legal mudam a ordem, e isso se escreve.")

    os.makedirs(PASTA_SAIDAS, exist_ok=True)
    with open(PRIORIZADO, "w", encoding="utf-8") as f:
        f.write("# Backlog priorizado\n\n")
        f.write("| id | historia | criterio de aceite | valor | esforco | razao |\n")
        f.write("|---|---|---|---|---|---|\n")
        for ident, l, valor, esforco in ordenado:
            f.write("| %s | %s | %s | %d | %d | %s |\n" % (
                ident, (l.get("historia") or "").replace("|", "/"),
                (l.get("criterio_de_aceite") or "").replace("|", "/"),
                int(valor), int(esforco), ("%.2f" % (valor / esforco)).replace(".", ",")))
        f.write("\ncabe_na_versao_1: %s\n" % ", ".join(cabem))
        f.write("esforco_acumulado: %d\n" % int(acumulado))
        f.write("limite_de_esforco: %d\n" % ESFORCO_DA_VERSAO_1)
    print()
    print("Resultado gravado em", PRIORIZADO)


# ------------------------------------------------------------- conferencia

def conferir_ficha(problemas):
    if not os.path.exists(FICHA):
        problemas.append("ficha-produto.md nao existe. Rode: python atividade_modulo14.py produto")
        return
    campos = ler_campos(FICHA)
    obrigatorios = [
        ("usuario_cargo", "o cargo do usuario"),
        ("quem_mais_ocuparia_esse_lugar", "quem mais ocuparia esse lugar"),
        ("passos_hoje", "os passos do caminho atual"),
        ("tempo_por_execucao_minutos", "o tempo por execucao"),
        ("frequencia", "a frequencia"),
        ("o_que_a_pessoa_deixa_de_fazer", "o que a pessoa deixa de fazer"),
        ("sinal_de_que_funcionou", "o sinal de que funcionou"),
        ("o_que_entra", "o escopo da versao 1"),
        ("o_que_fica_de_fora", "o que ficou de fora"),
    ]
    for chave, nome in obrigatorios:
        if vazio(campos.get(chave)):
            problemas.append("ficha-produto.md: falta %s (campo %s)." % (nome, chave))

    usuario = normalizar(campos.get("usuario_cargo"))
    if usuario and usuario in USUARIOS_VAGOS:
        problemas.append("ficha-produto.md: '%s' e um grupo, nao um cargo. Escolha uma pessoa "
                         "concreta pelo cargo, porque e ela que vai testar o produto."
                         % campos.get("usuario_cargo"))

    tempo = num(campos.get("tempo_por_execucao_minutos"))
    if not vazio(campos.get("tempo_por_execucao_minutos")) and tempo is None:
        problemas.append("ficha-produto.md: o tempo por execucao precisa ser um numero de "
                         "minutos. Sem ele nao ha como dizer depois se o produto ajudou.")

    passos = campos.get("passos_hoje") or ""
    if not vazio(passos) and passos.count(";") < 2:
        problemas.append("ficha-produto.md: o caminho atual tem menos de tres passos. "
                         "Descreva o que a pessoa faz hoje com grao fino, separando por ponto e virgula.")


def conferir_teste(problemas):
    if not os.path.exists(TESTE):
        problemas.append("registro-teste.md nao existe. Rode: python atividade_modulo14.py teste")
        return
    campos = ler_campos(TESTE)
    obrigatorios = [
        ("quem_testou", "quem testou"),
        ("tarefa_dada", "a tarefa dada"),
        ("tempo_ate_concluir_minutos", "o tempo ate concluir, ou NAO CONCLUIU"),
        ("expectativa_frustrada", "o que a pessoa esperava e nao aconteceu"),
        ("historias_criadas", "as historias criadas a partir do teste"),
        ("o_que_entra_na_versao_2", "o que entra na versao 2"),
        ("o_que_atrapalhou_a_construcao", "a retrospectiva"),
    ]
    for chave, nome in obrigatorios:
        if vazio(campos.get(chave)):
            problemas.append("registro-teste.md: falta %s (campo %s)." % (nome, chave))

    achados = [(k, v) for k, v in campos.items() if k.startswith("achado_") and not vazio(v)]
    if not achados:
        problemas.append("registro-teste.md: nenhum achado registrado. Teste em que nada travou "
                         "quase sempre teve tarefa facil demais ou ajuda sua. Refaca com uma "
                         "tarefa mais dificil, ou escreva por que nada apareceu.")
    for chave, valor in achados:
        if "|" not in valor:
            problemas.append("registro-teste.md, %s: falta a classificacao depois da barra "
                             "(bloqueio ou incomodo)." % chave)
            continue
        _, _, classe = valor.partition("|")
        classe = normalizar(classe)
        if "bloqueio" not in classe and "incomodo" not in classe:
            problemas.append("registro-teste.md, %s: a classificacao precisa ser bloqueio ou "
                             "incomodo. Bloqueio vem antes na fila." % chave)


def cmd_conferir():
    problemas = []
    print("=" * 62)
    print("CONFERENCIA DO MODULO 14")
    print("=" * 62)
    conferir_ficha(problemas)
    if not os.path.exists(PRIORIZADO):
        problemas.append("backlog-priorizado.md nao existe. Rode: python atividade_modulo14.py priorizar")
    else:
        ler_backlog(problemas)
    conferir_teste(problemas)

    if problemas:
        print("A entrega ainda nao esta completa. Faltam", len(problemas), "itens:\n")
        for i, p in enumerate(problemas, 1):
            print(" %d. %s" % (i, p))
        print()
        print("Corrija e rode a conferencia de novo.")
        sys.exit(1)

    print("Entrega completa.")
    print()
    print("  ficha-produto.md          usuario pelo cargo, caminho atual medido, escopo cortado")
    print("  backlog.csv               historias no formato, com criterio de aceite verificavel")
    print("  backlog-priorizado.md     ordem por valor sobre esforco e o que cabe na versao 1")
    print("  registro-teste.md         achados classificados e proxima versao definida")
    print()
    print("Faca o commit pelo GitHub Desktop. No encontro 16 voce apresenta o produto,")
    print("inclusive o que ainda nao funciona.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    comando = sys.argv[1].lower()
    if comando == "produto":
        cmd_produto()
    elif comando == "backlog":
        cmd_backlog()
    elif comando == "priorizar":
        cmd_priorizar()
    elif comando == "teste":
        cmd_teste()
    elif comando == "conferir":
        cmd_conferir()
    else:
        print("Comando desconhecido:", comando)
        print("Use: produto, backlog, priorizar, teste, conferir")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        print("\nInterrompido.")
