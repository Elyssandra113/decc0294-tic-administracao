#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 6 - Analise exploratoria de dados
 DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
 UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que perfila a sua base, aponta os valores atipicos e
    organiza a conferencia dos numeros. Ele nao usa o modelo: e calculo
    determinístico, e por isso o mesmo arquivo devolve sempre o mesmo perfil.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute atividade_modulo6.py com o comando perfil dados/SEU-ARQUIVO.csv"
       Le o arquivo, detecta separador e codificacao, classifica cada coluna,
       mede vazios e distintos, calcula minimo, maximo, media e mediana, e
       grava saidas/perfil-SEU-ARQUIVO.md

    2) "execute atividade_modulo6.py com o comando atipicos dados/SEU-ARQUIVO.csv"
       Lista os valores fora do intervalo usual de cada coluna numerica, com a
       linha em que estao, e cria o formulario de decisao em
       entregas/modulo6-tratamento.csv

    3) "execute atividade_modulo6.py com o comando log"
       Cria o formulario de verificacao em entregas/modulo6-log-verificacao.csv

    4) "execute atividade_modulo6.py com o comando conferir"
       Valida o formulario de tratamento e o log, e gera
       entregas/modulo6-relatorio.md

    Sem nenhum comando, o script imprime estas instrucoes.

O QUE O SCRIPT NAO FAZ
    Ele nao remove atipico nem preenche ausente. Aponta e pede a sua decisao,
    com a razao escrita. Remover em silencio nao e limpeza, e perda de dado.

Nao precisa instalar nada. Roda com o Python que ja vem com o ambiente.
=============================================================================
"""

import csv
import os
import re
import sys
from datetime import date, datetime

SEP = ";"
TRATAMENTO = os.path.join("entregas", "modulo6-tratamento.csv")
LOG = os.path.join("entregas", "modulo6-log-verificacao.csv")
RELATORIO = os.path.join("entregas", "modulo6-relatorio.md")

COLS_TRATAMENTO = ["coluna", "caso", "valor", "linha", "classificacao", "decisao", "razao"]
CLASSIFICACOES = {
    "ausente ao acaso", "ausente por regra", "ausente com vies",
    "erro de registro", "unidade trocada", "realidade",
}
DECISOES = {"manter", "corrigir", "separar", "excluir", "nao preencher"}

COLS_LOG = ["numero", "o_que_mede", "valor", "total_fecha", "contagem_fecha",
            "ordem_de_grandeza", "linha_recalculada", "conclusao"]
SIM_NAO = {"sim", "nao", "nao se aplica"}


def titulo(t):
    print()
    print("=" * 74)
    print(" " + t)
    print("=" * 74)


# ---------------------------------------------------------------- leitura

def abrir(caminho):
    """Le o CSV tentando codificacoes e separadores comuns no Brasil."""
    if not os.path.exists(caminho):
        print()
        print("Nao encontrei o arquivo: " + caminho)
        print("Confira o caminho. Ele costuma comecar com dados/")
        return None, None, None

    bruto = None
    codificacao = None
    for cod in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(caminho, encoding=cod) as f:
                bruto = f.read()
            codificacao = cod
            break
        except (UnicodeDecodeError, LookupError):
            continue
    if bruto is None:
        print("Nao consegui ler o arquivo em nenhuma codificacao conhecida.")
        return None, None, None

    primeira = bruto.splitlines()[0] if bruto.splitlines() else ""
    contagens = {d: primeira.count(d) for d in (";", ",", "\t", "|")}
    separador = max(contagens, key=contagens.get)
    if contagens[separador] == 0:
        print("A primeira linha nao tem separador reconhecivel (; , tab |).")
        print("Abra o arquivo num editor de texto e confira o cabecalho.")
        return None, None, None

    linhas = list(csv.DictReader(bruto.splitlines(), delimiter=separador))
    return linhas, separador, codificacao


def numero(v):
    """Converte texto em numero, tolerando o formato brasileiro."""
    if v is None:
        return None
    t = str(v).strip().replace("R$", "").replace("%", "").strip()
    if not t:
        return None
    if re.match(r"^-?\d{1,3}(\.\d{3})+,\d+$", t):      # 1.234.567,89
        t = t.replace(".", "").replace(",", ".")
    elif re.match(r"^-?\d+,\d+$", t):                   # 1234,89
        t = t.replace(",", ".")
    elif re.match(r"^-?\d{1,3}(,\d{3})+\.\d+$", t):     # 1,234,567.89
        t = t.replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None


def eh_data(v):
    t = str(v).strip()
    return bool(re.match(r"^\d{2}[/-]\d{2}[/-]\d{4}", t) or
                re.match(r"^\d{4}-\d{2}-\d{2}", t))


def mediana(vals):
    s = sorted(vals)
    m = len(s)
    if m == 0:
        return None
    return s[m // 2] if m % 2 else (s[m // 2 - 1] + s[m // 2]) / 2


def quartis(vals):
    s = sorted(vals)
    m = len(s)
    if m < 4:
        return None, None
    return s[m // 4], s[(3 * m) // 4]


def fmt(v):
    if v is None:
        return "-"
    if abs(v - round(v)) < 1e-9 and abs(v) < 1e15:
        return "{:,}".format(int(round(v))).replace(",", ".")
    return "{:,.2f}".format(v).replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def analisar(linhas):
    """Devolve, por coluna, o tipo detectado e as estatisticas."""
    if not linhas:
        return []
    colunas = list(linhas[0].keys())
    total = len(linhas)
    perfil = []

    for c in colunas:
        valores = [(l.get(c) or "").strip() for l in linhas]
        preenchidos = [v for v in valores if v != ""]
        vazios = total - len(preenchidos)
        distintos = len(set(preenchidos))

        nums = [numero(v) for v in preenchidos]
        nums = [x for x in nums if x is not None]
        datas = sum(1 for v in preenchidos if eh_data(v))

        if preenchidos and len(nums) >= 0.9 * len(preenchidos):
            tipo = "numero"
        elif preenchidos and datas >= 0.9 * len(preenchidos):
            tipo = "data"
        elif preenchidos and distintos <= max(20, total * 0.05):
            tipo = "categoria"
        else:
            tipo = "texto"

        info = {
            "coluna": c, "tipo": tipo, "total": total, "vazios": vazios,
            "pct_vazios": 100.0 * vazios / total if total else 0,
            "distintos": distintos, "exemplos": [], "nums": nums,
        }

        if tipo == "numero" and nums:
            info["min"] = min(nums)
            info["max"] = max(nums)
            info["media"] = sum(nums) / len(nums)
            info["mediana"] = mediana(nums)
            info["soma"] = sum(nums)
        else:
            contagem = {}
            for v in preenchidos:
                contagem[v] = contagem.get(v, 0) + 1
            info["exemplos"] = sorted(contagem.items(), key=lambda x: -x[1])[:5]

        perfil.append(info)
    return perfil


def duplicadas(linhas):
    vistas, dup = set(), 0
    for l in linhas:
        chave = tuple((l.get(k) or "") for k in l)
        if chave in vistas:
            dup += 1
        else:
            vistas.add(chave)
    return dup


# ---------------------------------------------------------------- perfil

def perfil(caminho):
    titulo("MODULO 6 - CICLO 6.2 - PERFIL DA BASE")
    linhas, separador, codificacao = abrir(caminho)
    if linhas is None:
        return 1
    if not linhas:
        print("O arquivo tem cabecalho mas nenhuma linha de dados.")
        return 1

    p = analisar(linhas)
    dup = duplicadas(linhas)

    print()
    print("Arquivo:      " + caminho)
    print("Separador:    '%s'" % ("tab" if separador == "\t" else separador))
    print("Codificacao:  " + codificacao)
    print("Linhas:       %d" % len(linhas))
    print("Colunas:      %d" % len(p))
    print("Duplicadas:   %d linha(s) identica(s) a outra" % dup)
    print()
    print("%-28s %-11s %8s %9s" % ("COLUNA", "TIPO", "VAZIOS", "DISTINTOS"))
    print("-" * 62)
    for c in p:
        print("%-28s %-11s %7.1f%% %9d"
              % (c["coluna"][:28], c["tipo"], c["pct_vazios"], c["distintos"]))

    os.makedirs("saidas", exist_ok=True)
    base = os.path.splitext(os.path.basename(caminho))[0]
    destino = os.path.join("saidas", "perfil-%s.md" % base)

    L = []
    L.append("# Perfil da base %s" % base)
    L.append("")
    L.append("Modulo 6, ciclo 6.2. DECC0294, UFMA, Curso de Administracao.")
    L.append("Gerado em %s pelo script atividade_modulo6.py."
             % datetime.now().strftime("%d/%m/%Y as %H:%M"))
    L.append("")
    L.append("| Caracteristica | Valor |")
    L.append("|---|---|")
    L.append("| Arquivo | %s |" % caminho)
    L.append("| Separador | %s |" % ("tab" if separador == "\t" else separador))
    L.append("| Codificacao | %s |" % codificacao)
    L.append("| Linhas | %d |" % len(linhas))
    L.append("| Colunas | %d |" % len(p))
    L.append("| Linhas duplicadas | %d |" % dup)
    L.append("")
    L.append("## Visao geral das colunas")
    L.append("")
    L.append("| Coluna | Tipo | Vazios | % vazios | Distintos |")
    L.append("|---|---|---|---|---|")
    for c in p:
        L.append("| %s | %s | %d | %.1f%% | %d |"
                 % (c["coluna"], c["tipo"], c["vazios"], c["pct_vazios"], c["distintos"]))
    L.append("")
    L.append("## Colunas numericas")
    L.append("")
    numericas = [c for c in p if c["tipo"] == "numero" and c["nums"]]
    if numericas:
        L.append("| Coluna | Minimo | Mediana | Media | Maximo | Soma |")
        L.append("|---|---|---|---|---|---|")
        for c in numericas:
            L.append("| %s | %s | %s | %s | %s | %s |"
                     % (c["coluna"], fmt(c["min"]), fmt(c["mediana"]),
                        fmt(c["media"]), fmt(c["max"]), fmt(c["soma"])))
        L.append("")
        L.append("Quando a media fica muito acima da mediana, ha poucos valores altos")
        L.append("puxando o resumo. Apresente as duas medidas no seu relatorio.")
    else:
        L.append("Nenhuma coluna foi reconhecida como numerica.")
        L.append("")
        L.append("Se voce esperava colunas de valor aqui, o motivo mais provavel e a")
        L.append("virgula decimal lida como texto. Confira a exportacao da base.")
    L.append("")
    L.append("## Colunas de categoria e texto")
    L.append("")
    for c in p:
        if c["tipo"] in ("categoria", "texto") and c["exemplos"]:
            L.append("### %s (%s, %d valores distintos)"
                     % (c["coluna"], c["tipo"], c["distintos"]))
            L.append("")
            for valor, cont in c["exemplos"]:
                L.append("- %s: %d ocorrencia(s)" % (valor[:70], cont))
            L.append("")
    L.append("## O que olhar neste perfil")
    L.append("")
    L.append("- Coluna com um unico valor distinto nao informa nada e pode sair da analise.")
    L.append("- Coluna com todos os valores distintos costuma ser identificador.")
    L.append("- Percentual de vazios acima de 20% limita qualquer conclusao sobre a coluna.")
    L.append("- Maximo muito acima da mediana e onde moram os erros de digitacao.")
    L.append("- Linha duplicada infla contagem e soma. Confira antes de calcular qualquer total.")
    L.append("")
    L.append("## Minhas tres observacoes ao ler este perfil")
    L.append("")
    L.append("ESCREVA AQUI as tres coisas que mais surpreenderam voce:")
    L.append("")
    L.append("1. ")
    L.append("2. ")
    L.append("3. ")
    L.append("")

    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print()
    print("Perfil gravado em: " + destino)
    print()
    print("PROXIMO PASSO")
    print("  Leia o perfil inteiro e escreva as suas tres observacoes ao final dele.")
    print("  Depois: 'execute atividade_modulo6.py com o comando atipicos %s'" % caminho)
    return 0


# -------------------------------------------------------------- atipicos

def atipicos(caminho):
    titulo("MODULO 6 - CICLO 6.3 - VALORES ATIPICOS E AUSENTES")
    linhas, _, _ = abrir(caminho)
    if linhas is None:
        return 1

    p = analisar(linhas)
    casos = []

    for c in p:
        if c["pct_vazios"] > 0:
            casos.append({
                "coluna": c["coluna"], "caso": "valores ausentes",
                "valor": "%d vazios (%.1f%%)" % (c["vazios"], c["pct_vazios"]),
                "linha": "-",
            })

    for c in p:
        if c["tipo"] != "numero" or len(c["nums"]) < 8:
            continue
        q1, q3 = quartis(c["nums"])
        if q1 is None:
            continue
        amplitude = q3 - q1
        if amplitude == 0:
            continue
        piso, teto = q1 - 1.5 * amplitude, q3 + 1.5 * amplitude
        fora = []
        for i, l in enumerate(linhas, start=2):
            v = numero((l.get(c["coluna"]) or "").strip())
            if v is not None and (v < piso or v > teto):
                fora.append((v, i))
        fora.sort(key=lambda x: x[0])
        selecionados = fora[:5] + fora[-5:] if len(fora) > 10 else fora
        vistos = set()
        for v, i in selecionados:
            if i in vistos:
                continue
            vistos.add(i)
            casos.append({
                "coluna": c["coluna"], "caso": "valor atipico",
                "valor": fmt(v), "linha": str(i),
            })
        if fora:
            print("  %-28s %d valor(es) fora do intervalo usual [%s .. %s]"
                  % (c["coluna"][:28], len(fora), fmt(piso), fmt(teto)))

    if not casos:
        print()
        print("Nenhum valor ausente e nenhum valor atipico encontrado.")
        print("Isso e incomum. Confira se o arquivo lido e mesmo o do seu projeto.")
        return 0

    os.makedirs("entregas", exist_ok=True)
    if os.path.exists(TRATAMENTO):
        print()
        print("O formulario ja existe: " + TRATAMENTO)
        print("Nada foi sobrescrito. Para recomecar, renomeie o arquivo atual.")
        return 0

    with open(TRATAMENTO, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=SEP)
        w.writerow(COLS_TRATAMENTO)
        for caso in casos:
            w.writerow([caso["coluna"], caso["caso"], caso["valor"], caso["linha"], "", "", ""])

    print()
    print("Casos a decidir: %d" % len(casos))
    print("Formulario criado em: " + TRATAMENTO)
    print()
    print("COMO PREENCHER")
    print()
    print("  classificacao   Para ausentes: ausente ao acaso, ausente por regra ou")
    print("                  ausente com vies.")
    print("                  Para atipicos: erro de registro, unidade trocada ou")
    print("                  realidade.")
    print()
    print("  decisao         manter, corrigir, separar, excluir ou nao preencher.")
    print()
    print("  razao           Por que voce decidiu assim. Obrigatorio: o script recusa")
    print("                  decisao sem razao escrita.")
    print()
    print("Antes de decidir sobre um atipico, abra o arquivo e olhe a linha inteira.")
    print("O contexto quase sempre explica o valor.")
    return 0


# ------------------------------------------------------------------- log

def criar_log():
    titulo("MODULO 6 - CICLO 6.4 - LOG DE VERIFICACAO")
    os.makedirs("entregas", exist_ok=True)
    if os.path.exists(LOG):
        print()
        print("O arquivo ja existe: " + LOG)
        return 0
    with open(LOG, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=SEP)
        w.writerow(COLS_LOG)
        for _ in range(5):
            w.writerow([""] * len(COLS_LOG))
    print()
    print("Formulario criado em: " + LOG)
    print()
    print("COMO PREENCHER, uma linha por numero calculado")
    print()
    print("  numero               Um nome curto para o numero. Ex.: custo por atendimento")
    print("  o_que_mede           Numerador, denominador, periodo e recorte.")
    print("  valor                O resultado obtido.")
    print("  total_fecha          A soma das partes bate com o total independente?")
    print("                       sim, nao ou nao se aplica.")
    print("  contagem_fecha       O numero de registros usados e o esperado? sim/nao.")
    print("  ordem_de_grandeza    O valor faz sentido no mundo real? sim/nao.")
    print("  linha_recalculada    Voce refez o calculo de uma linha na mao? sim/nao.")
    print("  conclusao            O numero pode ir para o relatorio, ou o que falta.")
    print()
    print("Numero que nao fecha e fica sem explicacao nao vai para relatorio nenhum.")
    return 0


# -------------------------------------------------------------- conferir

def conferir():
    titulo("MODULO 6 - CONFERENCIA DAS ENTREGAS")
    erros, avisos = [], []
    tratamentos, verificacoes = [], []

    if not os.path.exists(TRATAMENTO):
        erros.append("nao encontrei " + TRATAMENTO + ". Execute o comando 'atipicos'.")
    else:
        with open(TRATAMENTO, newline="", encoding="utf-8-sig") as f:
            for i, l in enumerate(csv.DictReader(f, delimiter=SEP), start=2):
                if not (l.get("coluna") or "").strip():
                    continue
                classificacao = (l.get("classificacao") or "").strip().lower()
                decisao = (l.get("decisao") or "").strip().lower()
                razao = (l.get("razao") or "").strip()
                if classificacao not in CLASSIFICACOES:
                    erros.append("tratamento, linha %d: classificacao invalida ('%s')"
                                 % (i, l.get("classificacao")))
                if decisao not in DECISOES:
                    erros.append("tratamento, linha %d: decisao deveria ser manter, "
                                 "corrigir, separar, excluir ou nao preencher" % i)
                if len(razao) < 15:
                    erros.append("tratamento, linha %d: razao vazia ou curta demais. "
                                 "Decisao sem razao escrita nao conta." % i)
                if decisao == "excluir" and classificacao == "realidade":
                    erros.append("tratamento, linha %d: excluir um valor classificado como "
                                 "realidade nao e limpeza. Separe em analise propria." % i)
                tratamentos.append({"coluna": l.get("coluna"), "caso": l.get("caso"),
                                    "valor": l.get("valor"), "classificacao": classificacao,
                                    "decisao": decisao, "razao": razao})

    if not os.path.exists(LOG):
        erros.append("nao encontrei " + LOG + ". Execute o comando 'log'.")
    else:
        with open(LOG, newline="", encoding="utf-8-sig") as f:
            for i, l in enumerate(csv.DictReader(f, delimiter=SEP), start=2):
                if not (l.get("numero") or "").strip():
                    continue
                mede = (l.get("o_que_mede") or "").strip()
                if len(mede) < 20:
                    erros.append("log, linha %d: o_que_mede precisa dizer numerador, "
                                 "denominador, periodo e recorte." % i)
                checagens = {}
                for campo in ("total_fecha", "contagem_fecha", "ordem_de_grandeza",
                              "linha_recalculada"):
                    v = (l.get(campo) or "").strip().lower()
                    if v not in SIM_NAO:
                        erros.append("log, linha %d: %s deveria ser sim, nao ou "
                                     "nao se aplica" % (i, campo))
                    checagens[campo] = v
                conclusao = (l.get("conclusao") or "").strip()
                if len(conclusao) < 10:
                    erros.append("log, linha %d: escreva a conclusao sobre o numero" % i)
                if checagens.get("linha_recalculada") == "nao":
                    avisos.append("log, linha %d: nenhuma linha recalculada na mao. "
                                  "E a conferencia mais barata que existe." % i)
                if "nao" in (checagens.get("total_fecha"), checagens.get("contagem_fecha")) \
                        and len(conclusao) < 40:
                    erros.append("log, linha %d: alguma conferencia falhou. A conclusao "
                                 "precisa dizer o que voce fez a respeito." % i)
                verificacoes.append({"numero": l.get("numero"), "mede": mede,
                                     "valor": l.get("valor"), "checagens": checagens,
                                     "conclusao": conclusao})

    if len(verificacoes) < 5:
        erros.append("o log precisa de cinco numeros, e tem %d." % len(verificacoes))

    print()
    if erros:
        print("PROBLEMAS QUE PRECISAM SER CORRIGIDOS (%d):" % len(erros))
        for e in erros:
            print("  - " + e)
    else:
        print("Nenhum problema encontrado.")
    if avisos:
        print()
        print("PONTOS PARA VOCE REVER (%d):" % len(avisos))
        for a in avisos:
            print("  - " + a)

    print()
    print("Casos de tratamento decididos: %d" % len(tratamentos))
    print("Numeros verificados: %d de 5" % len(verificacoes))

    if erros:
        print()
        print("O relatorio nao foi gerado. Corrija os arquivos e execute 'conferir' de novo.")
        return 1

    gerar_relatorio(tratamentos, verificacoes, avisos)
    print()
    print("Relatorio gerado em: " + RELATORIO)
    print()
    print("ULTIMO PASSO")
    print("  Abra o relatorio e escreva a resposta a pergunta que voce escolheu no")
    print("  ciclo 6.1, com a limitacao que o tratamento e a qualidade da base impoem.")
    return 0


def gerar_relatorio(tratamentos, verificacoes, avisos):
    L = []
    L.append("# Relatorio do modulo 6")
    L.append("")
    L.append("Analise exploratoria. DECC0294, UFMA, Curso de Administracao.")
    L.append("Gerado em %s pelo script atividade_modulo6.py."
             % date.today().strftime("%d/%m/%Y"))
    L.append("")
    L.append("Nome e matricula: ______________________________")
    L.append("")
    L.append("## Tratamento de ausentes e atipicos")
    L.append("")
    L.append("| Coluna | Caso | Valor | Classificacao | Decisao | Razao |")
    L.append("|---|---|---|---|---|---|")
    for t in tratamentos:
        L.append("| %s | %s | %s | %s | %s | %s |"
                 % (t["coluna"], t["caso"], t["valor"], t["classificacao"],
                    t["decisao"], t["razao"]))
    L.append("")
    L.append("## Log de verificacao dos numeros")
    L.append("")
    for v in verificacoes:
        L.append("### %s" % v["numero"])
        L.append("")
        L.append("- O que mede: %s" % v["mede"])
        L.append("- Valor: %s" % v["valor"])
        L.append("- O total fecha: %s" % v["checagens"].get("total_fecha"))
        L.append("- A contagem fecha: %s" % v["checagens"].get("contagem_fecha"))
        L.append("- Ordem de grandeza plausivel: %s" % v["checagens"].get("ordem_de_grandeza"))
        L.append("- Linha recalculada na mao: %s" % v["checagens"].get("linha_recalculada"))
        L.append("- Conclusao: %s" % v["conclusao"])
        L.append("")
    if avisos:
        L.append("## Pontos marcados pelo script")
        L.append("")
        for a in avisos:
            L.append("- %s" % a)
        L.append("")
    L.append("## Resposta a pergunta do ciclo 6.1")
    L.append("")
    L.append("ESCREVA AQUI a pergunta escolhida e a resposta que a base sustenta:")
    L.append("")
    L.append("> ")
    L.append("")
    L.append("## O que esta resposta nao permite afirmar")
    L.append("")
    L.append("ESCREVA AQUI as limitacoes: o que o tratamento mudou, o que a")
    L.append("incompletude impede e o periodo que a base nao cobre.")
    L.append("")
    L.append("> ")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Declaracao de uso de inteligencia artificial")
    L.append("")
    L.append("Ferramenta e modelo usados: ______________________________")
    L.append("")
    L.append("Os scripts de calculo estao gravados na pasta saidas. Os numeros foram")
    L.append("conferidos por mim conforme o log acima.")
    L.append("")
    with open(RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main():
    args = sys.argv[1:]
    cmd = (args[0].strip().lower() if args else "")
    if cmd == "perfil":
        if len(args) < 2:
            print("Faltou o arquivo. Uso: perfil dados/SEU-ARQUIVO.csv")
            return 1
        return perfil(args[1])
    if cmd in ("atipicos", "atípicos"):
        if len(args) < 2:
            print("Faltou o arquivo. Uso: atipicos dados/SEU-ARQUIVO.csv")
            return 1
        return atipicos(args[1])
    if cmd == "log":
        return criar_log()
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    print(__doc__)
    print("Comandos disponiveis:")
    print("  python atividade_modulo6.py perfil dados/ARQUIVO.csv     perfila a base")
    print("  python atividade_modulo6.py atipicos dados/ARQUIVO.csv   aponta os casos")
    print("  python atividade_modulo6.py log                          cria o log")
    print("  python atividade_modulo6.py conferir                     valida e gera")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
    except KeyboardInterrupt:
        print()
        print("Interrompido.")
        sys.exit(1)
