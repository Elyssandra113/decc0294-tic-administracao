#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 5 - Mapa de dados e fechamento da entrega A2
 DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
 UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que monta o mapa de dados do seu projeto e depois confere
    a entrega A2 inteira, que fecha a nota 1.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute o arquivo atividade_modulo5.py com o comando iniciar"
       Cria o formulario em entregas/modulo5-mapa-de-dados.csv

    2) Preencha uma linha por fonte. Reaproveite o inventario do ciclo 5.1 e
       o diagnostico de qualidade do ciclo 5.3: a informacao ja foi levantada.

    3) "execute o arquivo atividade_modulo5.py com o comando conferir"
       Valida o preenchimento e gera o mapa em
       entregas/modulo5-mapa-de-dados.md

    4) "execute o arquivo atividade_modulo5.py com o comando a2"
       Percorre os arquivos dos modulos 1, 3, 4 e 5, diz o que falta e grava
       entregas/A2-relatorio.md

    Sem nenhum comando, o script imprime estas instrucoes.

A REGRA QUE O SCRIPT APLICA
    Quatro fontes no minimo, e ao menos uma externa. Linha sem data de
    extracao e sem responsavel e recusada: sao esses dois campos que tornam
    a analise refazivel.

Nao precisa instalar nada. Roda com o Python que ja vem com o ambiente.
=============================================================================
"""

import csv
import os
import re
import sys
from datetime import date, datetime

PASTA = "entregas"
CSV = os.path.join(PASTA, "modulo5-mapa-de-dados.csv")
MD = os.path.join(PASTA, "modulo5-mapa-de-dados.md")
A2 = os.path.join(PASTA, "A2-relatorio.md")
SEP = ";"
MINIMO = 4

COLUNAS = [
    "fonte",
    "origem",
    "forma",
    "o_que_registra",
    "como_e_obtida",
    "data_da_extracao",
    "completude_percentual",
    "principal_inconsistencia",
    "dono_do_dado",
    "custodiante",
]

ORIGENS = {"transacional", "cadastro", "externo"}
FORMAS = {"estruturado", "semiestruturado", "nao estruturado"}
OBTENCOES = {"exportacao manual", "arquivo periodico", "api"}
NAO_SEI = "nao informado"

EXEMPLO = [
    "Sistema de protocolo da autarquia",
    "transacional",
    "estruturado",
    "Cada documento recebido, com data, assunto, setor de destino e situacao",
    "exportacao manual",
    "15/09/2026",
    "92",
    "Setor de destino em branco em 8% dos registros de 2024",
    "Coordenacao de Protocolo",
    "Setor de TI",
]


def titulo(t):
    print()
    print("=" * 74)
    print(" " + t)
    print("=" * 74)


def iniciar():
    titulo("MODULO 5 - CICLO 5.4 - CRIACAO DO MAPA DE DADOS")
    os.makedirs(PASTA, exist_ok=True)

    if os.path.exists(CSV):
        print()
        print("O arquivo ja existe: " + CSV)
        print("Nada foi sobrescrito. Para recomecar, renomeie o arquivo atual.")
        return 0

    with open(CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=SEP)
        w.writerow(COLUNAS)
        w.writerow(EXEMPLO)
        for _ in range(MINIMO):
            w.writerow([""] * len(COLUNAS))

    print()
    print("Formulario criado em: " + CSV)
    print()
    print("COMO PREENCHER")
    print()
    print("  fonte                      Nome do sistema, da planilha ou da base.")
    print()
    print("  origem                     transacional, cadastro ou externo.")
    print()
    print("  forma                      estruturado, semiestruturado ou nao estruturado.")
    print()
    print("  o_que_registra             O que cada linha da base representa no mundo.")
    print()
    print("  como_e_obtida              exportacao manual, arquivo periodico ou api.")
    print()
    print("  data_da_extracao           dd/mm/aaaa. Quando voce pegou este dado.")
    print("                             Obrigatorio: sem ele ninguem refaz a analise.")
    print()
    print("  completude_percentual      Percentual de preenchimento medido no ciclo 5.3.")
    print("                             Numero de 0 a 100, sem o sinal.")
    print()
    print("  principal_inconsistencia   O defeito mais relevante que voce encontrou.")
    print("                             Se nao encontrou nenhum, escreva 'nenhuma'.")
    print()
    print("  dono_do_dado               Quem define o que os campos significam.")
    print("                             Se voce nao sabe, escreva NAO INFORMADO.")
    print()
    print("  custodiante                Quem guarda e libera o acesso.")
    print("                             Se voce nao sabe, escreva NAO INFORMADO.")
    print()
    print("Sao necessarias %d fontes, e pelo menos uma precisa ser externa." % MINIMO)
    print("A primeira linha vem preenchida como exemplo. Apague-a ou substitua-a.")
    print()
    print("Quando terminar:")
    print('  "execute atividade_modulo5.py com o comando conferir"')
    return 0


def conferir():
    titulo("MODULO 5 - CICLO 5.4 - CONFERENCIA DO MAPA")

    if not os.path.exists(CSV):
        print()
        print("Nao encontrei " + CSV + ". Execute primeiro o comando 'iniciar'.")
        return 1

    with open(CSV, newline="", encoding="utf-8-sig") as f:
        linhas = [l for l in csv.DictReader(f, delimiter=SEP)
                  if (l.get("fonte") or "").strip()]

    erros, avisos, fontes = [], [], []

    for i, l in enumerate(linhas, start=2):
        nome = (l.get("fonte") or "").strip()
        if nome == EXEMPLO[0]:
            avisos.append("linha %d: a linha de exemplo continua no arquivo" % i)
            continue

        origem = (l.get("origem") or "").strip().lower()
        if origem not in ORIGENS:
            erros.append("linha %d: origem deveria ser transacional, cadastro ou externo" % i)

        forma = (l.get("forma") or "").strip().lower()
        if forma not in FORMAS:
            erros.append("linha %d: forma deveria ser estruturado, semiestruturado ou "
                         "nao estruturado" % i)

        obtencao = (l.get("como_e_obtida") or "").strip().lower()
        if obtencao not in OBTENCOES:
            erros.append("linha %d: como_e_obtida deveria ser exportacao manual, "
                         "arquivo periodico ou api" % i)

        registra = (l.get("o_que_registra") or "").strip()
        if len(registra) < 20:
            erros.append("linha %d: o_que_registra esta vazio ou curto demais. "
                         "Diga o que cada linha da base representa." % i)

        data = (l.get("data_da_extracao") or "").strip()
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", data):
            erros.append("linha %d: data_da_extracao precisa estar em dd/mm/aaaa" % i)
        else:
            try:
                datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                erros.append("linha %d: data_da_extracao nao e uma data valida" % i)

        bruto = (l.get("completude_percentual") or "").strip().replace(",", ".").replace("%", "")
        try:
            completude = float(bruto)
            if not (0 <= completude <= 100):
                erros.append("linha %d: completude_percentual deveria estar entre 0 e 100" % i)
                completude = None
        except ValueError:
            erros.append("linha %d: completude_percentual deveria ser um numero de 0 a 100" % i)
            completude = None

        inconsistencia = (l.get("principal_inconsistencia") or "").strip()
        if not inconsistencia:
            erros.append("linha %d: principal_inconsistencia esta vazia. "
                         "Se nao encontrou defeito, escreva 'nenhuma'." % i)

        dono = (l.get("dono_do_dado") or "").strip()
        custodiante = (l.get("custodiante") or "").strip()
        if not dono:
            erros.append("linha %d: dono_do_dado esta vazio. Se voce nao sabe, "
                         "escreva NAO INFORMADO." % i)
        if not custodiante:
            erros.append("linha %d: custodiante esta vazio. Se voce nao sabe, "
                         "escreva NAO INFORMADO." % i)

        if completude is not None and completude < 70:
            avisos.append("linha %d: completude de %.0f%% e baixa. Diga na analise o que "
                          "isso limita." % (i, completude))

        fontes.append({
            "nome": nome, "origem": origem, "forma": forma, "registra": registra,
            "obtencao": obtencao, "data": data, "completude": completude,
            "inconsistencia": inconsistencia, "dono": dono, "custodiante": custodiante,
        })

    externas = [f for f in fontes if f["origem"] == "externo"]
    lacunas = sum(1 for f in fontes
                  if f["dono"].lower() == NAO_SEI or f["custodiante"].lower() == NAO_SEI)

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
    print("Fontes mapeadas: %d (minimo %d)." % (len(fontes), MINIMO))
    print("Fontes externas: %d (minimo 1)." % len(externas))
    print("Responsaveis ainda desconhecidos: %d." % lacunas)

    if len(fontes) < MINIMO:
        erros.append("faltam fontes: sao %d de %d" % (len(fontes), MINIMO))
    if not externas:
        erros.append("nenhuma fonte externa. O cruzamento do ciclo 5.2 precisa entrar no mapa.")

    if erros:
        print()
        print("O mapa nao foi gerado. Corrija o arquivo e execute 'conferir' de novo.")
        return 1

    gerar_mapa(fontes, avisos, lacunas)
    print()
    print("Mapa gerado em: " + MD)
    print()
    print("PROXIMO PASSO")
    print('  "execute atividade_modulo5.py com o comando a2"')
    return 0


def gerar_mapa(fontes, avisos, lacunas):
    L = []
    L.append("# Mapa de dados do projeto")
    L.append("")
    L.append("Modulo 5, ciclo 5.4. DECC0294, UFMA, Curso de Administracao.")
    L.append("Gerado em %s pelo script atividade_modulo5.py."
             % date.today().strftime("%d/%m/%Y"))
    L.append("")
    L.append("Nome e matricula: ______________________________")
    L.append("")
    L.append("Organizacao ou base do projeto: ______________________________")
    L.append("")
    L.append("## Fontes")
    L.append("")
    L.append("| Fonte | Origem | Forma | Obtencao | Extracao | Completude | Dono |")
    L.append("|---|---|---|---|---|---|---|")
    for f in fontes:
        L.append("| %s | %s | %s | %s | %s | %s%% | %s |"
                 % (f["nome"], f["origem"], f["forma"], f["obtencao"], f["data"],
                    ("%.0f" % f["completude"]) if f["completude"] is not None else "-",
                    f["dono"]))
    L.append("")
    L.append("## Detalhe por fonte")
    L.append("")
    for f in fontes:
        L.append("### %s" % f["nome"])
        L.append("")
        L.append("- O que cada linha representa: %s" % f["registra"])
        L.append("- Como e obtida: %s" % f["obtencao"])
        L.append("- Extraida em: %s" % f["data"])
        L.append("- Principal inconsistencia conhecida: %s" % f["inconsistencia"])
        L.append("- Dono do dado: %s" % f["dono"])
        L.append("- Custodiante: %s" % f["custodiante"])
        L.append("")
    if lacunas:
        L.append("## Lacunas de responsabilidade")
        L.append("")
        L.append("Em %d fonte(s) o dono ou o custodiante ainda e desconhecido." % lacunas)
        L.append("ESCREVA AQUI a quem voce perguntaria para preencher cada uma:")
        L.append("")
        L.append("- ")
        L.append("")
    if avisos:
        L.append("## Pontos marcados pelo script")
        L.append("")
        for a in avisos:
            L.append("- %s" % a)
        L.append("")
    L.append("## Limitacoes que este mapa impoe a analise")
    L.append("")
    L.append("ESCREVA AQUI, em ate cinco linhas, o que a qualidade e a defasagem das")
    L.append("fontes impedem de afirmar com seguranca:")
    L.append("")
    L.append("> ")
    L.append("")
    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


# ---------------------------------------------------------------------------
# Conferencia da entrega A2
# ---------------------------------------------------------------------------

ITENS_A2 = [
    ("Mapa de tarefas automatizaveis (modulo 1)",
     [os.path.join("entregas", "modulo1-mapa-de-tarefas.md")]),
    ("Diario de alucinacao (modulo 3)",
     [os.path.join("entregas", "modulo3-diario-de-alucinacao.md")]),
    ("Par de prompts documentado (modulo 3)",
     [os.path.join("prompts", "modulo3-par-de-prompts.md")]),
    ("AGENTS.md testado (modulo 4)", ["AGENTS.md"]),
    ("Registro da bateria de testes (modulo 4)",
     [os.path.join("entregas", "modulo4-registro.csv")]),
    ("Inventario de fontes (ciclo 5.1)",
     [os.path.join("entregas", "modulo5-ciclo1-inventario.csv"),
      os.path.join("entregas", "modulo5-ciclo1-inventario.md")]),
    ("Cruzamento com base publica (ciclo 5.2)",
     [os.path.join("entregas", "modulo5-ciclo2-cruzamento.md")]),
    ("Diagnostico de qualidade (ciclo 5.3)",
     [os.path.join("entregas", "modulo5-ciclo3-qualidade.md")]),
    ("Mapa de dados (ciclo 5.4)", [MD]),
]


def info_git():
    dados = {"repo": os.path.isdir(".git"), "commits": 0, "remoto": None}
    logs = os.path.join(".git", "logs", "HEAD")
    if os.path.exists(logs):
        with open(logs, encoding="utf-8", errors="replace") as f:
            linhas = [l for l in f.read().splitlines() if "\t" in l]
        dados["commits"] = sum(1 for l in linhas
                               if l.split("\t", 1)[1].strip().startswith("commit"))
    cfg = os.path.join(".git", "config")
    if os.path.exists(cfg):
        with open(cfg, encoding="utf-8", errors="replace") as f:
            m = re.search(r'\[remote "origin"\][^\[]*?url\s*=\s*(\S+)', f.read(), re.DOTALL)
            if m:
                dados["remoto"] = m.group(1)
    return dados


def conferir_a2():
    titulo("MODULO 5 - CONFERENCIA DA ENTREGA A2")
    itens = []

    for rotulo, caminhos in ITENS_A2:
        achado = next((c for c in caminhos if os.path.exists(c)), None)
        if achado:
            tamanho = os.path.getsize(achado)
            ok = tamanho > 200
            det = ("Encontrado: %s (%d bytes)." % (achado, tamanho)) if ok else \
                  ("%s existe mas esta quase vazio (%d bytes)." % (achado, tamanho))
        else:
            ok = False
            det = "Nao encontrei " + " nem ".join(caminhos)
        itens.append((ok, rotulo, det))

    g = info_git()
    itens.append((g["repo"], "Pasta sob controle de versao",
                  "Repositorio local encontrado." if g["repo"]
                  else "Adicione a pasta no GitHub Desktop."))
    itens.append((g["commits"] >= 4, "Historico de versoes do bloco",
                  "%d versao(oes) gravada(s)." % g["commits"]))
    itens.append((bool(g["remoto"]), "Repositorio publicado",
                  ("Publicado em: " + g["remoto"]) if g["remoto"]
                  else "Clique em Publish repository, mantendo o repositorio privado."))

    print()
    for ok, rotulo, det in itens:
        print(("  [OK]    " if ok else "  [FALTA] ") + rotulo)
        print("           " + det)

    ok_n = sum(1 for i in itens if i[0])
    print()
    print("Concluidos: %d de %d." % (ok_n, len(itens)))

    L = ["# Relatorio da entrega A2", "",
         "Modulo 5, encontro 6. DECC0294, UFMA, Curso de Administracao.",
         "Gerado em %s pelo script atividade_modulo5.py."
         % datetime.now().strftime("%d/%m/%Y as %H:%M"), "",
         "Situacao: %d de %d itens concluidos." % (ok_n, len(itens)), "",
         "| Item | Situacao | Observacao |", "|---|---|---|"]
    for ok, rotulo, det in itens:
        L.append("| %s | %s | %s |" % (rotulo, "concluido" if ok else "pendente", det))
    L += ["", "## Conferido por mim", "",
          "Nome e matricula: ______________________________", "",
          "Declaro que o repositorio nao contem dado pessoal identificavel de terceiro,",
          "que as fontes usadas estao registradas no mapa de dados e que os numeros",
          "apresentados foram conferidos contra a fonte.", ""]
    os.makedirs(PASTA, exist_ok=True)
    with open(A2, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print()
    print("Relatorio gravado em: " + A2)
    if ok_n < len(itens):
        print()
        print("Resolva os itens pendentes e execute 'a2' de novo antes de publicar.")
        return 1
    print()
    print("Entrega A2 completa. Grave com a mensagem 'entrega A2' e publique.")
    return 0


def main():
    cmd = (sys.argv[1].strip().lower() if len(sys.argv) > 1 else "")
    if cmd in ("iniciar", "criar", "start"):
        return iniciar()
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    if cmd in ("a2", "entrega", "bloco"):
        return conferir_a2()
    print(__doc__)
    print("Comandos disponiveis:")
    print("  python atividade_modulo5.py iniciar    cria o formulario do mapa")
    print("  python atividade_modulo5.py conferir   valida e gera o mapa")
    print("  python atividade_modulo5.py a2         confere a entrega A2 inteira")
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
