#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 7 - Dados estruturados e consulta
 DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
 UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que transforma os seus arquivos CSV em tabelas de um
    banco de dados, executa as suas consultas guardando o SQL usado, e valida
    as juncoes pela contagem de linhas.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute atividade_modulo7.py com o comando banco dados/A.csv dados/B.csv"
       Cria projeto.db com uma tabela por arquivo e imprime o esquema.

    2) "execute atividade_modulo7.py com o comando esquema"
       Mostra as tabelas, as colunas e os tipos. E o que voce mostra ao agente
       antes de pedir uma consulta.

    3) "execute atividade_modulo7.py com o comando sql SELECT ..."
       Executa a consulta, mostra as primeiras linhas e grava o SQL e o
       resultado em saidas/

    4) "execute atividade_modulo7.py com o comando juntar TABELA_A TABELA_B CHAVE"
       Junta as duas tabelas e informa as contagens antes, depois e os
       registros sem par dos dois lados.

    5) "execute atividade_modulo7.py com o comando registrar"
       Cria entregas/modulo7-consultas.csv para voce registrar as cinco
       perguntas.

    6) "execute atividade_modulo7.py com o comando conferir"
       Valida o registro e gera entregas/modulo7-relatorio.md

    Sem nenhum comando, o script imprime estas instrucoes.

A REGRA QUE O SCRIPT APLICA
    Toda consulta fica gravada com o SQL usado. Numero sem consulta gravada
    nao e auditavel, e a pergunta "de onde veio esse numero" fica sem resposta.

Nao precisa instalar nada. Usa o sqlite3 que ja vem com o Python.
=============================================================================
"""

import csv
import os
import re
import sqlite3
import sys
from datetime import date, datetime

BANCO = "projeto.db"
SEP = ";"
REGISTRO = os.path.join("entregas", "modulo7-consultas.csv")
RELATORIO = os.path.join("entregas", "modulo7-relatorio.md")
COLS_REGISTRO = ["pergunta", "arquivo_sql", "resultado", "linhas_antes_do_filtro",
                 "linhas_depois_do_filtro", "conferencia", "precisou_corrigir"]


def titulo(t):
    print()
    print("=" * 74)
    print(" " + t)
    print("=" * 74)


def numero(v):
    if v is None:
        return None
    t = str(v).strip().replace("R$", "").strip()
    if not t:
        return None
    if re.match(r"^-?\d{1,3}(\.\d{3})+,\d+$", t):
        t = t.replace(".", "").replace(",", ".")
    elif re.match(r"^-?\d+,\d+$", t):
        t = t.replace(",", ".")
    elif re.match(r"^-?\d{1,3}(,\d{3})+\.\d+$", t):
        t = t.replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None


def ler_csv(caminho):
    bruto = None
    for cod in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(caminho, encoding=cod) as f:
                bruto = f.read()
            break
        except (UnicodeDecodeError, LookupError):
            continue
    if bruto is None:
        return None, None
    primeira = bruto.splitlines()[0] if bruto.splitlines() else ""
    contagens = {d: primeira.count(d) for d in (";", ",", "\t", "|")}
    sep = max(contagens, key=contagens.get)
    if contagens[sep] == 0:
        return None, None
    return list(csv.DictReader(bruto.splitlines(), delimiter=sep)), sep


def nome_tabela(caminho):
    base = os.path.splitext(os.path.basename(caminho))[0]
    base = re.sub(r"[^0-9a-zA-Z_]", "_", base).strip("_").lower()
    if not base or base[0].isdigit():
        base = "t_" + base
    return base


def nome_coluna(c):
    c = re.sub(r"[^0-9a-zA-Z_]", "_", (c or "").strip()).strip("_").lower()
    return c or "coluna"


def tipo_coluna(valores):
    preenchidos = [v for v in valores if (v or "").strip()]
    if not preenchidos:
        return "TEXT"
    nums = [numero(v) for v in preenchidos]
    nums = [x for x in nums if x is not None]
    if len(nums) < 0.9 * len(preenchidos):
        return "TEXT"
    if all(abs(x - round(x)) < 1e-9 for x in nums):
        return "INTEGER"
    return "REAL"


def criar_banco(arquivos):
    titulo("MODULO 7 - CICLO 7.1 - CRIACAO DO BANCO")
    if not arquivos:
        print()
        print("Faltou o arquivo. Uso: banco dados/A.csv dados/B.csv")
        return 1

    con = sqlite3.connect(BANCO)
    cur = con.cursor()
    resumo = []

    for caminho in arquivos:
        if not os.path.exists(caminho):
            print("  [XX] nao encontrei " + caminho)
            continue
        linhas, sep = ler_csv(caminho)
        if linhas is None:
            print("  [XX] nao consegui ler " + caminho + " (separador ou codificacao)")
            continue
        if not linhas:
            print("  [XX] " + caminho + " tem cabecalho e nenhuma linha")
            continue

        tabela = nome_tabela(caminho)
        originais = list(linhas[0].keys())
        colunas = [nome_coluna(c) for c in originais]
        tipos = [tipo_coluna([l.get(o) for l in linhas]) for o in originais]

        cur.execute("DROP TABLE IF EXISTS %s" % tabela)
        cur.execute("CREATE TABLE %s (%s)" %
                    (tabela, ", ".join("%s %s" % (c, t) for c, t in zip(colunas, tipos))))

        rejeitadas = 0
        for l in linhas:
            valores = []
            for o, t in zip(originais, tipos):
                v = (l.get(o) or "").strip()
                if v == "":
                    valores.append(None)
                elif t in ("INTEGER", "REAL"):
                    x = numero(v)
                    valores.append(int(x) if (x is not None and t == "INTEGER") else x)
                else:
                    valores.append(v)
            try:
                cur.execute("INSERT INTO %s VALUES (%s)" %
                            (tabela, ",".join("?" * len(valores))), valores)
            except sqlite3.Error:
                rejeitadas += 1
        con.commit()
        cur.execute("SELECT COUNT(*) FROM %s" % tabela)
        gravadas = cur.fetchone()[0]
        resumo.append((tabela, caminho, len(linhas), gravadas, rejeitadas,
                       list(zip(colunas, tipos))))

    con.close()

    if not resumo:
        print()
        print("Nenhuma tabela foi criada.")
        return 1

    print()
    for tabela, caminho, no_csv, gravadas, rejeitadas, cols in resumo:
        print("TABELA %s  (de %s)" % (tabela, caminho))
        print("  linhas no CSV: %d | gravadas: %d | rejeitadas: %d"
              % (no_csv, gravadas, rejeitadas))
        print("  colunas: " + ", ".join("%s %s" % (c, t) for c, t in cols))
        if no_csv != gravadas:
            print("  ATENCAO: a contagem nao bate. Descubra por que antes de consultar.")
        print()

    print("Banco criado em: " + BANCO)
    print()
    print("PROXIMO PASSO")
    print("  Confira as contagens contra o perfil do encontro 7.")
    print("  Coluna de valor que ficou TEXT e virgula decimal: corrija o CSV e refaca.")
    return 0


def esquema():
    titulo("MODULO 7 - ESQUEMA DO BANCO")
    if not os.path.exists(BANCO):
        print()
        print("Nao encontrei " + BANCO + ". Execute primeiro o comando 'banco'.")
        return 1
    con = sqlite3.connect(BANCO)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tabelas = [r[0] for r in cur.fetchall()]
    print()
    for t in tabelas:
        cur.execute("SELECT COUNT(*) FROM %s" % t)
        total = cur.fetchone()[0]
        print("TABELA %s (%d linhas)" % (t, total))
        for r in cur.execute("PRAGMA table_info(%s)" % t):
            print("  %-28s %s" % (r[1], r[2]))
        print()
    con.close()
    print("Mostre este esquema ao agente antes de pedir uma consulta.")
    return 0


def proximo_numero():
    os.makedirs("saidas", exist_ok=True)
    existentes = [f for f in os.listdir("saidas") if re.match(r"^consulta-\d+\.sql$", f)]
    return len(existentes) + 1


def executar(consulta):
    titulo("MODULO 7 - CICLO 7.3 - EXECUCAO DE CONSULTA")
    if not os.path.exists(BANCO):
        print()
        print("Nao encontrei " + BANCO + ". Execute primeiro o comando 'banco'.")
        return 1
    if not consulta.strip():
        print()
        print("Faltou a consulta. Uso: sql SELECT ... FROM ...")
        return 1

    proibidos = ("drop ", "delete ", "update ", "insert ", "alter ")
    if any(p in consulta.lower() for p in proibidos):
        print()
        print("Este comando so executa consultas de leitura (SELECT).")
        print("Para recriar tabelas, use o comando 'banco'.")
        return 1

    con = sqlite3.connect(BANCO)
    cur = con.cursor()
    try:
        cur.execute(consulta)
        colunas = [d[0] for d in cur.description] if cur.description else []
        linhas = cur.fetchall()
    except sqlite3.Error as e:
        print()
        print("A consulta nao rodou: %s" % e)
        print()
        print("Cole esta mensagem de volta para o agente. O erro mais comum e nome de")
        print("coluna: confira no esquema.")
        con.close()
        return 1
    con.close()

    print()
    print("CONSULTA EXECUTADA")
    print(consulta.strip())
    print()
    print("Linhas no resultado: %d" % len(linhas))
    print()
    if colunas:
        print(" | ".join(str(c)[:18] for c in colunas))
        print("-" * 70)
        for l in linhas[:12]:
            print(" | ".join(str(v)[:18] for v in l))
        if len(linhas) > 12:
            print("... e mais %d linha(s)" % (len(linhas) - 12))

    i = proximo_numero()
    sql_path = os.path.join("saidas", "consulta-%d.sql" % i)
    csv_path = os.path.join("saidas", "consulta-%d.csv" % i)
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- Consulta %d, gravada em %s\n" % (i, datetime.now().strftime("%d/%m/%Y %H:%M")))
        f.write(consulta.strip() + "\n")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=SEP)
        w.writerow(colunas)
        w.writerows(linhas)

    print()
    print("GRAVADO:")
    print("  + " + sql_path)
    print("  + " + csv_path)
    print()
    print("O arquivo .sql e a resposta auditavel a 'como esse numero foi calculado'.")
    return 0


def juntar(args):
    titulo("MODULO 7 - CICLO 7.4 - JUNCAO VALIDADA PELA CONTAGEM")
    if len(args) < 3:
        print()
        print("Uso: juntar TABELA_A TABELA_B CHAVE")
        print("A chave precisa existir com o mesmo nome nas duas tabelas.")
        return 1
    if not os.path.exists(BANCO):
        print()
        print("Nao encontrei " + BANCO + ". Execute primeiro o comando 'banco'.")
        return 1

    a, b, chave = args[0], args[1], args[2]
    con = sqlite3.connect(BANCO)
    cur = con.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM %s" % a)
        n_a = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM %s" % b)
        n_b = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM %s AS x JOIN %s AS y ON x.%s = y.%s"
                    % (a, b, chave, chave))
        n_join = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM %s WHERE %s NOT IN (SELECT %s FROM %s)"
                    % (a, chave, chave, b))
        sem_par_a = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM %s WHERE %s NOT IN (SELECT %s FROM %s)"
                    % (b, chave, chave, a))
        sem_par_b = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM (SELECT %s FROM %s GROUP BY %s HAVING COUNT(*) > 1)"
                    % (chave, b, chave))
        repetidas_b = cur.fetchone()[0]
    except sqlite3.Error as e:
        print()
        print("Nao consegui juntar: %s" % e)
        print("Confira os nomes das tabelas e da chave com o comando 'esquema'.")
        con.close()
        return 1

    print()
    print("  Linhas em %-22s %d" % (a, n_a))
    print("  Linhas em %-22s %d" % (b, n_b))
    print("  Linhas depois da juncao       %d" % n_join)
    print("  Sem par em %-21s %d" % (a, sem_par_a))
    print("  Sem par em %-21s %d" % (b, sem_par_b))
    print("  Chaves repetidas em %-12s %d" % (b, repetidas_b))
    print()

    if n_join > n_a:
        print("  ATENCAO: a juncao AUMENTOU a contagem.")
        print("  A chave se repete em %s (%d valor(es) repetido(s))." % (b, repetidas_b))
        print("  Some linhas foram multiplicadas e qualquer soma sobre o resultado esta inflada.")
        print("  Investigue antes de seguir. Nao entregue assim.")
    elif n_join < n_a:
        print("  A juncao DIMINUIU a contagem: %d linha(s) de %s nao encontraram par."
              % (sem_par_a, a))
        print("  Isso pode estar certo, mas precisa ser declarado na entrega.")
    else:
        print("  A contagem permaneceu igual. E o resultado esperado de uma juncao por")
        print("  chave unica.")

    tabela = "%s_%s" % (a[:12], b[:12])
    cur.execute("DROP TABLE IF EXISTS %s" % tabela)
    cur.execute("CREATE TABLE %s AS SELECT x.*, y.* FROM %s AS x JOIN %s AS y ON x.%s = y.%s"
                % (tabela, a, b, chave, chave))
    con.commit()
    con.close()
    print()
    print("Tabela juntada criada: " + tabela)
    print("Registre as cinco contagens acima na entrega do ciclo 7.4.")
    return 0


def registrar():
    titulo("MODULO 7 - CICLO 7.3 - FORMULARIO DE CONSULTAS")
    os.makedirs("entregas", exist_ok=True)
    if os.path.exists(REGISTRO):
        print()
        print("O arquivo ja existe: " + REGISTRO)
        return 0
    with open(REGISTRO, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=SEP)
        w.writerow(COLS_REGISTRO)
        for _ in range(5):
            w.writerow([""] * len(COLS_REGISTRO))
    print()
    print("Formulario criado em: " + REGISTRO)
    print()
    print("COMO PREENCHER, uma linha por consulta")
    print()
    print("  pergunta                    A pergunta de negocio, em uma frase.")
    print("  arquivo_sql                 O nome do arquivo gravado, ex.: consulta-1.sql")
    print("  resultado                   O numero ou a conclusao em uma linha.")
    print("  linhas_antes_do_filtro      Quantas linhas a tabela tinha.")
    print("  linhas_depois_do_filtro     Quantas sobraram depois do WHERE.")
    print("  conferencia                 Como voce conferiu que o numero esta certo.")
    print("  precisou_corrigir           O que precisou ser corrigido na consulta,")
    print("                              ou 'nada'.")
    return 0


def conferir():
    titulo("MODULO 7 - CONFERENCIA DAS ENTREGAS")
    erros, avisos, consultas = [], [], []

    if not os.path.exists(REGISTRO):
        print()
        print("Nao encontrei " + REGISTRO + ". Execute o comando 'registrar'.")
        return 1

    with open(REGISTRO, newline="", encoding="utf-8-sig") as f:
        for i, l in enumerate(csv.DictReader(f, delimiter=SEP), start=2):
            if not (l.get("pergunta") or "").strip():
                continue
            pergunta = (l.get("pergunta") or "").strip()
            arquivo = (l.get("arquivo_sql") or "").strip()
            resultado = (l.get("resultado") or "").strip()
            conferencia = (l.get("conferencia") or "").strip()
            corrigir = (l.get("precisou_corrigir") or "").strip()

            if len(pergunta) < 15:
                erros.append("linha %d: pergunta vazia ou curta demais" % i)
            caminho = os.path.join("saidas", arquivo) if arquivo else ""
            if not arquivo:
                erros.append("linha %d: arquivo_sql esta vazio" % i)
            elif not os.path.exists(caminho):
                erros.append("linha %d: nao encontrei saidas/%s" % (i, arquivo))
            if len(resultado) < 5:
                erros.append("linha %d: resultado esta vazio" % i)
            if len(conferencia) < 15:
                erros.append("linha %d: conferencia vazia ou curta demais. Diga como "
                             "voce checou o numero." % i)
            if not corrigir:
                erros.append("linha %d: precisou_corrigir esta vazio. Se nada precisou, "
                             "escreva 'nada'." % i)

            try:
                antes = int((l.get("linhas_antes_do_filtro") or "").strip())
                depois = int((l.get("linhas_depois_do_filtro") or "").strip())
                if depois > antes:
                    erros.append("linha %d: o filtro nao pode aumentar a contagem. "
                                 "Se aumentou, houve juncao que multiplicou linhas." % i)
                if antes and depois / float(antes) < 0.2:
                    avisos.append("linha %d: o filtro descartou mais de 80%% das linhas. "
                                  "Confira se e mesmo o filtro que voce queria." % i)
            except ValueError:
                erros.append("linha %d: as contagens antes e depois do filtro precisam "
                             "ser numeros inteiros" % i)
                antes = depois = None

            consultas.append({"pergunta": pergunta, "arquivo": arquivo,
                              "resultado": resultado, "antes": antes, "depois": depois,
                              "conferencia": conferencia, "corrigir": corrigir})

    if len(consultas) < 5:
        erros.append("sao necessarias cinco consultas, e ha %d." % len(consultas))

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
    print("Consultas registradas: %d de 5" % len(consultas))

    if erros:
        print()
        print("O relatorio nao foi gerado. Corrija e execute 'conferir' de novo.")
        return 1

    L = ["# Relatorio do modulo 7", "",
         "Dados estruturados e consulta. DECC0294, UFMA, Curso de Administracao.",
         "Gerado em %s pelo script atividade_modulo7.py." % date.today().strftime("%d/%m/%Y"),
         "", "Nome e matricula: ______________________________", "",
         "## Consultas", ""]
    for i, c in enumerate(consultas, 1):
        L.append("### %d. %s" % (i, c["pergunta"]))
        L.append("")
        L.append("- Consulta gravada em: saidas/%s" % c["arquivo"])
        L.append("- Resultado: %s" % c["resultado"])
        L.append("- Linhas antes do filtro: %s" % c["antes"])
        L.append("- Linhas depois do filtro: %s" % c["depois"])
        L.append("- Como conferi: %s" % c["conferencia"])
        L.append("- Precisou corrigir: %s" % c["corrigir"])
        L.append("")
        caminho = os.path.join("saidas", c["arquivo"])
        if os.path.exists(caminho):
            L.append("```sql")
            L.append(open(caminho, encoding="utf-8").read().strip())
            L.append("```")
            L.append("")
    if avisos:
        L += ["## Pontos marcados pelo script", ""]
        L += ["- %s" % a for a in avisos]
        L.append("")
    L += ["## As cinco partes, identificadas", "",
          "ESCREVA AQUI, para duas das consultas acima, o que cada parte faz:",
          "o que quero ver, de onde, filtrado por que, agrupado como, ordenado como.",
          "", "> ", "",
          "---", "",
          "## Declaracao de uso de inteligencia artificial", "",
          "Ferramenta e modelo usados: ______________________________", "",
          "As consultas foram escritas com apoio do agente, lidas por mim antes da",
          "execucao, e conferidas conforme registrado acima.", ""]

    os.makedirs("entregas", exist_ok=True)
    with open(RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print()
    print("Relatorio gerado em: " + RELATORIO)
    return 0


def main():
    args = sys.argv[1:]
    cmd = (args[0].strip().lower() if args else "")
    if cmd == "banco":
        return criar_banco(args[1:])
    if cmd == "esquema":
        return esquema()
    if cmd == "sql":
        return executar(" ".join(args[1:]))
    if cmd == "juntar":
        return juntar(args[1:])
    if cmd == "registrar":
        return registrar()
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    print(__doc__)
    print("Comandos disponiveis:")
    print("  python atividade_modulo7.py banco dados/A.csv dados/B.csv")
    print("  python atividade_modulo7.py esquema")
    print("  python atividade_modulo7.py sql SELECT ...")
    print("  python atividade_modulo7.py juntar TABELA_A TABELA_B CHAVE")
    print("  python atividade_modulo7.py registrar")
    print("  python atividade_modulo7.py conferir")
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
