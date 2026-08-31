#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 3 - Diario de alucinacao
 DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
 UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que conduz a atividade do ciclo 3.2. Voce nao precisa
    saber programar. Voce precisa provocar cinco erros do modelo, conferir
    cada um na fonte e registrar o que encontrou.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute o arquivo atividade_modulo3.py com o comando iniciar"
       Cria o diario em entregas/modulo3-diario-de-alucinacao.csv

    2) Preencha um caso por linha, no Excel ou no editor. Salve mantendo o
       formato CSV, separado por ponto e virgula.

    3) "execute o arquivo atividade_modulo3.py com o comando conferir"
       Valida o preenchimento e gera o relatorio em
       entregas/modulo3-diario-de-alucinacao.md

    Sem nenhum comando, o script imprime estas instrucoes.

A REGRA QUE O SCRIPT APLICA
    Cinco casos do mesmo tipo contam como um. Sao exigidos pelo menos tres
    tipos diferentes de erro entre os cinco casos, e a coluna que descreve
    como voce conferiu e obrigatoria.

Nao precisa instalar nada. Roda com o Python que ja vem com o ambiente.
=============================================================================
"""

import csv
import os
import sys
from datetime import date

PASTA = "entregas"
CSV = os.path.join(PASTA, "modulo3-diario-de-alucinacao.csv")
MD = os.path.join(PASTA, "modulo3-diario-de-alucinacao.md")
SEP = ";"
MINIMO = 5
TIPOS_MINIMOS = 3

COLUNAS = [
    "caso",
    "tipo_de_erro",
    "instrucao_usada",
    "o_que_o_modelo_respondeu",
    "como_conferi",
    "fonte_consultada",
    "veredito",
    "o_que_corrigi",
]

TIPOS = {
    "referencia inventada",
    "numero plausivel",
    "atribuicao trocada",
    "procedimento inexistente",
    "sem erro",
}

VEREDITOS = {"confirmado", "incorreto", "nao verificavel"}

EXEMPLO = [
    "Artigo brasileiro sobre retencao de talentos em PMEs",
    "referencia inventada",
    "Cite tres artigos academicos brasileiros dos ultimos dez anos sobre retencao "
    "de talentos, com autores, titulo, revista, ano e DOI.",
    "SILVA, M. A.; OLIVEIRA, R. C. Estrategias de retencao de talentos em PMEs "
    "brasileiras. Revista de Administracao Contemporanea, v. 19, n. 3, 2021.",
    "Procurei o titulo exato entre aspas no Google Academico e colei o DOI em doi.org",
    "Google Academico e doi.org, consultados em 15/09/2026",
    "incorreto",
    "Removi a referencia e busquei um artigo real sobre o tema na base SPELL",
]

LINHA_VAZIA = [""] * len(COLUNAS)


def titulo(t):
    print()
    print("=" * 74)
    print(" " + t)
    print("=" * 74)


def iniciar():
    titulo("MODULO 3 - CICLO 3.2 - CRIACAO DO DIARIO")
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
            w.writerow(LINHA_VAZIA)

    print()
    print("Diario criado em: " + CSV)
    print()
    print("COMO PREENCHER")
    print()
    print("  caso                      Uma frase dizendo o que voce pediu.")
    print()
    print("  tipo_de_erro              Um destes:")
    for t in sorted(TIPOS):
        print("                              " + t)
    print()
    print("  instrucao_usada           A instrucao dada ao agente, na integra.")
    print()
    print("  o_que_o_modelo_respondeu  O essencial da resposta. Nao precisa ser tudo.")
    print()
    print("  como_conferi              O procedimento que voce usou para checar.")
    print("                            Esta coluna e obrigatoria e e o que mais")
    print("                            vale nota. 'Pesquisei' nao serve: diga onde")
    print("                            e o que procurou.")
    print()
    print("  fonte_consultada          Nome da base ou endereco, com a data.")
    print("                            Obrigatoria quando o veredito nao for")
    print("                            'nao verificavel'.")
    print()
    print("  veredito                  confirmado, incorreto ou nao verificavel.")
    print()
    print("  o_que_corrigi             O que voce fez depois de detectar o erro.")
    print()
    print("SUGESTAO DE CASOS, para cobrir tipos diferentes")
    print("  1. Referencias academicas sobre o seu tema.")
    print("  2. Um numero sobre a sua organizacao ou o seu municipio.")
    print("  3. Um artigo de lei ou norma recente.")
    print("  4. Um passo a passo de um sistema que voce usa.")
    print("  5. Um dado regional do Maranhao.")
    print()
    print("A primeira linha vem preenchida como exemplo. Apague-a ou substitua-a.")
    print()
    print("Quando terminar, peca ao agente:")
    print('  "execute atividade_modulo3.py com o comando conferir"')
    return 0


def conferir():
    titulo("MODULO 3 - CICLO 3.2 - CONFERENCIA DO DIARIO")

    if not os.path.exists(CSV):
        print()
        print("Nao encontrei o arquivo " + CSV)
        print("Execute primeiro o comando 'iniciar'.")
        return 1

    with open(CSV, newline="", encoding="utf-8-sig") as f:
        linhas = [l for l in csv.DictReader(f, delimiter=SEP)
                  if (l.get("caso") or "").strip()]

    erros, avisos, casos = [], [], []

    for i, l in enumerate(linhas, start=2):
        caso = (l.get("caso") or "").strip()

        if caso == EXEMPLO[0]:
            avisos.append("linha %d: a linha de exemplo continua no arquivo" % i)
            continue

        tipo = (l.get("tipo_de_erro") or "").strip().lower()
        if tipo not in TIPOS:
            erros.append("linha %d: tipo_de_erro invalido ('%s'). Use um dos cinco tipos."
                         % (i, l.get("tipo_de_erro")))

        veredito = (l.get("veredito") or "").strip().lower()
        if veredito not in VEREDITOS:
            erros.append("linha %d: veredito deveria ser confirmado, incorreto ou "
                         "nao verificavel, veio '%s'" % (i, l.get("veredito")))

        instrucao = (l.get("instrucao_usada") or "").strip()
        if len(instrucao) < 25:
            erros.append("linha %d: instrucao_usada esta vazia ou curta demais. "
                         "Cole a instrucao na integra." % i)

        resposta = (l.get("o_que_o_modelo_respondeu") or "").strip()
        if len(resposta) < 15:
            erros.append("linha %d: o_que_o_modelo_respondeu esta vazio" % i)

        conferi = (l.get("como_conferi") or "").strip()
        if len(conferi) < 20:
            erros.append("linha %d: como_conferi esta vazia ou curta demais. "
                         "Diga onde procurou e o que procurou." % i)
        elif conferi.lower() in ("pesquisei", "procurei", "conferi", "pesquisei na internet"):
            erros.append("linha %d: como_conferi precisa dizer onde e o quê, "
                         "nao apenas que voce procurou." % i)

        fonte = (l.get("fonte_consultada") or "").strip()
        if veredito in ("confirmado", "incorreto") and len(fonte) < 5:
            erros.append("linha %d: fonte_consultada e obrigatoria quando o veredito "
                         "e confirmado ou incorreto." % i)

        corrigi = (l.get("o_que_corrigi") or "").strip()
        if veredito == "incorreto" and len(corrigi) < 10:
            erros.append("linha %d: veredito incorreto exige dizer o que voce corrigiu." % i)

        casos.append({
            "caso": caso, "tipo": tipo, "instrucao": instrucao, "resposta": resposta,
            "conferi": conferi, "fonte": fonte, "veredito": veredito, "corrigi": corrigi
        })

    tipos_usados = sorted(set(c["tipo"] for c in casos if c["tipo"] in TIPOS))

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
    print("Casos registrados: %d (minimo %d)." % (len(casos), MINIMO))
    print("Tipos de erro cobertos: %d (minimo %d) -> %s"
          % (len(tipos_usados), TIPOS_MINIMOS, ", ".join(tipos_usados) or "nenhum"))

    if len(casos) < MINIMO:
        erros.append("faltam casos: sao %d de %d" % (len(casos), MINIMO))
    if len(tipos_usados) < TIPOS_MINIMOS:
        erros.append("faltam tipos diferentes: sao %d de %d. Cinco casos do mesmo "
                     "tipo contam como um." % (len(tipos_usados), TIPOS_MINIMOS))

    if erros:
        print()
        print("O relatorio nao foi gerado. Corrija o diario e execute 'conferir' de novo.")
        return 1

    gerar(casos, tipos_usados, avisos)
    print()
    print("Relatorio gerado em: " + MD)
    print()
    print("ULTIMO PASSO")
    print("  Abra o arquivo e escreva, ao final, a sua conclusao: em que tipo de")
    print("  pedido voce passou a nao confiar, e o que voce vai fazer diferente.")
    return 0


def gerar(casos, tipos, avisos):
    conta = {}
    for c in casos:
        conta[c["veredito"]] = conta.get(c["veredito"], 0) + 1

    L = []
    L.append("# Diario de alucinacao")
    L.append("")
    L.append("Modulo 3, ciclo 3.2. DECC0294, UFMA, Curso de Administracao.")
    L.append("Gerado em %s pelo script atividade_modulo3.py."
             % date.today().strftime("%d/%m/%Y"))
    L.append("")
    L.append("Nome e matricula: ______________________________")
    L.append("")
    L.append("## Resumo")
    L.append("")
    L.append("| Situacao | Casos |")
    L.append("|---|---|")
    for v in sorted(conta):
        L.append("| %s | %d |" % (v, conta[v]))
    L.append("")
    L.append("Tipos de erro cobertos: %s." % ", ".join(tipos))
    L.append("")
    L.append("## Casos")
    L.append("")
    for i, c in enumerate(casos, 1):
        L.append("### Caso %d — %s" % (i, c["caso"]))
        L.append("")
        L.append("- Tipo de erro: %s" % c["tipo"])
        L.append("- Veredito: %s" % c["veredito"])
        L.append("")
        L.append("Instrucao usada:")
        L.append("")
        L.append("> %s" % c["instrucao"])
        L.append("")
        L.append("O que o modelo respondeu:")
        L.append("")
        L.append("> %s" % c["resposta"])
        L.append("")
        L.append("Como conferi: %s" % c["conferi"])
        L.append("")
        if c["fonte"]:
            L.append("Fonte consultada: %s" % c["fonte"])
            L.append("")
        if c["corrigi"]:
            L.append("O que corrigi: %s" % c["corrigi"])
            L.append("")

    if avisos:
        L.append("## Pontos marcados pelo script")
        L.append("")
        for a in avisos:
            L.append("- %s" % a)
        L.append("")

    L.append("## Conclusao")
    L.append("")
    L.append("ESCREVA AQUI: em que tipo de pedido voce passou a nao confiar, e o que")
    L.append("vai fazer diferente a partir de agora.")
    L.append("")
    L.append("> ")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Declaracao de uso de inteligencia artificial")
    L.append("")
    L.append("Ferramenta e modelo usados: ______________________________")
    L.append("")
    L.append("As instrucoes estao registradas na pasta prompts. Todas as fontes foram")
    L.append("consultadas por mim, e nenhuma conferencia foi delegada ao proprio modelo.")
    L.append("")

    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main():
    cmd = (sys.argv[1].strip().lower() if len(sys.argv) > 1 else "")
    if cmd in ("iniciar", "criar", "start"):
        return iniciar()
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    print(__doc__)
    print("Comandos disponiveis:")
    print("  python atividade_modulo3.py iniciar    cria o diario")
    print("  python atividade_modulo3.py conferir   valida e gera o relatorio")
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
