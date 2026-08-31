#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 4 - Bateria de testes do AGENTS.md
 DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
 UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que conduz a atividade do ciclo 4.2. Ele guarda a versao
    atual do seu AGENTS.md, prepara tres tarefas de teste e depois confere se
    voce testou, corrigiu e testou de novo.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute o arquivo atividade_modulo4.py com o comando iniciar"
       Guarda uma copia do AGENTS.md em saidas/agents-v1.md, escreve as tres
       tarefas de teste em saidas/modulo4-bateria-de-testes.md e cria o
       registro em entregas/modulo4-registro.csv

    2) Rode as tres tarefas (rodada 1). Anote no registro o que saiu fora do
       que voce configurou. Corrija o AGENTS.md. Rode as tres de novo
       (rodada 2) e anote.

    3) "execute o arquivo atividade_modulo4.py com o comando conferir"
       Valida o registro, compara o AGENTS.md com a copia da versao 1 e gera
       entregas/modulo4-relatorio.md

    Para o ciclo 4.3, o mesmo script consulta APIs publicas brasileiras:

    4) "execute atividade_modulo4.py com o comando apis"
       Lista as fontes disponiveis e a URL de cada uma.

    5) "execute atividade_modulo4.py com o comando apis testar"
       Testa todas as fontes e diz quais o laboratorio alcanca. Grava o
       diagnostico em dados/api-diagnostico.md

    6) "execute atividade_modulo4.py com o comando apis municipios MA"
       (ou qualquer outra fonte da lista) consulta, mostra a URL chamada e
       grava o resultado em dados/

    Sem nenhum comando, o script imprime estas instrucoes.

A REGRA QUE O SCRIPT APLICA
    Duas rodadas das mesmas tres tarefas, e o AGENTS.md precisa ter mudado
    entre elas. Escrever a regra e nao testar e o erro mais comum.

Nao precisa instalar nada. Roda com o Python que ja vem com o ambiente.
=============================================================================
"""

import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime

CSV = os.path.join("entregas", "modulo4-registro.csv")
MD = os.path.join("entregas", "modulo4-relatorio.md")
COPIA = os.path.join("saidas", "agents-v1.md")
BATERIA = os.path.join("saidas", "modulo4-bateria-de-testes.md")
AGENTS = "AGENTS.md"
GLOSSARIO = os.path.join("entregas", "glossario.html")
SEP = ";"

COLUNAS = ["rodada", "tarefa", "saiu_como_configurado_1a5", "o_que_saiu_fora", "ajuste_feito"]

TAREFAS = [
    "conceito",
    "analise",
    "redacao",
]

TEXTO_BATERIA = """# Bateria de testes do AGENTS.md

Modulo 4, ciclo 4.2. Rode estas tres tarefas duas vezes: antes e depois de
corrigir o AGENTS.md. Use exatamente o mesmo texto nas duas rodadas, para que
a comparacao signifique alguma coisa.

## Tarefa 1 — conceito

    Explique o que e [um conceito central da sua area] para alguem que vai
    usar isso numa decisao de gestao. Grave em saidas/teste-conceito-r1.md
    (na rodada 2, use -r2).

O que observar: o nivel da explicacao, o vocabulario, se ha exemplo, se ha
referencia, e se o formato saiu como voce configurou.

## Tarefa 2 — analise com numero

    Com base no arquivo [uma planilha ou tabela da pasta dados], calcule
    [uma medida simples] e interprete o resultado em ate cinco linhas.
    Grave em saidas/teste-analise-r1.md (na rodada 2, use -r2).

O que observar: se ele mostrou a conta, se declarou a limitacao do dado e se
inventou algum numero que nao estava no arquivo.

## Tarefa 3 — redacao

    Escreva um paragrafo de abertura para um relatorio sobre [tema do seu
    projeto], dirigido a [quem vai ler]. Grave em saidas/teste-redacao-r1.md
    (na rodada 2, use -r2).

O que observar: o tom, a pessoa verbal, o tamanho e se ele escreveu o texto
final no seu lugar quando a sua regra dizia para produzir apenas rascunho.

## Como preencher o registro

Uma linha por tarefa por rodada, seis linhas no total, em
entregas/modulo4-registro.csv

- rodada: 1 ou 2
- tarefa: conceito, analise ou redacao
- saiu_como_configurado_1a5: 1 = nada saiu como configurado, 5 = tudo saiu
- o_que_saiu_fora: o que divergiu do que voce escreveu no AGENTS.md
- ajuste_feito: o que voce mudou no AGENTS.md por causa disso (na rodada 2,
  pode ser "nenhum" se nada mais precisou mudar)
"""


def titulo(t):
    print()
    print("=" * 74)
    print(" " + t)
    print("=" * 74)


def iniciar():
    titulo("MODULO 4 - CICLO 4.2 - PREPARACAO DA BATERIA DE TESTES")

    if not os.path.exists(AGENTS):
        print()
        print("Nao encontrei o arquivo AGENTS.md nesta pasta.")
        print("Ele foi criado no encontro 3, pelo script atividade_modulo2.py.")
        print("Confirme que voce abriu a pasta certa do projeto.")
        return 1

    os.makedirs("saidas", exist_ok=True)
    os.makedirs("entregas", exist_ok=True)
    criados = []

    if os.path.exists(COPIA):
        print()
        print("A copia da versao 1 ja existe em " + COPIA)
        print("Ela nao foi sobrescrita: e ela que permite comparar o antes e o depois.")
    else:
        with open(AGENTS, encoding="utf-8", errors="replace") as f:
            atual = f.read()
        with open(COPIA, "w", encoding="utf-8") as f:
            f.write(atual)
        criados.append(COPIA)

    if not os.path.exists(BATERIA):
        with open(BATERIA, "w", encoding="utf-8") as f:
            f.write(TEXTO_BATERIA)
        criados.append(BATERIA)

    if not os.path.exists(CSV):
        with open(CSV, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=SEP)
            w.writerow(COLUNAS)
            for r in (1, 2):
                for t in TAREFAS:
                    w.writerow([r, t, "", "", ""])
        criados.append(CSV)

    print()
    if criados:
        print("CRIADO:")
        for c in criados:
            print("  + " + c)
    print()
    print("PROXIMOS PASSOS, NESTA ORDEM")
    print()
    print("  1. Abra " + BATERIA + " e adapte as tres tarefas ao seu projeto.")
    print()
    print("  2. Rode as tres tarefas (rodada 1) e preencha as tres primeiras")
    print("     linhas de " + CSV)
    print()
    print("  3. Corrija o AGENTS.md com base no que saiu fora.")
    print()
    print("  4. Rode as mesmas tres tarefas (rodada 2) e preencha as tres")
    print("     ultimas linhas.")
    print()
    print("  5. Peca ao agente:")
    print('     "execute atividade_modulo4.py com o comando conferir"')
    return 0


def secoes(texto):
    partes = re.split(r"^##\s+\d\.\s*(.+)$", texto, flags=re.MULTILINE)
    out = {}
    for i in range(1, len(partes), 2):
        corpo = re.sub(r"\([^)]*\)", "", partes[i + 1], flags=re.DOTALL)
        out[partes[i].strip()] = corpo.replace("PREENCHER", "").strip()
    return out


def conferir():
    titulo("MODULO 4 - CICLO 4.2 - CONFERENCIA")
    itens = []

    # registro
    if not os.path.exists(CSV):
        print()
        print("Nao encontrei " + CSV + ". Execute primeiro o comando 'iniciar'.")
        return 1

    with open(CSV, newline="", encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f, delimiter=SEP))

    erros = []
    registros = []
    for i, l in enumerate(linhas, start=2):
        rodada = (l.get("rodada") or "").strip()
        tarefa = (l.get("tarefa") or "").strip().lower()
        nota = (l.get("saiu_como_configurado_1a5") or "").strip()
        fora = (l.get("o_que_saiu_fora") or "").strip()
        ajuste = (l.get("ajuste_feito") or "").strip()

        if rodada not in ("1", "2"):
            erros.append("linha %d: rodada deveria ser 1 ou 2" % i)
            continue
        if tarefa not in TAREFAS:
            erros.append("linha %d: tarefa deveria ser conceito, analise ou redacao" % i)
            continue
        if not nota.isdigit() or not (1 <= int(nota) <= 5):
            erros.append("linha %d: saiu_como_configurado_1a5 deveria ser um inteiro de 1 a 5" % i)
            continue
        if len(fora) < 12 and int(nota) < 5:
            erros.append("linha %d: nota abaixo de 5 exige dizer o que saiu fora" % i)
        if rodada == "1" and len(ajuste) < 5:
            erros.append("linha %d: na rodada 1, diga o ajuste feito (ou escreva 'nenhum')" % i)

        registros.append({"rodada": int(rodada), "tarefa": tarefa, "nota": int(nota),
                          "fora": fora, "ajuste": ajuste})

    r1 = [r for r in registros if r["rodada"] == 1]
    r2 = [r for r in registros if r["rodada"] == 2]
    completo = len(r1) == 3 and len(r2) == 3
    itens.append((completo, "Duas rodadas das tres tarefas",
                  "Rodada 1: %d de 3. Rodada 2: %d de 3." % (len(r1), len(r2))))

    # AGENTS.md mudou?
    mudou = False
    detalhe = "Nao encontrei a copia da versao 1. Execute o comando 'iniciar'."
    if os.path.exists(COPIA) and os.path.exists(AGENTS):
        v1 = open(COPIA, encoding="utf-8", errors="replace").read().strip()
        v2 = open(AGENTS, encoding="utf-8", errors="replace").read().strip()
        mudou = v1 != v2
        if mudou:
            d = len(v2.split()) - len(v1.split())
            detalhe = ("O arquivo mudou entre as duas rodadas (%s%d palavras)."
                       % ("+" if d >= 0 else "", d))
        else:
            detalhe = ("O AGENTS.md esta identico a versao 1. Se as tres tarefas sairam "
                       "perfeitas na rodada 1, escreva isso no relatorio. Caso contrario, "
                       "corrija o arquivo antes de entregar.")
    itens.append((mudou, "AGENTS.md revisado", detalhe))

    # seções preenchidas
    if os.path.exists(AGENTS):
        secs = secoes(open(AGENTS, encoding="utf-8", errors="replace").read())
        vazias = [k for k, v in secs.items() if len(v) < 25]
        ok = len(secs) >= 4 and not vazias
        itens.append((ok, "As quatro secoes continuam preenchidas",
                      "Tudo preenchido." if ok else "Secoes vazias ou curtas: " + "; ".join(vazias)))

    # melhora entre rodadas
    if completo:
        m1 = sum(r["nota"] for r in r1) / 3.0
        m2 = sum(r["nota"] for r in r2) / 3.0
        itens.append((m2 >= m1, "A segunda rodada nao piorou",
                      "Media da rodada 1: %.1f. Media da rodada 2: %.1f." % (m1, m2)))

    # glossário do ciclo 4.1
    itens.append((os.path.exists(GLOSSARIO), "Glossario do ciclo 4.1 entregue",
                  "Encontrado." if os.path.exists(GLOSSARIO)
                  else "Grave o glossario em " + GLOSSARIO))

    print()
    if erros:
        print("PROBLEMAS NO REGISTRO (%d):" % len(erros))
        for e in erros:
            print("  - " + e)
        print()

    for ok, tit, det in itens:
        print(("  [OK]    " if ok else "  [FALTA] ") + tit)
        print("           " + det)

    ok_n = sum(1 for i in itens if i[0])
    print()
    print("Concluidos: %d de %d." % (ok_n, len(itens)))

    if erros:
        print()
        print("O relatorio nao foi gerado. Corrija o registro e execute 'conferir' de novo.")
        return 1

    gerar(itens, registros, ok_n)
    print()
    print("Relatorio gerado em: " + MD)
    print()
    print("ULTIMO PASSO")
    print("  Abra o relatorio e escreva a lista do que mudou entre a versao 1 e a")
    print("  versao 2 do AGENTS.md, e ao menos uma regra que voce escreveu e depois")
    print("  removeu, com a razao.")
    return 0 if ok_n == len(itens) else 1


def gerar(itens, registros, ok_n):
    L = []
    L.append("# Relatorio do modulo 4")
    L.append("")
    L.append("Ciclo 4.2, bateria de testes do AGENTS.md. DECC0294, UFMA.")
    L.append("Gerado em %s pelo script atividade_modulo4.py."
             % date.today().strftime("%d/%m/%Y"))
    L.append("")
    L.append("Nome e matricula: ______________________________")
    L.append("")
    L.append("Situacao: %d de %d itens concluidos." % (ok_n, len(itens)))
    L.append("")
    L.append("| Item | Situacao | Observacao |")
    L.append("|---|---|---|")
    for ok, tit, det in itens:
        L.append("| %s | %s | %s |" % (tit, "concluido" if ok else "pendente", det))
    L.append("")
    L.append("## Registro das rodadas")
    L.append("")
    L.append("| Rodada | Tarefa | Saiu como configurado | O que saiu fora | Ajuste feito |")
    L.append("|---|---|---|---|---|")
    for r in sorted(registros, key=lambda r: (r["rodada"], r["tarefa"])):
        L.append("| %d | %s | %d de 5 | %s | %s |"
                 % (r["rodada"], r["tarefa"], r["nota"], r["fora"] or "—", r["ajuste"] or "—"))
    L.append("")
    L.append("## O que mudou entre a versao 1 e a versao 2")
    L.append("")
    L.append("ESCREVA AQUI, uma linha por mudanca, dizendo o que motivou cada uma:")
    L.append("")
    L.append("- ")
    L.append("")
    L.append("## Regra que eu escrevi e depois removi")
    L.append("")
    L.append("ESCREVA AQUI a regra e a razao de ter saido. Regra removida vale tanto")
    L.append("quanto regra acrescentada.")
    L.append("")
    L.append("> ")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Declaracao de uso de inteligencia artificial")
    L.append("")
    L.append("Ferramenta e modelo usados: ______________________________")
    L.append("")
    L.append("As instrucoes das tres tarefas estao em saidas/modulo4-bateria-de-testes.md")
    L.append("e os resultados de cada rodada estao gravados na pasta saidas.")
    L.append("")
    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))



# ---------------------------------------------------------------------------
# CICLO 4.3 - APIs publicas brasileiras
# ---------------------------------------------------------------------------
# Todas as fontes abaixo respondem sem cadastro e sem chave de acesso.
# O script sempre imprime a URL que chamou: e ela que voce precisa entender.
# Uma ferramenta de MCP nada mais e do que um invólucro em torno de uma URL
# como estas.

FONTES = {
    "cnpj": {
        "desc": "Dados cadastrais de uma empresa pela Receita Federal",
        "url": "https://brasilapi.com.br/api/cnpj/v1/{0}",
        "arg": "o CNPJ, so numeros. Exemplo: apis cnpj 06990590000123",
        "teste": "06990590000123",
        "fonte": "BrasilAPI",
    },
    "cep": {
        "desc": "Endereco a partir do CEP",
        "url": "https://brasilapi.com.br/api/cep/v2/{0}",
        "arg": "o CEP, so numeros. Exemplo: apis cep 65080805",
        "teste": "65080805",
        "fonte": "BrasilAPI",
    },
    "bancos": {
        "desc": "Lista de todos os bancos com codigo e ISPB",
        "url": "https://brasilapi.com.br/api/banks/v1",
        "arg": None,
        "teste": None,
        "fonte": "BrasilAPI",
    },
    "feriados": {
        "desc": "Feriados nacionais de um ano",
        "url": "https://brasilapi.com.br/api/feriados/v1/{0}",
        "arg": "o ano com quatro digitos. Exemplo: apis feriados 2026",
        "teste": "2026",
        "fonte": "BrasilAPI",
    },
    "taxas": {
        "desc": "Taxas oficiais vigentes (Selic, CDI, IPCA)",
        "url": "https://brasilapi.com.br/api/taxas/v1",
        "arg": None,
        "teste": None,
        "fonte": "BrasilAPI",
    },
    "municipios": {
        "desc": "Todos os municipios de um estado, com codigo do IBGE",
        "url": "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{0}/municipios",
        "arg": "a sigla da UF. Exemplo: apis municipios MA",
        "teste": "MA",
        "fonte": "IBGE, servico de dados",
    },
    "serie": {
        "desc": "Serie temporal do Banco Central (1 = cambio, 432 = Selic meta, 433 = IPCA)",
        "url": ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.{0}/dados"
                "?formato=json&dataInicial={1}&dataFinal={2}"),
        "arg": ("o codigo da serie e, opcionalmente, duas datas dd/mm/aaaa. "
                "Exemplo: apis serie 432 01/01/2026 31/08/2026"),
        "teste": "432",
        "fonte": "Banco Central, SGS",
    },
    "contratacoes": {
        "desc": "Contratacoes publicas divulgadas no PNCP num periodo",
        "url": ("https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
                "?dataInicial={1}&dataFinal={2}&codigoModalidadeContratacao={3}"
                "&uf={0}&pagina=1&tamanhoPagina=50"),
        "arg": ("a UF, a data inicial e a data final em aaaammdd e, opcionalmente, "
                "o codigo da modalidade (6 = pregao eletronico). "
                "Exemplo: apis contratacoes MA 20260801 20260810"),
        "teste": None,
        "fonte": "PNCP, Portal Nacional de Contratacoes Publicas",
    },
}

PRECISAM_CADASTRO = [
    ("Portal da Transparencia", "despesas, convenios, servidores, sancoes",
     "cadastro gratuito de um minuto para obter a chave"),
    ("DataJud, do CNJ", "processos judiciais", "cadastro gratuito para obter a chave"),
]


def buscar(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": "DECC0294-UFMA/1.0 (atividade academica)",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        bruto = r.read().decode("utf-8", errors="replace")
    return json.loads(bruto)


def achatar(d, prefixo=""):
    """Transforma um dicionario aninhado em pares chave/valor de um nivel."""
    saida = {}
    for k, v in d.items():
        chave = prefixo + str(k)
        if isinstance(v, dict):
            saida.update(achatar(v, chave + "."))
        elif isinstance(v, list):
            saida[chave] = "; ".join(
                str(x if not isinstance(x, dict) else x.get("descricao", x)) for x in v[:5])
        else:
            saida[chave] = v
    return saida


def gravar(nome, dados):
    os.makedirs("dados", exist_ok=True)
    caminho_json = os.path.join("dados", nome + ".json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    gerados = [caminho_json]

    lista = None
    if isinstance(dados, list):
        lista = dados
    elif isinstance(dados, dict):
        for chave in ("data", "items", "resultado", "registros"):
            if isinstance(dados.get(chave), list):
                lista = dados[chave]
                break

    if lista and lista and isinstance(lista[0], (dict,)):
        linhas = [achatar(x) for x in lista]
        colunas = []
        for l in linhas:
            for c in l:
                if c not in colunas:
                    colunas.append(c)
        caminho_csv = os.path.join("dados", nome + ".csv")
        with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=colunas, delimiter=SEP, extrasaction="ignore")
            w.writeheader()
            for l in linhas:
                w.writerow(l)
        gerados.append(caminho_csv)
    return gerados


def montar_url(chave, argumentos):
    f = FONTES[chave]
    url = f["url"]
    if "{" not in url:
        return url
    if chave == "serie":
        if not argumentos:
            return None
        codigo = argumentos[0]
        d1 = argumentos[1] if len(argumentos) > 1 else "01/01/2026"
        d2 = argumentos[2] if len(argumentos) > 2 else date.today().strftime("%d/%m/%Y")
        return url.format(codigo, d1, d2)
    if chave == "contratacoes":
        if len(argumentos) < 3:
            return None
        modalidade = argumentos[3] if len(argumentos) > 3 else "6"
        return url.format(argumentos[0].upper(), argumentos[1], argumentos[2], modalidade)
    if not argumentos:
        return None
    return url.format(argumentos[0])


def listar_fontes():
    titulo("MODULO 4 - CICLO 4.3 - FONTES PUBLICAS BRASILEIRAS")
    print()
    print("Todas as fontes abaixo respondem sem cadastro e sem chave de acesso.")
    print()
    for chave in FONTES:
        f = FONTES[chave]
        print("  %-14s %s" % (chave, f["desc"]))
        print("  %-14s fonte: %s" % ("", f["fonte"]))
        print("  %-14s URL:   %s" % ("", f["url"]))
        if f["arg"]:
            print("  %-14s uso:   %s" % ("", f["arg"]))
        else:
            print("  %-14s uso:   apis %s" % ("", chave))
        print()
    print("EXIGEM CADASTRO GRATUITO E FICAM FORA DA AULA")
    for nome, o_que, como in PRECISAM_CADASTRO:
        print("  %s: %s (%s)" % (nome, o_que, como))
    print()
    print("Para saber o que o laboratorio alcanca:")
    print("  python atividade_modulo4.py apis testar")
    return 0


def testar_fontes():
    titulo("MODULO 4 - CICLO 4.3 - DIAGNOSTICO DE ACESSO")
    print()
    print("Testando cada fonte a partir desta maquina. Isso leva cerca de um minuto.")
    print()
    resultados = []
    for chave in FONTES:
        f = FONTES[chave]
        args = [f["teste"]] if f["teste"] else []
        if chave == "contratacoes":
            hoje = date.today()
            args = ["MA", hoje.strftime("%Y%m01"), hoje.strftime("%Y%m%d"), "6"]
        url = montar_url(chave, args)
        if not url:
            resultados.append((chave, "sem teste automatico", "-"))
            print("  [--] %-14s sem teste automatico" % chave)
            continue
        try:
            inicio = datetime.now()
            buscar(url, timeout=20)
            ms = int((datetime.now() - inicio).total_seconds() * 1000)
            resultados.append((chave, "alcancavel", "%d ms" % ms))
            print("  [OK] %-14s alcancavel (%d ms)" % (chave, ms))
        except urllib.error.HTTPError as e:
            resultados.append((chave, "respondeu com erro HTTP %s" % e.code, "-"))
            print("  [!!] %-14s respondeu com erro HTTP %s" % (chave, e.code))
        except Exception as e:
            resultados.append((chave, "inalcancavel: %s" % type(e).__name__, "-"))
            print("  [XX] %-14s inalcancavel (%s)" % (chave, type(e).__name__))

    os.makedirs("dados", exist_ok=True)
    L = ["# Diagnostico de acesso as APIs publicas", "",
         "Modulo 4, ciclo 4.3. Gerado em %s pelo script atividade_modulo4.py."
         % datetime.now().strftime("%d/%m/%Y as %H:%M"), "",
         "| Fonte | Situacao | Tempo |", "|---|---|---|"]
    for chave, situacao, tempo in resultados:
        L.append("| %s | %s | %s |" % (chave, situacao, tempo))
    L += ["", "## O que fazer com isto", "",
          "Fonte inalcancavel a partir do laboratorio nao e defeito do script: e",
          "restricao de rede da instituicao. Registre quais fontes o laboratorio",
          "bloqueia. Numa organizacao, essa e a primeira pergunta antes de propor",
          "qualquer integracao: o dado existe, e a rede deixa chegar nele?", ""]
    caminho = os.path.join("dados", "api-diagnostico.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print()
    print("Diagnostico gravado em: " + caminho)
    return 0


def consultar(chave, argumentos):
    f = FONTES[chave]
    url = montar_url(chave, argumentos)
    if not url:
        print()
        print("Faltou argumento para a fonte '%s'." % chave)
        print("Uso: " + (f["arg"] or ("apis " + chave)))
        return 1

    titulo("MODULO 4 - CICLO 4.3 - CONSULTA A " + chave.upper())
    print()
    print("Fonte: " + f["fonte"])
    print("URL chamada:")
    print("  " + url)
    print()
    print("Esta URL e o que uma ferramenta de MCP executaria por baixo.")
    print("Guarde-a: ela e a resposta a pergunta 'de onde veio esse dado?'.")
    print()

    try:
        dados = buscar(url)
    except urllib.error.HTTPError as e:
        print("A fonte respondeu com erro HTTP %s." % e.code)
        if e.code == 404:
            print("Costuma significar argumento invalido: confira o valor que voce passou.")
        elif e.code == 429:
            print("Excesso de pedidos. Espere um minuto e tente de novo.")
        return 1
    except Exception as e:
        print("Nao consegui alcancar a fonte (%s)." % type(e).__name__)
        print("Pode ser restricao de rede do laboratorio. Rode 'apis testar' para saber.")
        return 1

    gerados = gravar("api-" + chave, dados)

    if isinstance(dados, list):
        print("Registros recebidos: %d" % len(dados))
        if dados and isinstance(dados[0], dict):
            print()
            print("Primeiro registro:")
            for k, v in list(achatar(dados[0]).items())[:10]:
                print("  %-28s %s" % (k, str(v)[:60]))
    elif isinstance(dados, dict):
        print("Campos recebidos:")
        for k, v in list(achatar(dados).items())[:14]:
            print("  %-28s %s" % (k, str(v)[:60]))

    print()
    print("GRAVADO:")
    for g in gerados:
        print("  + " + g)
    print()
    print("O arquivo .json guarda a resposta como ela veio. O .csv, quando existe,")
    print("e a mesma resposta em formato de planilha, pronta para analise.")
    return 0


def apis(argumentos):
    if not argumentos:
        return listar_fontes()
    chave = argumentos[0].strip().lower()
    if chave in ("testar", "teste", "diagnostico"):
        return testar_fontes()
    if chave not in FONTES:
        print()
        print("Fonte '%s' nao existe." % chave)
        print("Execute 'apis' sem argumento para ver a lista.")
        return 1
    return consultar(chave, argumentos[1:])


def main():
    cmd = (sys.argv[1].strip().lower() if len(sys.argv) > 1 else "")
    if cmd in ("iniciar", "criar", "start"):
        return iniciar()
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    if cmd in ("apis", "api"):
        return apis(sys.argv[2:])
    print(__doc__)
    print("Comandos disponiveis:")
    print("  python atividade_modulo4.py iniciar        prepara a bateria de testes")
    print("  python atividade_modulo4.py conferir       valida e gera o relatorio")
    print("  python atividade_modulo4.py apis           lista as fontes publicas")
    print("  python atividade_modulo4.py apis testar    diagnostico de acesso")
    print("  python atividade_modulo4.py apis <fonte>   consulta uma fonte")
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
