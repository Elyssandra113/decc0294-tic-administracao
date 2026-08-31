#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 9 - Automacao de documentos
 DECC0294 - UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que separa a parte fixa do seu documento das variaveis
    que mudam a cada execucao, gera um documento por linha da tabela, e mede
    se a automacao compensa.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute atividade_modulo9.py com o comando iniciar"
       Cria o modelo em prompts/modulo9-modelo.md, a tabela de variaveis em
       dados/modulo9-variaveis.csv e o formulario de medicao em
       entregas/modulo9-fluxo.csv

    2) Adapte o modelo ao seu documento e preencha tres linhas de variaveis.

    3) "execute atividade_modulo9.py com o comando gerar"
       Produz um documento por linha em saidas/, avisa variavel sem valor e
       coluna sem uso.

    4) "execute atividade_modulo9.py com o comando conferir"
       Valida a medicao, calcula em quantas execucoes o investimento se paga
       e gera entregas/modulo9-relatorio.md

    Sem nenhum comando, o script imprime estas instrucoes.

A REGRA QUE O SCRIPT APLICA
    Ganho declarado sem os tres tempos medidos nao conta. E variavel usada no
    modelo sem coluna correspondente na tabela interrompe a geracao: e o
    defeito que faz o documento sair com um campo em branco no lugar do valor.

Nao precisa instalar nada. Roda com o Python que ja vem com o ambiente.
=============================================================================
"""

import csv
import os
import re
import sys
from datetime import date

SEP = ";"
MODELO = os.path.join("prompts", "modulo9-modelo.md")
VARIAVEIS = os.path.join("dados", "modulo9-variaveis.csv")
FLUXO = os.path.join("entregas", "modulo9-fluxo.csv")
RELATORIO = os.path.join("entregas", "modulo9-relatorio.md")

COLS_FLUXO = ["item", "valor", "observacao"]
ITENS_FLUXO = [
    ("tempo_manual_minutos", "", "quanto a tarefa levava por execucao, antes"),
    ("tempo_automatizado_minutos", "", "quanto leva agora, incluindo conferencia"),
    ("tempo_construcao_minutos", "", "quanto voce gastou hoje construindo o fluxo"),
    ("execucoes_por_ano", "", "quantas vezes a tarefa e feita por ano"),
    ("passo_irreversivel", "", "onde o fluxo se torna irreversivel"),
    ("o_que_se_confere", "", "no maximo dois itens"),
    ("cargo_responsavel", "", "o cargo, nao a pessoa"),
    ("se_a_conferencia_falhar", "", "o que se faz"),
]

TEXTO_MODELO = """# Modelo de documento

Responsavel por este modelo: PREENCHER
Ultima revisao: PREENCHER

## Regra para dado ausente

Se alguma variavel vier vazia, escrever NAO INFORMADO no lugar e acrescentar
um aviso no inicio do documento listando os campos faltantes.

## Documento

RELATORIO MENSAL DE [AREA]
Periodo de referencia: [MES_REFERENCIA]
Unidade: [UNIDADE]

No periodo de referencia foram registrados [QUANTIDADE] atendimentos, contra
a meta de [META] estabelecida para o periodo. O custo total apurado foi de
R$ [CUSTO_TOTAL].

Observacao do responsavel: [OBSERVACAO]

Elaborado por [RESPONSAVEL] em [DATA_ELABORACAO].

---

COMO ADAPTAR ESTE MODELO

1. Substitua o texto acima pelo seu documento real.
2. Troque por marcadores entre colchetes tudo que muda a cada execucao.
3. Use nomes descritivos: [MES_REFERENCIA] e nao [X1].
4. Nenhum numero fixo dentro do texto: meta e valor de referencia sao variaveis.
5. Cada marcador precisa de uma coluna com o mesmo nome em
   dados/modulo9-variaveis.csv
"""


def titulo(t):
    print()
    print("=" * 74)
    print(" " + t)
    print("=" * 74)


def marcadores(texto):
    corpo = texto.split("COMO ADAPTAR ESTE MODELO")[0]
    return sorted(set(re.findall(r"\[([A-Z0-9_]{2,})\]", corpo)))


def iniciar():
    titulo("MODULO 9 - CICLO 9.2 - CRIACAO DO MODELO")
    for p in ("prompts", "dados", "entregas", "saidas"):
        os.makedirs(p, exist_ok=True)
    criados = []

    if not os.path.exists(MODELO):
        with open(MODELO, "w", encoding="utf-8") as f:
            f.write(TEXTO_MODELO)
        criados.append(MODELO)

    if not os.path.exists(VARIAVEIS):
        cols = marcadores(TEXTO_MODELO)
        with open(VARIAVEIS, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=SEP)
            w.writerow(cols)
            for _ in range(3):
                w.writerow([""] * len(cols))
        criados.append(VARIAVEIS)

    if not os.path.exists(FLUXO):
        with open(FLUXO, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=SEP)
            w.writerow(COLS_FLUXO)
            for item, valor, obs in ITENS_FLUXO:
                w.writerow([item, valor, obs])
        criados.append(FLUXO)

    print()
    if criados:
        print("CRIADO:")
        for c in criados:
            print("  + " + c)
    else:
        print("Todos os arquivos ja existiam. Nada foi sobrescrito.")

    print()
    print("PROXIMOS PASSOS")
    print()
    print("  1. Abra " + MODELO + " e substitua pelo seu documento real,")
    print("     trocando por marcadores entre colchetes tudo que muda.")
    print()
    print("  2. Ajuste as colunas de " + VARIAVEIS + " para os marcadores que")
    print("     voce usou, e preencha tres linhas com casos reais.")
    print()
    print("  3. Peca: \"execute atividade_modulo9.py com o comando gerar\"")
    return 0


def gerar():
    titulo("MODULO 9 - CICLO 9.2 - GERACAO DOS DOCUMENTOS")
    if not os.path.exists(MODELO):
        print()
        print("Nao encontrei " + MODELO + ". Execute o comando 'iniciar'.")
        return 1
    if not os.path.exists(VARIAVEIS):
        print()
        print("Nao encontrei " + VARIAVEIS + ". Execute o comando 'iniciar'.")
        return 1

    texto = open(MODELO, encoding="utf-8").read()
    corpo = texto.split("COMO ADAPTAR ESTE MODELO")[0].rstrip()
    usados = marcadores(texto)

    with open(VARIAVEIS, newline="", encoding="utf-8-sig") as f:
        linhas = [l for l in csv.DictReader(f, delimiter=SEP)
                  if any((v or "").strip() for v in l.values())]

    if not linhas:
        print()
        print("A tabela de variaveis esta vazia. Preencha ao menos tres linhas.")
        return 1

    colunas = [c for c in linhas[0].keys() if c]
    faltando = [m for m in usados if m not in colunas]
    sobrando = [c for c in colunas if c not in usados]

    if faltando:
        print()
        print("O modelo usa marcadores que nao tem coluna na tabela:")
        for m in faltando:
            print("  - [%s]" % m)
        print()
        print("Acrescente essas colunas em " + VARIAVEIS + " ou corrija o nome no")
        print("modelo. A geracao foi interrompida: sem isso o documento sairia com")
        print("o marcador cru no lugar do valor.")
        return 1

    if sobrando:
        print()
        print("Colunas da tabela que o modelo nao usa (pode ser erro de digitacao):")
        for c in sobrando:
            print("  - %s" % c)

    os.makedirs("saidas", exist_ok=True)
    gerados, avisos_totais = [], 0

    for i, l in enumerate(linhas, 1):
        doc = corpo
        vazias = []
        for m in usados:
            v = (l.get(m) or "").strip()
            if not v:
                v = "NAO INFORMADO"
                vazias.append(m)
            doc = doc.replace("[%s]" % m, v)
        if vazias:
            aviso = ("> AVISO: os campos a seguir vieram sem valor e foram preenchidos "
                     "com NAO INFORMADO: %s\n\n" % ", ".join(vazias))
            doc = aviso + doc
            avisos_totais += 1
        destino = os.path.join("saidas", "documento-%d.md" % i)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(doc)
        gerados.append((destino, vazias))

    print()
    print("DOCUMENTOS GERADOS (%d):" % len(gerados))
    for destino, vazias in gerados:
        marca = "  + %s" % destino
        if vazias:
            marca += "   (%d campo(s) sem valor)" % len(vazias)
        print(marca)

    print()
    print("Marcadores usados no modelo: %d" % len(usados))
    print("Documentos com campo faltando: %d" % avisos_totais)
    print()
    print("PROXIMO PASSO")
    print("  Leia os tres documentos. Alguma frase ficou sem sentido? E onde o")
    print("  modelo precisa de ajuste na parte fixa.")
    print("  Depois: \"execute atividade_modulo9.py com o comando conferir\"")
    return 0


def conferir():
    titulo("MODULO 9 - CICLO 9.4 - CONFERENCIA E MEDICAO")
    if not os.path.exists(FLUXO):
        print()
        print("Nao encontrei " + FLUXO + ". Execute o comando 'iniciar'.")
        return 1

    with open(FLUXO, newline="", encoding="utf-8-sig") as f:
        dados = {(l.get("item") or "").strip(): (l.get("valor") or "").strip()
                 for l in csv.DictReader(f, delimiter=SEP)}

    erros = []
    numeros = {}
    for campo in ("tempo_manual_minutos", "tempo_automatizado_minutos",
                  "tempo_construcao_minutos", "execucoes_por_ano"):
        bruto = dados.get(campo, "").replace(",", ".")
        try:
            numeros[campo] = float(bruto)
            if numeros[campo] < 0:
                erros.append("%s nao pode ser negativo" % campo)
        except ValueError:
            erros.append("%s precisa ser um numero de minutos" % campo)

    for campo in ("passo_irreversivel", "o_que_se_confere", "cargo_responsavel",
                  "se_a_conferencia_falhar"):
        if len(dados.get(campo, "")) < 10:
            erros.append("%s esta vazio ou curto demais" % campo)

    if "equipe" in dados.get("cargo_responsavel", "").lower() and \
            len(dados.get("cargo_responsavel", "")) < 25:
        erros.append("cargo_responsavel: 'a equipe' nao e um cargo. Nomeie a funcao.")

    gerados = [f for f in os.listdir("saidas")
               if re.match(r"^documento-\d+\.md$", f)] if os.path.isdir("saidas") else []
    if len(gerados) < 3:
        erros.append("faltam documentos gerados: sao %d de 3. Execute 'gerar'."
                     % len(gerados))

    print()
    if erros:
        print("PROBLEMAS QUE PRECISAM SER CORRIGIDOS (%d):" % len(erros))
        for e in erros:
            print("  - " + e)
        print()
        print("O relatorio nao foi gerado.")
        return 1

    manual = numeros["tempo_manual_minutos"]
    automat = numeros["tempo_automatizado_minutos"]
    constr = numeros["tempo_construcao_minutos"]
    por_ano = numeros["execucoes_por_ano"]
    economia = manual - automat

    print("Nenhum problema encontrado.")
    print()
    print("  Tempo manual por execucao:        %.0f min" % manual)
    print("  Tempo automatizado por execucao:  %.0f min" % automat)
    print("  Economia por execucao:            %.0f min" % economia)
    print("  Investimento na construcao:       %.0f min" % constr)

    if economia <= 0:
        equilibrio = None
        print()
        print("  A automacao nao economiza tempo por execucao.")
        print("  Isso e um resultado, e um resultado util: descobrir que nao compensa")
        print("  antes de investir e exatamente o objetivo do metodo. Se ainda assim")
        print("  ela se justifica, o argumento tem de ser reducao de erro, e nao tempo.")
    else:
        equilibrio = constr / economia
        anos = (equilibrio / por_ano) if por_ano else None
        print("  Execucoes ate o investimento se pagar: %.1f" % equilibrio)
        if anos is not None:
            print("  Ou seja, cerca de %.1f ano(s) na frequencia informada." % anos)
        print("  Economia anual estimada: %.0f min (%.1f h)"
              % (economia * por_ano, economia * por_ano / 60.0))

    gerar_relatorio(dados, numeros, economia, equilibrio, gerados)
    print()
    print("Relatorio gerado em: " + RELATORIO)
    print()
    print("ULTIMO PASSO")
    print("  Abra o relatorio e escreva a frase para a chefia: o que era, o que e")
    print("  agora, e em quanto tempo o investimento se paga.")
    return 0


def gerar_relatorio(dados, numeros, economia, equilibrio, gerados):
    L = ["# Fluxo automatizado", "",
         "Modulo 9, encontro 10. DECC0294, UFMA, Curso de Administracao.",
         "Gerado em %s pelo script atividade_modulo9.py." % date.today().strftime("%d/%m/%Y"),
         "", "Nome e matricula: ______________________________", "",
         "## Medicao", "", "| Item | Valor |", "|---|---|"]
    L.append("| Tempo manual por execucao | %.0f min |" % numeros["tempo_manual_minutos"])
    L.append("| Tempo automatizado por execucao | %.0f min |" % numeros["tempo_automatizado_minutos"])
    L.append("| Economia por execucao | %.0f min |" % economia)
    L.append("| Investimento na construcao | %.0f min |" % numeros["tempo_construcao_minutos"])
    L.append("| Execucoes por ano | %.0f |" % numeros["execucoes_por_ano"])
    if equilibrio is not None:
        L.append("| Execucoes ate se pagar | %.1f |" % equilibrio)
        L.append("| Economia anual estimada | %.1f h |"
                 % (economia * numeros["execucoes_por_ano"] / 60.0))
    L += ["", "## Documentacao do fluxo", "",
          "### O que entra e de onde vem", "", "ESCREVA AQUI os arquivos de insumo, "
          "com a origem de cada um e quem os disponibiliza.", "", "- ", "",
          "### A sequencia de comandos", "",
          "ESCREVA AQUI a ordem dos comandos e o que cada um produz.", "", "1. ", "",
          "### Ponto de conferencia", "",
          "- Passo irreversivel: %s" % dados.get("passo_irreversivel", ""),
          "- O que se confere: %s" % dados.get("o_que_se_confere", ""),
          "- Cargo responsavel: %s" % dados.get("cargo_responsavel", ""),
          "- Se a conferencia falhar: %s" % dados.get("se_a_conferencia_falhar", ""), "",
          "### O que fazer quando da errado", "",
          "ESCREVA AQUI os dois ou tres defeitos previsiveis e o que fazer em cada caso.",
          "", "- ", "",
          "## Documentos gerados", ""]
    for g in sorted(gerados):
        L.append("- saidas/%s" % g)
    L += ["", "## Frase para a chefia", "",
          "ESCREVA AQUI em uma frase: o que era, o que e agora, e em quanto tempo o",
          "investimento se paga.", "", "> ", "",
          "## Comparacao com a estimativa do modulo 1", "",
          "ESCREVA AQUI: o ganho que voce estimou la bate com o medido agora? "
          "O que explica a diferenca?", "", "> ", "",
          "---", "", "## Declaracao de uso de inteligencia artificial", "",
          "Ferramenta e modelo usados: ______________________________", "",
          "O modelo com variaveis esta em prompts/ e os documentos gerados em saidas/.",
          "Os tempos foram medidos por mim.", ""]
    os.makedirs("entregas", exist_ok=True)
    with open(RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main():
    cmd = (sys.argv[1].strip().lower() if len(sys.argv) > 1 else "")
    if cmd in ("iniciar", "criar", "start"):
        return iniciar()
    if cmd in ("gerar", "produzir"):
        return gerar()
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    print(__doc__)
    print("Comandos disponiveis:")
    print("  python atividade_modulo9.py iniciar    cria modelo, variaveis e medicao")
    print("  python atividade_modulo9.py gerar      produz um documento por linha")
    print("  python atividade_modulo9.py conferir   valida a medicao e gera o relatorio")
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
