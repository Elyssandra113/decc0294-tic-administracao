#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 8 - Painel de indicadores
 DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
 UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que monta o painel do seu projeto em HTML, a partir de um
    formulario de indicadores e de uma serie exportada do banco. O painel e
    autocontido: abre em qualquer navegador, sem internet e sem instalar nada.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute atividade_modulo8.py com o comando iniciar"
       Cria entregas/modulo8-indicadores.csv com as colunas do painel.

    2) Preencha um indicador por linha. Todos os campos sao obrigatorios: e a
       comparacao e a fonte que transformam um numero solto em informacao.

    3) Exporte a serie do grafico com o script do modulo 7:
       "execute atividade_modulo7.py com o comando sql SELECT categoria, valor ..."
       O resultado sai em saidas/consulta-N.csv, com duas colunas.

    4) "execute atividade_modulo8.py com o comando painel saidas/consulta-N.csv"
       Gera entregas/painel.html

    5) "execute atividade_modulo8.py com o comando conferir"
       Valida o formulario e o painel.

    6) "execute atividade_modulo8.py com o comando b1"
       Percorre os encontros 7, 8 e 9 e diz o que falta para a entrega B1.

    Sem nenhum comando, o script imprime estas instrucoes.

A REGRA QUE O SCRIPT APLICA
    Indicador sem comparacao ao lado e sem fonte declarada e recusado. Numero
    solto nao informa, e numero sem origem nao e verificavel.

Nao precisa instalar nada. Roda com o Python que ja vem com o ambiente.
=============================================================================
"""

import csv
import html
import os
import re
import sys
from datetime import date, datetime

SEP = ";"
INDICADORES = os.path.join("entregas", "modulo8-indicadores.csv")
PAINEL = os.path.join("entregas", "painel.html")
RELATORIO = os.path.join("entregas", "B1-relatorio.md")

COLUNAS = ["indicador", "titulo_conclusao", "valor", "unidade", "periodo",
           "comparacao", "valor_comparacao", "fonte", "consulta"]

VINHO = "#8D0333"
DOURADO = "#D4B277"
TEAL = "#0AB0AB"
CINZA = "#BDBDBD"

EXEMPLO = [
    "Custo por atendimento",
    "O custo por atendimento na unidade Centro e 40% maior que a media das demais",
    "17,66",
    "R$ por atendimento",
    "jan a ago de 2026",
    "media das demais unidades",
    "12,58",
    "Tabela base do projeto.db, filtrada por custo maior que zero",
    "consulta-1.sql",
]


def titulo(t):
    print()
    print("=" * 74)
    print(" " + t)
    print("=" * 74)


def numero(v):
    if v is None:
        return None
    t = str(v).strip().replace("R$", "").replace("%", "").strip()
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
        return None
    primeira = bruto.splitlines()[0] if bruto.splitlines() else ""
    contagens = {d: primeira.count(d) for d in (";", ",", "\t", "|")}
    sep = max(contagens, key=contagens.get)
    if contagens[sep] == 0:
        return None
    return list(csv.DictReader(bruto.splitlines(), delimiter=sep))


def iniciar():
    titulo("MODULO 8 - CICLO 8.3 - FORMULARIO DO PAINEL")
    os.makedirs("entregas", exist_ok=True)
    if os.path.exists(INDICADORES):
        print()
        print("O arquivo ja existe: " + INDICADORES)
        return 0
    with open(INDICADORES, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=SEP)
        w.writerow(COLUNAS)
        w.writerow(EXEMPLO)
        for _ in range(3):
            w.writerow([""] * len(COLUNAS))
    print()
    print("Formulario criado em: " + INDICADORES)
    print()
    print("COMO PREENCHER, um indicador por linha")
    print()
    print("  indicador           Nome curto. Ex.: custo por atendimento")
    print()
    print("  titulo_conclusao    A frase que o leitor deve levar. Afirmativa, com o")
    print("                      numero dentro. Se voce nao consegue escrever, o")
    print("                      indicador ainda nao esta pronto.")
    print()
    print("  valor               O numero apurado.")
    print()
    print("  unidade             R$, %, dias, atendimentos.")
    print()
    print("  periodo             O intervalo coberto. Ex.: jan a ago de 2026")
    print()
    print("  comparacao          Contra o que se compara: meta, periodo anterior,")
    print("                      media das demais unidades. Obrigatorio.")
    print()
    print("  valor_comparacao    O numero da comparacao.")
    print()
    print("  fonte               De que tabela saiu e com que filtro.")
    print()
    print("  consulta            O arquivo .sql do encontro 8 que produziu o numero.")
    print()
    print("Sao necessarios tres indicadores. A primeira linha e exemplo: substitua.")
    return 0


def carregar():
    linhas = ler_csv(INDICADORES) if os.path.exists(INDICADORES) else None
    if linhas is None:
        return None, ["nao encontrei " + INDICADORES + ". Execute o comando 'iniciar'."]
    erros, indicadores = [], []
    for i, l in enumerate(linhas, start=2):
        nome = (l.get("indicador") or "").strip()
        if not nome:
            continue
        if nome == EXEMPLO[0] and (l.get("titulo_conclusao") or "").strip() == EXEMPLO[1]:
            erros.append("linha %d: a linha de exemplo continua no arquivo" % i)
            continue
        campos = {c: (l.get(c) or "").strip() for c in COLUNAS}
        if len(campos["titulo_conclusao"]) < 25:
            erros.append("linha %d: titulo_conclusao vazio ou curto demais. Escreva a "
                         "frase afirmativa que o leitor deve levar." % i)
        if numero(campos["valor"]) is None:
            erros.append("linha %d: valor precisa ser um numero" % i)
        for obrig in ("unidade", "periodo", "comparacao", "fonte"):
            if not campos[obrig]:
                erros.append("linha %d: %s esta vazio. Indicador sem %s nao entra no painel."
                             % (i, obrig, obrig))
        if numero(campos["valor_comparacao"]) is None:
            erros.append("linha %d: valor_comparacao precisa ser um numero" % i)
        indicadores.append(campos)
    if len(indicadores) < 3:
        erros.append("sao necessarios tres indicadores, e ha %d." % len(indicadores))
    return indicadores, erros


def variacao(campos):
    v = numero(campos["valor"])
    c = numero(campos["valor_comparacao"])
    if v is None or c is None or c == 0:
        return None
    return 100.0 * (v - c) / abs(c)


def barras_svg(serie, rotulo):
    if not serie:
        return ""
    maximo = max(v for _, v in serie) or 1
    alt_barra, espaco = 34, 14
    larg, marg_esq = 900, 250
    altura = len(serie) * (alt_barra + espaco) + 20
    partes = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">'
              % (larg, altura, html.escape(rotulo))]
    for i, (cat, val) in enumerate(serie):
        y = 10 + i * (alt_barra + espaco)
        comp = (larg - marg_esq - 120) * (val / maximo)
        cor = VINHO if i == 0 else CINZA
        partes.append('<text x="%d" y="%d" class="cat">%s</text>'
                      % (marg_esq - 12, y + 23, html.escape(str(cat)[:34])))
        partes.append('<rect x="%d" y="%d" width="%.1f" height="%d" fill="%s"></rect>'
                      % (marg_esq, y, max(comp, 1), alt_barra, cor))
        partes.append('<text x="%.1f" y="%d" class="val">%s</text>'
                      % (marg_esq + max(comp, 1) + 10, y + 23, fmt(val)))
    partes.append("</svg>")
    return "\n".join(partes)


def fmt(v):
    if v is None:
        return "-"
    if abs(v - round(v)) < 1e-9 and abs(v) < 1e15:
        return "{:,}".format(int(round(v))).replace(",", ".")
    return "{:,.2f}".format(v).replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def painel(args):
    titulo("MODULO 8 - CICLO 8.3 - GERACAO DO PAINEL")
    indicadores, erros = carregar()
    if erros:
        print()
        print("PROBLEMAS QUE PRECISAM SER CORRIGIDOS (%d):" % len(erros))
        for e in erros:
            print("  - " + e)
        print()
        print("O painel nao foi gerado.")
        return 1

    serie, rotulo = [], "Comparacao por categoria"
    if args:
        linhas = ler_csv(args[0])
        if linhas is None:
            print()
            print("Nao consegui ler a serie em " + args[0])
            return 1
        colunas = list(linhas[0].keys()) if linhas else []
        if len(colunas) < 2:
            print()
            print("A serie precisa de duas colunas: categoria e valor.")
            return 1
        for l in linhas:
            v = numero(l.get(colunas[1]))
            if v is not None:
                serie.append((l.get(colunas[0]), v))
        serie.sort(key=lambda x: -x[1])
        rotulo = "%s por %s" % (colunas[1], colunas[0])
        if len(args) > 1:
            rotulo = " ".join(args[1:])

    cartoes = []
    for c in indicadores:
        var = variacao(c)
        if var is None:
            sinal, cor = "", "#555"
        elif var > 0:
            sinal, cor = "+%.1f%%" % var, VINHO
        elif var < 0:
            sinal, cor = "%.1f%%" % var, TEAL
        else:
            sinal, cor = "estavel", "#555"
        cartoes.append("""
    <article class="cartao">
      <span class="rot">%s</span>
      <p class="numero">%s <span class="un">%s</span></p>
      <p class="comp">contra %s: <strong>%s</strong> <span style="color:%s">%s</span></p>
      <p class="conc">%s</p>
      <p class="periodo">%s</p>
    </article>""" % (
            html.escape(c["indicador"]), html.escape(c["valor"]), html.escape(c["unidade"]),
            html.escape(c["comparacao"]), html.escape(c["valor_comparacao"]), cor, sinal,
            html.escape(c["titulo_conclusao"]), html.escape(c["periodo"])))

    linhas_fonte = "\n".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (html.escape(c["indicador"]), html.escape(c["periodo"]),
           html.escape(c["fonte"]), html.escape(c["consulta"] or "-"))
        for c in indicadores)

    grafico = ""
    if serie:
        grafico = """
  <section class="bloco">
    <h2>%s</h2>
    <div class="grafico">%s</div>
    <p class="nota">A barra em destaque e a maior do conjunto. As demais aparecem em
    cinza porque servem de contexto, e nao de comparacao principal.</p>
  </section>""" % (html.escape(rotulo), barras_svg(serie, rotulo))

    doc = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Painel do projeto - DECC0294</title>
<style>
  :root{--vinho:%s;--dourado:%s;--teal:%s}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:"Segoe UI",Calibri,Arial,sans-serif;color:#333;background:#f2f2f2;padding:0 0 48px}
  header{background:var(--vinho);color:#fff;padding:26px 40px 22px}
  header h1{font-size:26px;font-weight:700}
  header p{margin-top:6px;font-size:15px;color:#f1d9e2}
  .filete{height:10px;background:var(--dourado)}
  main{max-width:1060px;margin:26px auto;padding:0 20px}
  .cartoes{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
  .cartao{background:#fff;border:1px solid #e0e0e0;border-top:5px solid var(--vinho);padding:18px 20px}
  .cartao .rot{font-size:13px;font-weight:700;letter-spacing:1px;color:var(--vinho);text-transform:uppercase}
  .cartao .numero{font-size:38px;font-weight:700;color:#1a1a1a;margin-top:6px;line-height:1.1}
  .cartao .un{font-size:15px;font-weight:400;color:#666}
  .cartao .comp{font-size:14px;margin-top:8px;color:#555}
  .cartao .conc{font-size:15px;margin-top:12px;line-height:1.4;color:#1a1a1a}
  .cartao .periodo{font-size:13px;margin-top:10px;color:#777}
  .bloco{background:#fff;border:1px solid #e0e0e0;padding:22px 24px;margin-top:22px}
  .bloco h2{font-size:19px;color:var(--vinho);margin-bottom:16px}
  .grafico svg{width:100%%;height:auto}
  .grafico .cat{font-size:15px;fill:#333;text-anchor:end}
  .grafico .val{font-size:15px;fill:#1a1a1a;font-weight:700}
  .nota{font-size:13px;color:#777;margin-top:12px}
  table{width:100%%;border-collapse:collapse;font-size:14px}
  th{background:var(--vinho);color:#fff;text-align:left;padding:9px 10px;font-weight:700}
  td{padding:8px 10px;border-bottom:1px solid #eee;vertical-align:top}
  tr:nth-child(even) td{background:#fafafa}
  footer{max-width:1060px;margin:22px auto 0;padding:0 20px;font-size:13px;color:#777}
  .destinatario{background:#faf7f8;border:1px solid var(--dourado);padding:14px 18px;margin-top:22px;font-size:14px}
</style>
</head>
<body>
<div class="filete"></div>
<header>
  <h1>Painel do projeto</h1>
  <p>DECC0294 &middot; Tecnologia da Informacao e Comunicacao Aplicada a Administracao &middot; UFMA</p>
  <p>Atualizado em %s</p>
</header>
<main>
  <div class="cartoes">%s
  </div>%s
  <section class="bloco">
    <h2>De onde vem cada numero</h2>
    <table>
      <thead><tr><th>Indicador</th><th>Periodo</th><th>Fonte e filtro</th><th>Consulta</th></tr></thead>
      <tbody>
%s
      </tbody>
    </table>
  </section>
  <div class="destinatario">
    <strong>Destinatario deste painel:</strong> ____________________________<br>
    <strong>Decisao que ele sustenta:</strong> ____________________________
  </div>
</main>
<footer>
  Gerado em %s pelo script atividade_modulo8.py. Os numeros vieram das consultas
  registradas no encontro 8 e podem ser refeitos a partir dos arquivos .sql citados.
</footer>
</body>
</html>
""" % (VINHO, DOURADO, TEAL,
       datetime.now().strftime("%d/%m/%Y as %H:%M"),
       "".join(cartoes), grafico, linhas_fonte,
       datetime.now().strftime("%d/%m/%Y"))

    os.makedirs("entregas", exist_ok=True)
    with open(PAINEL, "w", encoding="utf-8") as f:
        f.write(doc)

    print()
    print("Indicadores no painel: %d" % len(indicadores))
    print("Categorias no grafico: %d" % len(serie))
    print()
    print("Painel gerado em: " + PAINEL)
    print()
    print("PROXIMOS PASSOS")
    print("  Abra o arquivo no navegador e confira: os numeros batem com as consultas?")
    print("  Preencha o destinatario e a decisao ao pe do painel.")
    print("  Depois: 'execute atividade_modulo8.py com o comando conferir'")
    return 0


def conferir():
    titulo("MODULO 8 - CONFERENCIA DO PAINEL")
    indicadores, erros = carregar()
    avisos = []

    if not os.path.exists(PAINEL):
        erros.append("nao encontrei " + PAINEL + ". Execute o comando 'painel'.")
    else:
        conteudo = open(PAINEL, encoding="utf-8").read()
        if "____________________________" in conteudo:
            avisos.append("o destinatario e a decisao ainda nao foram preenchidos no painel")

    if indicadores:
        for c in indicadores:
            if not c["consulta"]:
                avisos.append("o indicador '%s' nao aponta o arquivo de consulta que o "
                              "produziu" % c["indicador"])
            elif not os.path.exists(os.path.join("saidas", c["consulta"])):
                avisos.append("nao encontrei saidas/%s, citado pelo indicador '%s'"
                              % (c["consulta"], c["indicador"]))

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
    print("Indicadores validos: %d" % (len(indicadores) if indicadores else 0))
    if erros:
        return 1
    print()
    print("PROXIMO PASSO")
    print('  "execute atividade_modulo8.py com o comando b1"')
    return 0


ITENS_B1 = [
    ("Perguntas formuladas (encontro 7)",
     [os.path.join("entregas", "modulo6-ciclo1-perguntas.md")]),
    ("Perfil da base (encontro 7)",
     [os.path.join("entregas", "modulo6-ciclo2-perfil.md")]),
    ("Tratamento de ausentes e atipicos (encontro 7)",
     [os.path.join("entregas", "modulo6-tratamento.csv")]),
    ("Log de verificacao (encontro 7)",
     [os.path.join("entregas", "modulo6-log-verificacao.csv")]),
    ("Banco povoado (encontro 8)", ["projeto.db"]),
    ("Modelo das tabelas (encontro 8)",
     [os.path.join("entregas", "modulo7-ciclo2-modelo.md")]),
    ("Cinco consultas registradas (encontro 8)",
     [os.path.join("entregas", "modulo7-consultas.csv")]),
    ("Juncao validada (encontro 8)",
     [os.path.join("entregas", "modulo7-ciclo4-juncao.md")]),
    ("Reconstrucao de grafico (encontro 9)",
     [os.path.join("entregas", "modulo8-ciclo1-reconstrucao.md")]),
    ("Escolha de formas (encontro 9)",
     [os.path.join("entregas", "modulo8-ciclo2-formas.md")]),
    ("Painel (encontro 9)", [PAINEL]),
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


def conferir_b1():
    titulo("MODULO 8 - CONFERENCIA DA ENTREGA B1")
    itens = []
    for rotulo, caminhos in ITENS_B1:
        achado = next((c for c in caminhos if os.path.exists(c)), None)
        if achado:
            tamanho = os.path.getsize(achado)
            ok = tamanho > 200
            det = ("Encontrado: %s (%d bytes)." % (achado, tamanho)) if ok else \
                  ("%s existe mas esta quase vazio." % achado)
        else:
            ok, det = False, "Nao encontrei " + " nem ".join(caminhos)
        itens.append((ok, rotulo, det))

    g = info_git()
    itens.append((bool(g["remoto"]), "Repositorio publicado",
                  ("Publicado em: " + g["remoto"]) if g["remoto"]
                  else "Publique o repositorio antes de entregar."))

    print()
    for ok, rotulo, det in itens:
        print(("  [OK]    " if ok else "  [FALTA] ") + rotulo)
        print("           " + det)
    ok_n = sum(1 for i in itens if i[0])
    print()
    print("Concluidos: %d de %d." % (ok_n, len(itens)))

    L = ["# Relatorio da entrega B1", "",
         "Modulo 8, encontro 9. DECC0294, UFMA, Curso de Administracao.",
         "Gerado em %s pelo script atividade_modulo8.py."
         % datetime.now().strftime("%d/%m/%Y as %H:%M"), "",
         "Situacao: %d de %d itens concluidos." % (ok_n, len(itens)), "",
         "| Item | Situacao | Observacao |", "|---|---|---|"]
    for ok, rotulo, det in itens:
        L.append("| %s | %s | %s |" % (rotulo, "concluido" if ok else "pendente", det))
    L += ["", "## Conferido por mim", "",
          "Nome e matricula: ______________________________", "",
          "Declaro que os numeros do painel foram conferidos contra as consultas",
          "registradas, que cada indicador declara a sua fonte, e que o painel nao",
          "contem dado pessoal identificavel de terceiro.", ""]
    os.makedirs("entregas", exist_ok=True)
    with open(RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print()
    print("Relatorio gravado em: " + RELATORIO)
    if ok_n < len(itens):
        print()
        print("Resolva os itens pendentes e execute 'b1' de novo antes de publicar.")
        return 1
    print()
    print("Entrega B1 completa. Grave com a mensagem 'entrega B1' e publique.")
    return 0


def main():
    args = sys.argv[1:]
    cmd = (args[0].strip().lower() if args else "")
    if cmd in ("iniciar", "criar", "start"):
        return iniciar()
    if cmd in ("painel", "gerar"):
        return painel(args[1:])
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    if cmd in ("b1", "entrega", "bloco"):
        return conferir_b1()
    print(__doc__)
    print("Comandos disponiveis:")
    print("  python atividade_modulo8.py iniciar                     cria o formulario")
    print("  python atividade_modulo8.py painel saidas/serie.csv     gera o painel")
    print("  python atividade_modulo8.py conferir                    valida o painel")
    print("  python atividade_modulo8.py b1                          confere a entrega B1")
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
