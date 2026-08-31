"""
Atividade do modulo 11 - Aprendizado de maquina e analytics para a decisao
DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
UFMA - Curso de Administracao

O QUE ESTE SCRIPT FAZ

Ele treina um modelo de regressao linear multipla sobre uma base sua, separa
os dados em treino e teste, e compara o erro do modelo com o erro do palpite
simples (prever sempre a media). Se o modelo nao ganhar do palpite simples,
o script diz isso com todas as letras.

Nao usa nenhuma biblioteca externa. Roda com o Python que ja esta instalado.

COMO USAR (peca ao agente do opencode que execute cada comando)

  python atividade_modulo11.py iniciar
      Cria a pasta modelo/ e o arquivo modelo/ficha-modelo.md, que voce
      preenche com a pergunta de decisao antes de treinar qualquer coisa.

  python atividade_modulo11.py prever <arquivo.csv> <coluna_alvo> [preditoras...]
      Treina o modelo. A coluna_alvo e o numero que voce quer prever.
      As preditoras sao as colunas usadas para prever. Se voce nao listar
      nenhuma, o script usa todas as colunas numericas que sobraram.
      Escreve o resultado em modelo/resultado.md.

  python atividade_modulo11.py conferir
      Verifica se a entrega esta completa antes de voce fechar o encontro.

ORDEM: iniciar -> preencher a ficha -> prever -> ler o resultado -> conferir.

SE O MODELO NAO GANHAR DO PALPITE SIMPLES

Isso nao e erro do script nem seu. Significa que as colunas escolhidas nao
explicam o alvo. Anote isso na ficha e troque as preditoras. Um modelo que
perde para a media e uma resposta valida da atividade.
"""

import csv
import os
import random
import sys

PASTA = "modelo"
FICHA = os.path.join(PASTA, "ficha-modelo.md")
RESULTADO = os.path.join(PASTA, "resultado.md")
SEMENTE = 42
PROPORCAO_TREINO = 0.7

TEXTO_FICHA = """# Ficha do modelo

Preencha antes de treinar. Sem isso o script recusa a conferencia.

## Pergunta de decisao
pergunta: (o que voce quer decidir com essa previsao?)

## Alvo
coluna_alvo: (nome exato da coluna que voce quer prever)
unidade_do_alvo: (reais, dias, unidades, pessoas...)

## Preditoras candidatas
preditoras: (nomes das colunas que voce acha que explicam o alvo, separados por virgula)

## Custo do erro
erro_para_mais: (o que acontece se o modelo prever acima do real)
erro_para_menos: (o que acontece se o modelo prever abaixo do real)

## Depois de rodar
o_modelo_ganhou_do_palpite_simples: (sim / nao)
o_que_voce_faria_com_esse_modelo: (usar / nao usar / usar com que ressalva)
"""


# ----------------------------------------------------------------- leitura

def detectar_separador(caminho):
    with open(caminho, "r", encoding="utf-8-sig", errors="replace") as f:
        amostra = f.read(4096)
    contagens = {s: amostra.count(s) for s in [";", ",", "\t", "|"]}
    return max(contagens, key=contagens.get) or ","


def ler_csv(caminho):
    sep = detectar_separador(caminho)
    with open(caminho, "r", encoding="utf-8-sig", errors="replace", newline="") as f:
        leitor = csv.DictReader(f, delimiter=sep)
        linhas = [dict(l) for l in leitor]
    if not linhas:
        print("O arquivo nao tem linhas de dados.")
        sys.exit(1)
    return linhas, sep


def para_numero(valor):
    if valor is None:
        return None
    t = str(valor).strip()
    if t == "" or t.upper() in ("NA", "N/A", "NAO INFORMADO", "-"):
        return None
    t = t.replace("R$", "").replace("%", "").strip()
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".")
    elif "," in t:
        t = t.replace(",", ".")
    t = t.replace(" ", "")
    try:
        return float(t)
    except ValueError:
        return None


def colunas_numericas(linhas):
    if not linhas:
        return []
    nomes = list(linhas[0].keys())
    saida = []
    for nome in nomes:
        vals = [para_numero(l.get(nome)) for l in linhas]
        preenchidos = [v for v in vals if v is not None]
        if len(preenchidos) >= max(3, int(0.6 * len(linhas))):
            saida.append(nome)
    return saida


# ------------------------------------------------------------------ algebra

def resolver(matriz, vetor):
    """Eliminacao de Gauss com pivotamento parcial. Devolve None se singular."""
    n = len(vetor)
    m = [linha[:] + [vetor[i]] for i, linha in enumerate(matriz)]
    for coluna in range(n):
        piv = max(range(coluna, n), key=lambda r: abs(m[r][coluna]))
        if abs(m[piv][coluna]) < 1e-12:
            return None
        m[coluna], m[piv] = m[piv], m[coluna]
        for linha in range(coluna + 1, n):
            fator = m[linha][coluna] / m[coluna][coluna]
            for k in range(coluna, n + 1):
                m[linha][k] -= fator * m[coluna][k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = m[i][n] - sum(m[i][k] * x[k] for k in range(i + 1, n))
        x[i] = soma / m[i][i]
    return x


def treinar(x_treino, y_treino):
    """Minimos quadrados sobre as equacoes normais. x ja inclui o termo 1."""
    p = len(x_treino[0])
    xtx = [[sum(linha[i] * linha[j] for linha in x_treino) for j in range(p)] for i in range(p)]
    xty = [sum(x_treino[k][i] * y_treino[k] for k in range(len(y_treino))) for i in range(p)]
    return resolver(xtx, xty)


def prever_um(coefs, linha):
    return sum(c * v for c, v in zip(coefs, linha))


def erro_medio_absoluto(reais, previstos):
    return sum(abs(r - p) for r, p in zip(reais, previstos)) / len(reais)


def fmt(v):
    if v is None:
        return "-"
    if abs(v) >= 1000:
        inteiro = f"{v:,.2f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")
        return inteiro
    return f"{v:.4f}".rstrip("0").rstrip(".").replace(".", ",")


# ------------------------------------------------------------------ comandos

def cmd_iniciar():
    os.makedirs(PASTA, exist_ok=True)
    if os.path.exists(FICHA):
        print("A ficha ja existe em", FICHA)
    else:
        with open(FICHA, "w", encoding="utf-8") as f:
            f.write(TEXTO_FICHA)
        print("Ficha criada em", FICHA)
    print()
    print("Preencha a ficha antes de treinar. Depois rode:")
    print("  python atividade_modulo11.py prever <arquivo.csv> <coluna_alvo>")


def cmd_prever(args):
    if len(args) < 2:
        print("Uso: python atividade_modulo11.py prever <arquivo.csv> <coluna_alvo> [preditoras...]")
        sys.exit(1)
    caminho, alvo = args[0], args[1]
    pedidas = args[2:]

    if not os.path.exists(caminho):
        print("Arquivo nao encontrado:", caminho)
        sys.exit(1)

    linhas, sep = ler_csv(caminho)
    numericas = colunas_numericas(linhas)

    if alvo not in linhas[0]:
        print("A coluna", repr(alvo), "nao existe no arquivo.")
        print("Colunas disponiveis:", ", ".join(linhas[0].keys()))
        sys.exit(1)
    if alvo not in numericas:
        print("A coluna", repr(alvo), "nao tem numeros suficientes para ser prevista.")
        print("Colunas numericas encontradas:", ", ".join(numericas) or "nenhuma")
        sys.exit(1)

    if pedidas:
        faltando = [c for c in pedidas if c not in linhas[0]]
        if faltando:
            print("Estas colunas nao existem no arquivo:", ", ".join(faltando))
            sys.exit(1)
        nao_num = [c for c in pedidas if c not in numericas]
        if nao_num:
            print("Estas colunas nao sao numericas e nao podem entrar no modelo:", ", ".join(nao_num))
            print("Este script so trabalha com colunas de numero. Escolha outras.")
            sys.exit(1)
        preditoras = [c for c in pedidas if c != alvo]
    else:
        preditoras = [c for c in numericas if c != alvo]

    if not preditoras:
        print("Nao sobrou nenhuma coluna numerica para prever o alvo.")
        sys.exit(1)

    # monta a base completa, descartando linhas com buraco
    base = []
    descartadas = 0
    for l in linhas:
        y = para_numero(l.get(alvo))
        xs = [para_numero(l.get(c)) for c in preditoras]
        if y is None or any(v is None for v in xs):
            descartadas += 1
            continue
        base.append(([1.0] + xs, y))

    if len(base) < len(preditoras) + 5:
        print("Sobraram apenas", len(base), "linhas completas para", len(preditoras), "preditoras.")
        print("Sao poucas linhas para treinar. Use menos preditoras ou uma base maior.")
        sys.exit(1)

    random.seed(SEMENTE)
    random.shuffle(base)
    corte = int(len(base) * PROPORCAO_TREINO)
    treino, teste = base[:corte], base[corte:]
    if len(teste) < 3:
        print("Sobraram menos de 3 linhas para teste. A base e pequena demais para separar treino e teste.")
        sys.exit(1)

    x_tr = [b[0] for b in treino]
    y_tr = [b[1] for b in treino]
    x_te = [b[0] for b in teste]
    y_te = [b[1] for b in teste]

    coefs = treinar(x_tr, y_tr)
    if coefs is None:
        print("Nao foi possivel treinar: duas ou mais colunas preditoras carregam a mesma informacao.")
        print("Isso acontece quando uma coluna e copia ou soma exata de outra. Retire uma delas.")
        sys.exit(1)

    previstos = [prever_um(coefs, x) for x in x_te]
    ema_modelo = erro_medio_absoluto(y_te, previstos)

    media_treino = sum(y_tr) / len(y_tr)
    ema_palpite = erro_medio_absoluto(y_te, [media_treino] * len(y_te))

    ganhou = ema_modelo < ema_palpite
    reducao = (1 - ema_modelo / ema_palpite) * 100 if ema_palpite else 0.0

    # relatorio na tela
    print("=" * 62)
    print("MODELO TREINADO")
    print("=" * 62)
    print("arquivo:            ", caminho)
    print("separador:          ", repr(sep))
    print("alvo:               ", alvo)
    print("preditoras:         ", ", ".join(preditoras))
    print("linhas completas:   ", len(base), "(descartadas por buraco:", str(descartadas) + ")")
    print("treino / teste:     ", len(treino), "/", len(teste))
    print()
    print("Coeficientes")
    print("  intercepto        ", fmt(coefs[0]))
    for nome, c in zip(preditoras, coefs[1:]):
        print("  " + nome.ljust(18), fmt(c))
    print()
    print("Erro medio absoluto no conjunto de teste")
    print("  modelo            ", fmt(ema_modelo))
    print("  palpite simples   ", fmt(ema_palpite), "(prever sempre a media do treino:", fmt(media_treino) + ")")
    print()
    if ganhou:
        print("O modelo ficou %.1f%% mais preciso que o palpite simples." % reducao)
    else:
        print("O modelo NAO ganhou do palpite simples.")
        print("As colunas escolhidas nao explicam o alvo. Troque as preditoras ou aceite")
        print("que essa pergunta nao se responde com esses dados.")
    print()
    print("Uma leitura de coeficiente: mantendo as outras colunas paradas, cada unidade")
    print("a mais na preditora muda o alvo no valor do coeficiente. Isso descreve a base,")
    print("nao prova que uma coisa causa a outra.")

    os.makedirs(PASTA, exist_ok=True)
    with open(RESULTADO, "w", encoding="utf-8") as f:
        f.write("# Resultado do modelo\n\n")
        f.write("arquivo: %s\n" % caminho)
        f.write("alvo: %s\n" % alvo)
        f.write("preditoras: %s\n" % ", ".join(preditoras))
        f.write("linhas completas: %d\n" % len(base))
        f.write("linhas descartadas: %d\n" % descartadas)
        f.write("treino: %d\nteste: %d\n\n" % (len(treino), len(teste)))
        f.write("## Coeficientes\n\n")
        f.write("| termo | coeficiente |\n|---|---|\n")
        f.write("| intercepto | %s |\n" % fmt(coefs[0]))
        for nome, c in zip(preditoras, coefs[1:]):
            f.write("| %s | %s |\n" % (nome, fmt(c)))
        f.write("\n## Erro no teste\n\n")
        f.write("| medida | valor |\n|---|---|\n")
        f.write("| erro medio absoluto do modelo | %s |\n" % fmt(ema_modelo))
        f.write("| erro medio absoluto do palpite simples | %s |\n" % fmt(ema_palpite))
        f.write("| media do treino | %s |\n" % fmt(media_treino))
        f.write("\nganhou_do_palpite_simples: %s\n" % ("sim" if ganhou else "nao"))
        if ganhou:
            f.write("reducao_de_erro_percentual: %.1f\n" % reducao)
        f.write("\n## Leitura\n\n")
        f.write("(escreva aqui, em duas frases, o que esse resultado permite decidir "
                "e o que ele nao permite)\n")
    print()
    print("Resultado gravado em", RESULTADO)
    print("Abra o arquivo e escreva a secao Leitura. Sem ela a conferencia falha.")


def ler_campos(caminho):
    campos = {}
    if not os.path.exists(caminho):
        return campos
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            if ":" in linha and not linha.strip().startswith("#") and not linha.strip().startswith("|"):
                chave, valor = linha.split(":", 1)
                chave = chave.strip().lower().replace(" ", "_")
                if chave and " " not in chave:
                    campos[chave] = valor.strip()
    return campos


def vazio(valor):
    if not valor:
        return True
    t = valor.strip().lower()
    return t == "" or t.startswith("(")


def cmd_conferir():
    problemas = []
    print("=" * 62)
    print("CONFERENCIA DO MODULO 11")
    print("=" * 62)

    if not os.path.exists(FICHA):
        print("A ficha nao existe. Rode: python atividade_modulo11.py iniciar")
        sys.exit(1)
    if not os.path.exists(RESULTADO):
        print("O resultado nao existe. Rode o comando prever antes de conferir.")
        sys.exit(1)

    ficha = ler_campos(FICHA)
    res = ler_campos(RESULTADO)

    obrigatorios = [
        ("pergunta", "a pergunta de decisao"),
        ("coluna_alvo", "a coluna alvo"),
        ("unidade_do_alvo", "a unidade do alvo"),
        ("preditoras", "as preditoras candidatas"),
        ("erro_para_mais", "o custo de errar para mais"),
        ("erro_para_menos", "o custo de errar para menos"),
        ("o_modelo_ganhou_do_palpite_simples", "se o modelo ganhou do palpite simples"),
        ("o_que_voce_faria_com_esse_modelo", "o que voce faria com o modelo"),
    ]
    for chave, nome in obrigatorios:
        if vazio(ficha.get(chave)):
            problemas.append("ficha-modelo.md: falta " + nome + " (campo " + chave + ")")

    # o custo do erro nao pode ser a mesma frase dos dois lados
    a = (ficha.get("erro_para_mais") or "").strip().lower()
    b = (ficha.get("erro_para_menos") or "").strip().lower()
    if a and b and a == b:
        problemas.append("ficha-modelo.md: errar para mais e errar para menos estao com a mesma "
                         "resposta. Se o custo fosse igual dos dois lados, a decisao seria outra. "
                         "Escreva o que muda em cada direcao.")

    # a resposta sobre o palpite simples tem que bater com o resultado
    declarado = (ficha.get("o_modelo_ganhou_do_palpite_simples") or "").strip().lower()
    apurado = (res.get("ganhou_do_palpite_simples") or "").strip().lower()
    if not vazio(declarado) and apurado and not declarado.startswith(apurado):
        problemas.append("ficha-modelo.md: voce escreveu '%s' em ganhou do palpite simples, "
                         "mas o resultado apurado foi '%s'. Confira o arquivo resultado.md."
                         % (declarado, apurado))

    # a secao Leitura precisa estar escrita
    with open(RESULTADO, "r", encoding="utf-8") as f:
        texto = f.read()
    if "## Leitura" in texto:
        corpo = texto.split("## Leitura", 1)[1].strip()
        corpo = corpo.replace("(escreva aqui, em duas frases, o que esse resultado permite decidir",
                              "").replace("e o que ele nao permite)", "").strip()
        if len(corpo) < 60:
            problemas.append("resultado.md: a secao Leitura esta vazia ou curta demais. "
                             "Escreva o que o resultado permite decidir e o que ele nao permite.")
    else:
        problemas.append("resultado.md: a secao Leitura sumiu do arquivo.")

    # decisao de uso coerente com o resultado
    uso = (ficha.get("o_que_voce_faria_com_esse_modelo") or "").strip().lower()
    if apurado == "nao" and uso.startswith("usar") and "ressalva" not in uso and "nao" not in uso:
        problemas.append("ficha-modelo.md: o modelo perdeu para o palpite simples e voce escreveu "
                         "que usaria mesmo assim, sem ressalva. Justifique ou mude a resposta.")

    if problemas:
        print("A entrega ainda nao esta completa. Faltam", len(problemas), "itens:\n")
        for i, p in enumerate(problemas, 1):
            print(" %d. %s" % (i, p))
        print()
        print("Corrija e rode a conferencia de novo.")
        sys.exit(1)

    print("Entrega completa.")
    print()
    print("  ficha-modelo.md   pergunta, alvo, preditoras e custo do erro preenchidos")
    print("  resultado.md      modelo treinado, comparado com o palpite simples e lido")
    print()
    print("Guarde os dois arquivos na pasta do projeto e faca o commit pelo GitHub Desktop.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    comando = sys.argv[1].lower()
    if comando == "iniciar":
        cmd_iniciar()
    elif comando == "prever":
        cmd_prever(sys.argv[2:])
    elif comando == "conferir":
        cmd_conferir()
    else:
        print("Comando desconhecido:", comando)
        print("Use: iniciar, prever, conferir")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        print("\nInterrompido.")
