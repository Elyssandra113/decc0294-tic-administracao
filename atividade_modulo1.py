#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 1 - Mapa de tarefas automatizaveis
 DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
 UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que conduz a atividade do ciclo 1.4 do comeco ao fim.
    Voce nao precisa saber programar. Voce precisa saber pedir ao agente que
    ele execute o script, e depois preencher um arquivo de planilha.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute o arquivo atividade_modulo1.py com o comando iniciar"
       O script cria o formulario em entregas/modulo1-mapa-de-tarefas.csv

    2) Abra esse arquivo no Excel (ou no editor de texto) e preencha as suas
       dez tarefas. Salve mantendo o formato CSV, separado por ponto e virgula.

    3) "execute o arquivo atividade_modulo1.py com o comando conferir"
       O script valida o preenchimento, ordena as tarefas por prioridade e
       gera o mapa em entregas/modulo1-mapa-de-tarefas.md

    Se quiser ver as instrucoes de novo, peca: "execute atividade_modulo1.py"
    sem nenhum comando.

O QUE O SCRIPT NAO FAZ
    Ele nao decide por voce. As notas de esforco, ganho e risco sao seu
    julgamento. O script so confere se o preenchimento esta completo e
    coerente, e organiza o resultado.

Nao precisa instalar nada. Roda com o Python que ja vem com o ambiente.
=============================================================================
"""

import csv
import os
import sys
from datetime import date

PASTA = "entregas"
CSV = os.path.join(PASTA, "modulo1-mapa-de-tarefas.csv")
MD = os.path.join(PASTA, "modulo1-mapa-de-tarefas.md")
SEP = ";"

COLUNAS = [
    "tarefa",
    "quem_executa",
    "frequencia",
    "destino",
    "esforco_1a5",
    "ganho_horas_mes",
    "base_da_estimativa",
    "risco_1a5",
]

DESTINOS = {"automatizar", "aumentar", "manter humana"}

EXEMPLO = [
    [
        "Consolidar as planilhas de frequencia das quatro unidades num arquivo unico",
        "assistente administrativo",
        "mensal",
        "automatizar",
        "2",
        "6",
        "leva cerca de 1h30 por unidade, quatro vezes por mes",
        "2",
    ]
]

LINHA_VAZIA = ["", "", "", "", "", "", "", ""]


def titulo(txt):
    print()
    print("=" * 74)
    print(" " + txt)
    print("=" * 74)


def ajuda():
    print(__doc__)


def iniciar():
    titulo("MODULO 1 - CICLO 1.4 - CRIACAO DO FORMULARIO")
    os.makedirs(PASTA, exist_ok=True)

    if os.path.exists(CSV):
        print()
        print("O arquivo ja existe: " + CSV)
        print("Nada foi sobrescrito. Se quiser recomecar do zero, renomeie o")
        print("arquivo atual e execute 'iniciar' de novo.")
        return 0

    with open(CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=SEP)
        w.writerow(COLUNAS)
        for linha in EXEMPLO:
            w.writerow(linha)
        for _ in range(10):
            w.writerow(LINHA_VAZIA)

    print()
    print("Formulario criado em: " + CSV)
    print()
    print("COMO PREENCHER")
    print()
    print("  tarefa               O que se faz, com verbo no infinitivo e objeto")
    print("                       definido. 'Cuidar do setor' nao e tarefa.")
    print("                       'Conferir as notas fiscais do mes' e tarefa.")
    print()
    print("  quem_executa         O cargo que faz a tarefa hoje.")
    print()
    print("  frequencia           diaria, semanal, quinzenal, mensal, trimestral,")
    print("                       anual ou eventual.")
    print()
    print("  destino              automatizar, aumentar ou manter humana.")
    print("                       Use a definicao do ciclo 1.3.")
    print()
    print("  esforco_1a5          Quanto custa mudar a tarefa.")
    print("                       1 = uma tarde. 5 = projeto de meses com outras")
    print("                       areas envolvidas.")
    print()
    print("  ganho_horas_mes      Quantas horas por mes se economiza. Numero, pode")
    print("                       ter virgula decimal. Estimativa grosseira serve.")
    print()
    print("  base_da_estimativa   Como voce chegou nesse numero. Esta coluna e")
    print("                       obrigatoria: numero sem base declarada nao conta.")
    print()
    print("  risco_1a5            O que acontece se der errado e ninguem perceber.")
    print("                       1 = corrige-se sozinho. 5 = dano a terceiro,")
    print("                       sancao ou perda irreversivel.")
    print()
    print("A primeira linha ja vem preenchida como exemplo. Apague-a ou substitua-a.")
    print("Sao necessarias dez tarefas.")
    print()
    print("Quando terminar, peca ao agente:")
    print('  "execute atividade_modulo1.py com o comando conferir"')
    return 0


def ler_linhas():
    with open(CSV, newline="", encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f, delimiter=SEP))
    return [l for l in linhas if (l.get("tarefa") or "").strip()]


def num(valor, campo, i, erros, inteiro=True, minimo=None, maximo=None):
    bruto = (valor or "").strip().replace(",", ".")
    if not bruto:
        erros.append("linha %d: %s esta vazio" % (i, campo))
        return None
    try:
        v = float(bruto)
    except ValueError:
        erros.append("linha %d: %s deveria ser um numero, veio '%s'" % (i, campo, bruto))
        return None
    if inteiro and v != int(v):
        erros.append("linha %d: %s deveria ser um numero inteiro" % (i, campo))
        return None
    if minimo is not None and v < minimo:
        erros.append("linha %d: %s deveria estar entre %s e %s" % (i, campo, minimo, maximo))
        return None
    if maximo is not None and v > maximo:
        erros.append("linha %d: %s deveria estar entre %s e %s" % (i, campo, minimo, maximo))
        return None
    return v


def conferir():
    titulo("MODULO 1 - CICLO 1.4 - CONFERENCIA E GERACAO DO MAPA")

    if not os.path.exists(CSV):
        print()
        print("Nao encontrei o arquivo " + CSV)
        print("Execute primeiro o comando 'iniciar'.")
        return 1

    linhas = ler_linhas()
    erros = []
    avisos = []
    tarefas = []

    if not linhas:
        print()
        print("O arquivo esta vazio. Preencha as tarefas antes de conferir.")
        return 1

    for i, l in enumerate(linhas, start=2):
        tarefa = (l.get("tarefa") or "").strip()

        if tarefa == EXEMPLO[0][0]:
            avisos.append("linha %d: a linha de exemplo continua no arquivo" % i)
            continue

        if len(tarefa.split()) < 3:
            erros.append("linha %d: a tarefa parece curta demais para ter verbo e objeto" % i)

        destino = (l.get("destino") or "").strip().lower()
        if destino not in DESTINOS:
            erros.append(
                "linha %d: destino deveria ser automatizar, aumentar ou manter humana, veio '%s'"
                % (i, l.get("destino"))
            )

        if not (l.get("quem_executa") or "").strip():
            erros.append("linha %d: quem_executa esta vazio" % i)
        if not (l.get("frequencia") or "").strip():
            erros.append("linha %d: frequencia esta vazia" % i)

        base = (l.get("base_da_estimativa") or "").strip()
        if len(base) < 15:
            erros.append(
                "linha %d: base_da_estimativa esta vazia ou curta demais. "
                "Numero sem base declarada nao conta." % i
            )

        esforco = num(l.get("esforco_1a5"), "esforco_1a5", i, erros, True, 1, 5)
        risco = num(l.get("risco_1a5"), "risco_1a5", i, erros, True, 1, 5)
        ganho = num(l.get("ganho_horas_mes"), "ganho_horas_mes", i, erros, False, 0, None)

        if None in (esforco, risco, ganho):
            continue

        if destino == "manter humana" and risco <= 2:
            avisos.append(
                "linha %d: destino 'manter humana' com risco baixo. Confira se e mesmo o caso." % i
            )
        if destino == "automatizar" and risco >= 4:
            avisos.append(
                "linha %d: destino 'automatizar' com risco alto. Reveja: risco 4 ou 5 nao entra "
                "na primeira leva." % i
            )

        tarefas.append(
            {
                "tarefa": tarefa,
                "quem": l.get("quem_executa", "").strip(),
                "freq": l.get("frequencia", "").strip(),
                "destino": destino,
                "esforco": int(esforco),
                "ganho": ganho,
                "base": base,
                "risco": int(risco),
                "prio": ganho / esforco if esforco else 0,
            }
        )

    print()
    if erros:
        print("PROBLEMAS QUE PRECISAM SER CORRIGIDOS (%d):" % len(erros))
        for e in erros:
            print("  - " + e)
    else:
        print("Nenhum problema de preenchimento encontrado.")

    if avisos:
        print()
        print("PONTOS PARA VOCE REVER (%d):" % len(avisos))
        for a in avisos:
            print("  - " + a)

    print()
    print("Tarefas validas: %d de 10 esperadas." % len(tarefas))

    if erros:
        print()
        print("O mapa nao foi gerado. Corrija o arquivo e execute 'conferir' de novo.")
        return 1

    if len(tarefas) < 10:
        print()
        print("Faltam tarefas. O mapa foi gerado assim mesmo, mas a entrega pede dez.")

    gerar_mapa(tarefas, avisos)
    print()
    print("Mapa gerado em: " + MD)
    print()
    print("ULTIMO PASSO, E O QUE MAIS VALE NOTA")
    print("  Abra o arquivo " + MD)
    print("  Escreva, ao final, a sua primeira acao: uma tarefa, uma frase, o que")
    print("  voce faria na segunda-feira. Depois escreva uma linha sobre o que")
    print("  mudaria no mapa se tivesse acesso a mais informacao.")
    return 0


def faixa_risco(t):
    return "alto" if t["risco"] >= 4 else ("medio" if t["risco"] == 3 else "baixo")


def gerar_mapa(tarefas, avisos):
    primeiros = sorted(
        [t for t in tarefas if t["risco"] <= 3 and t["destino"] != "manter humana"],
        key=lambda t: -t["prio"],
    )
    adiar = sorted([t for t in tarefas if t["risco"] >= 4], key=lambda t: -t["prio"])
    humanas = [t for t in tarefas if t["destino"] == "manter humana"]

    total_ganho = sum(t["ganho"] for t in primeiros[:3])

    L = []
    L.append("# Mapa de tarefas automatizaveis")
    L.append("")
    L.append("Modulo 1, ciclo 1.4. DECC0294, UFMA, Curso de Administracao.")
    L.append("Gerado em %s pelo script atividade_modulo1.py." % date.today().strftime("%d/%m/%Y"))
    L.append("")
    L.append("Preencher nome e matricula: ______________________________")
    L.append("")
    L.append("## 1. Ordem de ataque")
    L.append("")
    L.append(
        "Tarefas ordenadas por ganho dividido por esforco, excluidas as de risco alto "
        "e as de destino humano. A primeira linha e por onde comecar."
    )
    L.append("")
    L.append("| # | Tarefa | Destino | Esforco | Ganho (h/mes) | Risco | Prioridade |")
    L.append("|---|---|---|---|---|---|---|")
    for i, t in enumerate(primeiros, 1):
        L.append(
            "| %d | %s | %s | %d | %s | %d | %.1f |"
            % (i, t["tarefa"], t["destino"], t["esforco"], fmt(t["ganho"]), t["risco"], t["prio"])
        )
    L.append("")
    if primeiros:
        L.append(
            "As tres primeiras somam %s horas por mes de ganho estimado." % fmt(total_ganho)
        )
        L.append("")

    if adiar:
        L.append("## 2. Risco alto: nao comecar por aqui")
        L.append("")
        L.append(
            "Um erro visivel numa primeira iniciativa encerra o assunto na organizacao "
            "por anos. Estas tarefas ficam para depois, com controle explicito."
        )
        L.append("")
        L.append("| Tarefa | Risco | Ganho (h/mes) |")
        L.append("|---|---|---|")
        for t in adiar:
            L.append("| %s | %d | %s |" % (t["tarefa"], t["risco"], fmt(t["ganho"])))
        L.append("")

    if humanas:
        L.append("## 3. Tarefas que ficam humanas")
        L.append("")
        for t in humanas:
            L.append("- %s (risco %d)" % (t["tarefa"], t["risco"]))
        L.append("")

    L.append("## 4. Todas as tarefas, com a base da estimativa")
    L.append("")
    for t in sorted(tarefas, key=lambda t: -t["prio"]):
        L.append("### %s" % t["tarefa"])
        L.append("")
        L.append("- Quem executa hoje: %s" % t["quem"])
        L.append("- Frequencia: %s" % t["freq"])
        L.append("- Destino: %s" % t["destino"])
        L.append(
            "- Esforco %d de 5, ganho %s h/mes, risco %d de 5 (%s)"
            % (t["esforco"], fmt(t["ganho"]), t["risco"], faixa_risco(t))
        )
        L.append("- Base da estimativa: %s" % t["base"])
        L.append("")

    if avisos:
        L.append("## 5. Pontos que o script marcou para revisao")
        L.append("")
        for a in avisos:
            L.append("- %s" % a)
        L.append("")

    L.append("## 6. Primeira acao")
    L.append("")
    L.append("ESCREVA AQUI, em uma frase, o que voce faria na segunda-feira:")
    L.append("")
    L.append("> ")
    L.append("")
    L.append("## 7. O que mudaria com mais informacao")
    L.append("")
    L.append("ESCREVA AQUI, em uma linha:")
    L.append("")
    L.append("> ")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Declaracao de uso de inteligencia artificial")
    L.append("")
    L.append("Ferramenta e modelo usados: ______________________________")
    L.append("")
    L.append(
        "As instrucoes dadas ao agente estao registradas na pasta prompts. "
        "As classificacoes foram revisadas por mim e as divergencias estao anotadas."
    )
    L.append("")

    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def fmt(v):
    return ("%.1f" % v).replace(".0", "").replace(".", ",")


def main():
    cmd = (sys.argv[1].strip().lower() if len(sys.argv) > 1 else "")
    if cmd in ("iniciar", "criar", "start"):
        return iniciar()
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    ajuda()
    print("Comandos disponiveis:")
    print("  python atividade_modulo1.py iniciar    cria o formulario")
    print("  python atividade_modulo1.py conferir   valida e gera o mapa")
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
