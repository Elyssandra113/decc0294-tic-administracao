"""
Atividade do modulo 13 - Decisao apoiada por IA: contratos, editais e devolutivas
DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
UFMA - Curso de Administracao

O QUE ESTE SCRIPT FAZ

Ele monta a matriz de decisao, calcula a nota ponderada de cada alternativa,
testa se a vencedora muda quando o peso do criterio principal muda, cria o
modelo da devolutiva e confere a entrega C1 inteira.

Nao usa biblioteca externa, nao acessa a rede e nao usa modelo de linguagem.

COMO USAR (peca ao agente do opencode que execute cada comando)

  python atividade_modulo13.py matriz
      Cria entregas/matriz-decisao.csv com as colunas exigidas e um exemplo.

  python atividade_modulo13.py avaliar
      Confere os pesos, calcula o ranking e roda o teste de sensibilidade.
      Grava saidas/resultado-decisao.md.

  python atividade_modulo13.py devolutiva
      Cria entregas/devolutiva.md com as quatro secoes exigidas.

  python atividade_modulo13.py conferir
      Confere as entregas deste encontro.

  python atividade_modulo13.py c1
      Confere a entrega C1 inteira, dos encontros 12, 13 e 14.

ORDEM: matriz -> preencher criterios e pesos -> dar notas -> avaliar ->
devolutiva -> preencher -> conferir -> c1.

A ORDEM DOS PESOS

Preencha peso e justificativa ANTES de dar nota a qualquer alternativa. Peso
escolhido depois de ver o resultado nao e criterio, e justificativa.
"""

import csv
import os
import sys

PASTA_SAIDAS = "saidas"
PASTA_ENTREGAS = "entregas"
MATRIZ = os.path.join(PASTA_ENTREGAS, "matriz-decisao.csv")
DEVOLUTIVA = os.path.join(PASTA_ENTREGAS, "devolutiva.md")
MAPA = os.path.join(PASTA_ENTREGAS, "mapa-documento.md")
RESULTADO = os.path.join(PASTA_SAIDAS, "resultado-decisao.md")

MIN_CRITERIOS = 4
MAX_CRITERIOS = 7
EMPATE_TECNICO = 5.0
DESLOCAMENTO = 20.0

CABECALHO = ["criterio", "peso", "justificativa_do_peso", "alternativa", "nota", "razao_da_nota", "fonte_no_documento"]

EXEMPLO = [
    ["EXEMPLO preco total - apague estas linhas", "40", "e o maior componente do custo do contrato",
     "Proposta A", "8", "menor valor entre as tres", "item 5.1 da proposta"],
    ["EXEMPLO preco total - apague estas linhas", "40", "e o maior componente do custo do contrato",
     "Proposta B", "6", "12% acima da menor", "item 5.1 da proposta"],
]

TEXTO_DEVOLUTIVA = """# Devolutiva

## 1. Objeto e limite
objeto: (a pergunta exata que esta devolutiva responde)
o_que_ficou_fora: (o que nao foi examinado, e por que)

## 2. O que foi examinado
documentos_examinados: (quais, com data e origem)
dados_utilizados: (de onde vieram os numeros)

## 3. Analise
(escreva aqui a analise, ligando cada ponto ao criterio correspondente da
matriz. Cite o trecho do documento quando afirmar o que ele diz.)

## 4. Conclusao fundamentada
recomendacao: (a recomendacao, em uma frase)
criterio_que_sustenta: (qual criterio da matriz decide, e com que peso)
resultado_da_sensibilidade: (a vencedora muda quando o peso principal muda? escreva o resultado do script)
norma_aplicavel: (artigo e lei, ou NAO SE APLICA)
norma_conferida_em: (onde voce conferiu o texto do artigo, com data. Se nao ha norma, escreva NAO SE APLICA)

## 5. Responsabilidade
cargo_de_quem_assina: (o cargo, nao o nome)
uso_de_ferramenta: (em que a ferramenta de IA foi usada nesta devolutiva)
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
    return t.strip() == ""


def num(valor):
    t = str(valor or "").strip().replace("%", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def fmt(v):
    return ("%.2f" % v).replace(".", ",")


# ---------------------------------------------------------------- comandos

def cmd_matriz():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if os.path.exists(MATRIZ):
        print("A matriz ja existe em", MATRIZ)
        return
    with open(MATRIZ, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(CABECALHO)
        for linha in EXEMPLO:
            w.writerow(linha)
    print("Matriz criada em", MATRIZ)
    print()
    print("Uma linha por par criterio e alternativa. O peso se repete em todas as")
    print("linhas do mesmo criterio, e a justificativa tambem.")
    print()
    print("Regras que o script verifica:")
    print("  - de %d a %d criterios" % (MIN_CRITERIOS, MAX_CRITERIOS))
    print("  - pesos somando 100 (contando cada criterio uma vez)")
    print("  - justificativa do peso escrita em todo criterio")
    print("  - nota de 0 a 10, com razao e fonte no documento")
    print("  - toda alternativa avaliada em todo criterio")


def ler_matriz():
    if not os.path.exists(MATRIZ):
        print("A matriz nao existe. Rode: python atividade_modulo13.py matriz")
        sys.exit(1)
    with open(MATRIZ, "r", encoding="utf-8-sig", newline="") as f:
        linhas = [dict(l) for l in csv.DictReader(f, delimiter=";")]
    linhas = [l for l in linhas if not normalizar(l.get("criterio")).startswith("exemplo")]
    if not linhas:
        print("A matriz esta vazia. Apague o exemplo, sim, mas escreva as suas linhas.")
        sys.exit(1)
    return linhas


def montar(linhas, problemas):
    criterios = {}
    alternativas = []
    for i, l in enumerate(linhas, 2):
        crit = (l.get("criterio") or "").strip()
        alt = (l.get("alternativa") or "").strip()
        if not crit or not alt:
            problemas.append("linha %d: criterio ou alternativa em branco." % i)
            continue
        peso = num(l.get("peso"))
        nota = num(l.get("nota"))
        if peso is None:
            problemas.append("criterio '%s': peso vazio ou nao numerico." % crit)
        if nota is None:
            problemas.append("criterio '%s', alternativa '%s': nota vazia ou nao numerica." % (crit, alt))
        elif not (0 <= nota <= 10):
            problemas.append("criterio '%s', alternativa '%s': nota %s fora da faixa de 0 a 10."
                             % (crit, alt, l.get("nota")))
        if vazio(l.get("justificativa_do_peso")):
            problemas.append("criterio '%s': justificativa do peso vazia." % crit)
        if vazio(l.get("razao_da_nota")):
            problemas.append("criterio '%s', alternativa '%s': razao da nota vazia." % (crit, alt))
        if vazio(l.get("fonte_no_documento")):
            problemas.append("criterio '%s', alternativa '%s': fonte no documento vazia. "
                             "Toda nota se verifica em algum lugar." % (crit, alt))

        if crit not in criterios:
            criterios[crit] = {"peso": peso, "notas": {}}
        elif criterios[crit]["peso"] != peso:
            problemas.append("criterio '%s': o peso aparece com valores diferentes em linhas "
                             "diferentes. Use o mesmo peso em todas as linhas do criterio." % crit)
        if alt not in alternativas:
            alternativas.append(alt)
        if nota is not None:
            criterios[crit]["notas"][alt] = nota
    return criterios, alternativas


def ranquear(criterios, alternativas, pesos):
    total = {a: 0.0 for a in alternativas}
    for crit, dados in criterios.items():
        p = pesos.get(crit, 0.0)
        for a in alternativas:
            total[a] += dados["notas"].get(a, 0.0) * p / 100.0
    return sorted(total.items(), key=lambda x: -x[1])


def cmd_avaliar():
    problemas = []
    linhas = ler_matriz()
    criterios, alternativas = montar(linhas, problemas)

    if len(criterios) < MIN_CRITERIOS:
        problemas.append("ha %d criterios. O minimo e %d: menos que isso esconde a decisao."
                         % (len(criterios), MIN_CRITERIOS))
    if len(criterios) > MAX_CRITERIOS:
        problemas.append("ha %d criterios. O maximo e %d: mais que isso dilui os pesos e "
                         "as alternativas empatam." % (len(criterios), MAX_CRITERIOS))
    if len(alternativas) < 2:
        problemas.append("ha %d alternativa. Uma decisao precisa de pelo menos duas."
                         % len(alternativas))

    for crit, dados in criterios.items():
        faltando = [a for a in alternativas if a not in dados["notas"]]
        if faltando:
            problemas.append("criterio '%s': sem nota para %s." % (crit, ", ".join(faltando)))

    pesos = {c: (d["peso"] or 0.0) for c, d in criterios.items()}
    soma = sum(pesos.values())
    if abs(soma - 100.0) > 0.01:
        problemas.append("os pesos somam %s. Precisam somar 100." % fmt(soma))

    if problemas:
        print("=" * 62)
        print("A MATRIZ AINDA NAO PODE SER AVALIADA")
        print("=" * 62)
        for i, p in enumerate(problemas, 1):
            print(" %d. %s" % (i, p))
        sys.exit(1)

    ranking = ranquear(criterios, alternativas, pesos)
    vencedora, nota_v = ranking[0]
    segunda, nota_s = ranking[1]
    diferenca = (nota_v - nota_s) / nota_v * 100 if nota_v else 0.0
    empate = diferenca < EMPATE_TECNICO

    principal = max(pesos, key=lambda c: pesos[c])
    cenarios = []
    for direcao, sinal in (("para cima", 1), ("para baixo", -1)):
        novo = pesos[principal] + sinal * DESLOCAMENTO
        novo = max(0.0, min(100.0, novo))
        resto = 100.0 - novo
        antigo_resto = soma - pesos[principal]
        p2 = {}
        for c, p in pesos.items():
            if c == principal:
                p2[c] = novo
            elif antigo_resto > 0:
                p2[c] = p * resto / antigo_resto
            else:
                p2[c] = resto / max(1, len(pesos) - 1)
        r2 = ranquear(criterios, alternativas, p2)
        cenarios.append((direcao, novo, r2[0][0], r2))

    virou = any(c[2] != vencedora for c in cenarios)

    print("=" * 62)
    print("AVALIACAO DA MATRIZ")
    print("=" * 62)
    print("criterios:   ", len(criterios))
    print("alternativas:", len(alternativas))
    print()
    print("Pesos")
    for c, p in sorted(pesos.items(), key=lambda x: -x[1]):
        print("  %-34s %s" % (c[:34], fmt(p)))
    print()
    print("Ranking (nota ponderada, de 0 a 10)")
    for pos, (a, v) in enumerate(ranking, 1):
        print("  %d. %-30s %s" % (pos, a[:30], fmt(v)))
    print()
    if empate:
        print("EMPATE TECNICO. A diferenca entre a primeira e a segunda e de %s%%," % fmt(diferenca))
        print("abaixo do limite de %s%%. Os criterios escolhidos nao separam as opcoes." % fmt(EMPATE_TECNICO))
        print("A decisao precisa de um criterio novo, declarado, e nao da casa decimal.")
    else:
        print("A diferenca entre a primeira e a segunda e de %s%%." % fmt(diferenca))
    print()
    print("TESTE DE SENSIBILIDADE sobre '%s' (peso atual %s)" % (principal, fmt(pesos[principal])))
    for direcao, novo, venc, _ in cenarios:
        marca = "muda para " + venc if venc != vencedora else "continua " + vencedora
        print("  peso %s para %s: %s" % (direcao, fmt(novo), marca))
    print()
    if virou:
        print("A vencedora MUDA dentro da faixa testada. A decisao depende de um julgamento")
        print("de peso, e a devolutiva precisa dizer qual julgamento e quem o fez.")
    else:
        print("A vencedora NAO muda na faixa testada. A decisao e robusta a esse deslocamento,")
        print("e isso entra na devolutiva como argumento.")

    os.makedirs(PASTA_SAIDAS, exist_ok=True)
    with open(RESULTADO, "w", encoding="utf-8") as f:
        f.write("# Resultado da decisao\n\n")
        f.write("## Pesos\n\n| criterio | peso | justificativa |\n|---|---|---|\n")
        just = {}
        for l in linhas:
            just.setdefault((l.get("criterio") or "").strip(), l.get("justificativa_do_peso") or "")
        for c, p in sorted(pesos.items(), key=lambda x: -x[1]):
            f.write("| %s | %s | %s |\n" % (c, fmt(p), just.get(c, "")))
        f.write("\n## Ranking\n\n| posicao | alternativa | nota ponderada |\n|---|---|---|\n")
        for pos, (a, v) in enumerate(ranking, 1):
            f.write("| %d | %s | %s |\n" % (pos, a, fmt(v)))
        f.write("\nvencedora: %s\n" % vencedora)
        f.write("diferenca_para_a_segunda_percentual: %s\n" % fmt(diferenca))
        f.write("empate_tecnico: %s\n" % ("sim" if empate else "nao"))
        f.write("\n## Teste de sensibilidade\n\n")
        f.write("criterio_principal: %s\n" % principal)
        f.write("peso_original: %s\n\n" % fmt(pesos[principal]))
        f.write("| cenario | peso | vencedora |\n|---|---|---|\n")
        for direcao, novo, venc, _ in cenarios:
            f.write("| %s | %s | %s |\n" % (direcao, fmt(novo), venc))
        f.write("\nvencedora_muda: %s\n" % ("sim" if virou else "nao"))
    print()
    print("Resultado gravado em", RESULTADO)


def cmd_devolutiva():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if os.path.exists(DEVOLUTIVA):
        print("A devolutiva ja existe em", DEVOLUTIVA)
        return
    with open(DEVOLUTIVA, "w", encoding="utf-8") as f:
        f.write(TEXTO_DEVOLUTIVA)
    print("Devolutiva criada em", DEVOLUTIVA)
    print()
    print("Escreva a conclusao antes de pedir redacao ao modelo. E confira toda norma")
    print("citada na fonte oficial: o campo norma_conferida_em e obrigatorio.")


# ------------------------------------------------------------- conferencia

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


def conferir_modulo(problemas):
    if not os.path.exists(RESULTADO):
        problemas.append("resultado-decisao.md nao existe. Rode: python atividade_modulo13.py avaliar")
    if not os.path.exists(MAPA):
        problemas.append("mapa-documento.md nao existe. Ele e a entrega do ciclo 13.2.")
    else:
        with open(MAPA, "r", encoding="utf-8") as f:
            mapa = f.read()
        baixo = normalizar(mapa)
        categorias = [("obrigac", "obrigações com prazo"), ("pagamento", "pagamento e reajuste"),
                      ("penalidad", "penalidades e rescisão"), ("escopo", "escopo e exclusões"),
                      ("fiscaliza", "fiscalização e aceite")]
        for chave, nome in categorias:
            if chave not in baixo:
                problemas.append("mapa-documento.md: a categoria %s nao aparece no mapa." % nome)
        if '"' not in mapa and "“" not in mapa:
            problemas.append("mapa-documento.md: nao ha nenhum trecho transcrito entre aspas. "
                             "Cada item precisa do trecho de origem.")
        if "nao consta" not in baixo and "não consta" not in mapa.lower():
            problemas.append("mapa-documento.md: nenhuma categoria marcada como NAO CONSTA e "
                             "nenhum registro de que todas constam. Se o documento cobre tudo, "
                             "escreva isso.")

    if not os.path.exists(DEVOLUTIVA):
        problemas.append("devolutiva.md nao existe. Rode: python atividade_modulo13.py devolutiva")
        return
    campos = ler_campos(DEVOLUTIVA)
    obrigatorios = [
        ("objeto", "o objeto da devolutiva"),
        ("o_que_ficou_fora", "o limite do exame"),
        ("documentos_examinados", "os documentos examinados"),
        ("dados_utilizados", "os dados utilizados"),
        ("recomendacao", "a recomendacao"),
        ("criterio_que_sustenta", "o criterio que sustenta a recomendacao"),
        ("resultado_da_sensibilidade", "o resultado do teste de sensibilidade"),
        ("norma_aplicavel", "a norma aplicavel, ou NAO SE APLICA"),
        ("norma_conferida_em", "onde a norma foi conferida"),
        ("cargo_de_quem_assina", "o cargo de quem assina"),
        ("uso_de_ferramenta", "a declaracao de uso da ferramenta"),
    ]
    for chave, nome in obrigatorios:
        if vazio(campos.get(chave)):
            problemas.append("devolutiva.md: falta %s (campo %s)." % (nome, chave))

    norma = normalizar(campos.get("norma_aplicavel"))
    conferida = campos.get("norma_conferida_em") or ""
    if norma and "nao se aplica" not in norma and not vazio(conferida):
        if len(conferida.strip()) < 15:
            problemas.append("devolutiva.md: o campo norma_conferida_em precisa dizer onde e "
                             "quando voce conferiu o texto do artigo. Citacao nao conferida em "
                             "parecer e o erro que esta disciplina existe para evitar.")

    with open(DEVOLUTIVA, "r", encoding="utf-8") as f:
        texto = f.read()
    if "## 3. Analise" in texto:
        corpo = texto.split("## 3. Analise", 1)[1].split("## 4.", 1)[0]
        corpo = corpo.replace("(escreva aqui a analise, ligando cada ponto ao criterio correspondente da", "")
        corpo = corpo.replace("matriz. Cite o trecho do documento quando afirmar o que ele diz.)", "")
        if len(corpo.strip()) < 200:
            problemas.append("devolutiva.md: a secao 3, Analise, tem menos de 200 caracteres. "
                             "E a secao que liga a matriz ao documento.")

    # sensibilidade declarada precisa bater com o apurado
    if os.path.exists(RESULTADO):
        res = ler_campos(RESULTADO)
        apurado = normalizar(res.get("vencedora_muda"))
        declarado = normalizar(campos.get("resultado_da_sensibilidade"))
        if apurado and declarado and not vazio(declarado):
            diz_muda = "muda" in declarado and "nao muda" not in declarado and "não muda" not in declarado
            if apurado == "sim" and not diz_muda:
                problemas.append("devolutiva.md: o script apurou que a vencedora MUDA no teste de "
                                 "sensibilidade, e a devolutiva nao diz isso. Esse e o ponto que "
                                 "a chefia vai perguntar.")


def cmd_conferir():
    problemas = []
    print("=" * 62)
    print("CONFERENCIA DO MODULO 13")
    print("=" * 62)
    conferir_modulo(problemas)
    if problemas:
        print("A entrega ainda nao esta completa. Faltam", len(problemas), "itens:\n")
        for i, p in enumerate(problemas, 1):
            print(" %d. %s" % (i, p))
        print()
        print("Corrija e rode a conferencia de novo.")
        sys.exit(1)
    print("Entrega do modulo completa.")
    print()
    print("  matriz-decisao.csv        criterios, pesos justificados e notas com fonte")
    print("  resultado-decisao.md      ranking e teste de sensibilidade")
    print("  mapa-documento.md         cinco categorias com trecho de origem")
    print("  devolutiva.md             conclusao fundamentada, norma conferida, uso declarado")
    print()
    print("Agora rode: python atividade_modulo13.py c1")


ITENS_C1 = [
    ("modelo/ficha-modelo.md", "encontro 12: a ficha do modelo preditivo"),
    ("modelo/resultado.md", "encontro 12: o resultado comparado com o palpite simples"),
    ("saidas/varredura-dados-pessoais.md", "encontro 13: a varredura de dado pessoal"),
    ("entregas/inventario-dados.csv", "encontro 13: o inventario com base legal"),
    ("AGENTS.md", "encontro 13: a secao de uso seguro"),
    (".gitignore", "encontro 13: a pasta de dados restritos declarada"),
    ("entregas/plano-resposta-incidente.md", "encontro 13: o plano de resposta a incidente"),
    ("entregas/matriz-decisao.csv", "encontro 14: a matriz de decisao"),
    ("saidas/resultado-decisao.md", "encontro 14: a avaliacao com teste de sensibilidade"),
    ("entregas/mapa-documento.md", "encontro 14: o mapa do documento"),
    ("entregas/devolutiva.md", "encontro 14: a devolutiva fundamentada"),
]


def cmd_c1():
    print("=" * 62)
    print("CONFERENCIA DA ENTREGA C1 - 40% DA NOTA 3")
    print("=" * 62)
    faltando = []
    for caminho, nome in ITENS_C1:
        existe = os.path.exists(caminho)
        print("  [%s] %s" % ("x" if existe else " ", nome))
        if not existe:
            faltando.append((caminho, nome))
    print()

    problemas = []
    conferir_modulo(problemas)
    problemas = [p for p in problemas if "nao existe" not in p]

    if faltando:
        print("Faltam %d arquivos:" % len(faltando))
        for caminho, nome in faltando:
            print("  - %s (%s)" % (caminho, nome))
        print()
    if problemas:
        print("E ha %d pendencias de conteudo:" % len(problemas))
        for i, p in enumerate(problemas, 1):
            print("  %d. %s" % (i, p))
        print()
    if faltando or problemas:
        print("O que estiver pendente aqui conta como nao entregue. Corrija e rode de novo.")
        sys.exit(1)

    print("C1 completa.")
    print()
    print("Faca o commit pelo GitHub Desktop e confira, na lista de arquivos, que a pasta")
    print("de dados restritos nao aparece. O commit e a entrega.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    comando = sys.argv[1].lower()
    if comando == "matriz":
        cmd_matriz()
    elif comando == "avaliar":
        cmd_avaliar()
    elif comando == "devolutiva":
        cmd_devolutiva()
    elif comando == "conferir":
        cmd_conferir()
    elif comando == "c1":
        cmd_c1()
    else:
        print("Comando desconhecido:", comando)
        print("Use: matriz, avaliar, devolutiva, conferir, c1")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        print("\nInterrompido.")
