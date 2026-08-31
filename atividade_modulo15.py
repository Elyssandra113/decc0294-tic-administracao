"""
Atividade do modulo 15 - Projeto integrador
DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
UFMA - Curso de Administracao

O QUE ESTE SCRIPT FAZ

Ele confere a entrega C2 do semestre inteiro, cria o roteiro da apresentacao,
cria o formulario de avaliacao por pares e gera o portfolio: o indice de tudo
que voce produziu, com data, agrupado por encontro.

Nao usa biblioteca externa, nao acessa a rede e nao usa modelo de linguagem.

COMO USAR (peca ao agente do opencode que execute cada comando)

  python atividade_modulo15.py c2
      Percorre as entregas dos encontros 2 a 16 e lista o que existe e o que
      falta. O que ele apontar como pendente conta como nao entregue.

  python atividade_modulo15.py apresentacao
      Cria entregas/roteiro-apresentacao.md com os quatro blocos e o tempo
      de cada um.

  python atividade_modulo15.py pares
      Cria entregas/avaliacao-pares.md, com as quatro perguntas para tres
      apresentacoes. Rodado de novo, confere se as justificativas foram escritas.

  python atividade_modulo15.py portfolio
      Gera saidas/portfolio.md com o indice do semestre.

ORDEM NO ENCONTRO: c2 -> corrigir -> apresentacao -> pares -> portfolio.
"""

import os
import sys
import time

PASTA_SAIDAS = "saidas"
PASTA_ENTREGAS = "entregas"
ROTEIRO = os.path.join(PASTA_ENTREGAS, "roteiro-apresentacao.md")
PARES = os.path.join(PASTA_ENTREGAS, "avaliacao-pares.md")
PORTFOLIO = os.path.join(PASTA_SAIDAS, "portfolio.md")

TEXTO_ROTEIRO = """# Roteiro da apresentacao

Dez minutos, cronometrados. Escreva antes, e nao improvise na hora.

## Bloco 1 - O problema e quem o tem (2 min)
usuario_cargo: (o cargo de quem usa)
o_que_ele_faz_hoje: (o caminho atual, resumido)
quanto_custa_hoje: (tempo por execucao e frequencia, com numero)

## Bloco 2 - O que voce construiu (2 min)
escopo_da_versao: (o que o produto resolve, do comeco ao fim)
o_que_ficou_de_fora: (e por que voce cortou)
decisao_de_corte: (a razao da escolha, em uma frase)

## Bloco 3 - Demonstracao ao vivo (4 min)
caso_completo: (o caso que voce vai rodar na frente da turma)
caso_com_dado_errado: (o dado invalido que voce vai usar, e o que o produto faz com ele)

## Bloco 4 - O que ainda nao funciona (2 min)
achados_nao_resolvidos: (o que veio do teste com usuario e ficou de fora)
proximo_item_da_fila: (o que voce faria primeiro)
o_que_faria_com_mais_um_encontro: (uma frase)
"""

TEXTO_PARES = """# Avaliacao por pares

Preencha durante a apresentacao, e nao depois. Sim ou nao, mais uma frase
de justificativa em cada resposta. Justificativa vazia ou elogio generico
nao conta: escreva o que, especificamente, ficou claro ou nao ficou.

## Apresentacao 1
quem_apresentou_1: (nome ou identificacao)
problema_ficou_claro_1: (sim/nao) | (justificativa)
demonstracao_funcionou_1: (sim/nao) | (justificativa)
disse_o_que_nao_funciona_1: (sim/nao) | (justificativa)
voce_usaria_no_seu_setor_1: (sim/nao) | (justificativa)
ideia_que_voce_leva_1: (uma coisa que voce vai usar no seu produto)

## Apresentacao 2
quem_apresentou_2: (nome ou identificacao)
problema_ficou_claro_2: (sim/nao) | (justificativa)
demonstracao_funcionou_2: (sim/nao) | (justificativa)
disse_o_que_nao_funciona_2: (sim/nao) | (justificativa)
voce_usaria_no_seu_setor_2: (sim/nao) | (justificativa)
ideia_que_voce_leva_2: (uma coisa que voce vai usar no seu produto)

## Apresentacao 3
quem_apresentou_3: (nome ou identificacao)
problema_ficou_claro_3: (sim/nao) | (justificativa)
demonstracao_funcionou_3: (sim/nao) | (justificativa)
disse_o_que_nao_funciona_3: (sim/nao) | (justificativa)
voce_usaria_no_seu_setor_3: (sim/nao) | (justificativa)
ideia_que_voce_leva_3: (uma coisa que voce vai usar no seu produto)
"""

# entregas do semestre, por encontro
ENTREGAS = [
    (3, "Ambiente montado e A1", ["AGENTS.md", "README.md"]),
    (4, "Diario de alucinacao", ["entregas/modulo3-ciclo"]),
    (5, "AGENTS.md testado e diagnostico de APIs", ["dados/api-diagnostico.md"]),
    (6, "Mapa de dados e A2", ["entregas/mapa-de-dados"]),
    (7, "Perfil da base e decisao sobre atipicos", ["entregas/modulo6-"]),
    (8, "Consulta e juncao", ["entregas/modulo7-"]),
    (9, "Painel e entrega B1", ["entregas/painel.html"]),
    (10, "Fluxo documentado com ganho medido", ["entregas/modulo9-ciclo4"]),
    (11, "Codificacao, concordancia e entrega B2", ["entregas/modulo10-ciclo3"]),
    (12, "Modelo avaliado contra o palpite simples", ["modelo/ficha-modelo.md", "modelo/resultado.md"]),
    (13, "Inventario, uso seguro e plano de incidente",
     ["saidas/varredura-dados-pessoais.md", "entregas/inventario-dados.csv",
      "entregas/plano-resposta-incidente.md", ".gitignore"]),
    (14, "Matriz, mapa do documento e devolutiva (C1)",
     ["entregas/matriz-decisao.csv", "saidas/resultado-decisao.md",
      "entregas/mapa-documento.md", "entregas/devolutiva.md"]),
    (15, "Ficha do produto, backlog e teste com usuario",
     ["entregas/ficha-produto.md", "entregas/backlog.csv",
      "saidas/backlog-priorizado.md", "entregas/registro-teste.md"]),
    (16, "Apresentacao e avaliacao por pares",
     ["entregas/roteiro-apresentacao.md", "entregas/avaliacao-pares.md"]),
]


def existe(padrao):
    """Aceita caminho exato ou prefixo de nome dentro da pasta."""
    if os.path.exists(padrao):
        return padrao
    pasta = os.path.dirname(padrao) or "."
    prefixo = os.path.basename(padrao)
    if os.path.isdir(pasta):
        for nome in sorted(os.listdir(pasta)):
            if nome.startswith(prefixo):
                return os.path.join(pasta, nome)
    return None


def vazio(valor):
    if not valor:
        return True
    t = str(valor)
    while "(" in t and ")" in t:
        i, j = t.index("("), t.index(")")
        if j < i:
            break
        t = t[:i] + t[j + 1:]
    return t.replace("|", " ").strip() == ""


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


def normalizar(t):
    t = (t or "").strip().lower()
    for de, para in (("á", "a"), ("à", "a"), ("ã", "a"), ("â", "a"), ("é", "e"),
                     ("ê", "e"), ("í", "i"), ("ó", "o"), ("õ", "o"), ("ô", "o"),
                     ("ú", "u"), ("ç", "c")):
        t = t.replace(de, para)
    return t


# ---------------------------------------------------------------- comandos

def cmd_c2():
    print("=" * 66)
    print("CONFERENCIA DA ENTREGA C2 - 60% DA NOTA 3")
    print("=" * 66)
    print()
    faltando = []
    for encontro, nome, arquivos in ENTREGAS:
        achados = [(a, existe(a)) for a in arquivos]
        completo = all(c for _, c in achados)
        parcial = any(c for _, c in achados)
        marca = "x" if completo else ("~" if parcial else " ")
        print("  [%s] encontro %2d  %s" % (marca, encontro, nome))
        for pedido, achado in achados:
            if not achado:
                faltando.append((encontro, pedido))
    print()
    print("  [x] completo   [~] parcial   [ ] ausente")
    print()

    if faltando:
        print("Faltam %d arquivos:" % len(faltando))
        atual = None
        for encontro, pedido in faltando:
            if encontro != atual:
                print("  encontro %d:" % encontro)
                atual = encontro
            print("    - %s" % pedido)
        print()
        print("Rode a conferencia de cada encontro para o detalhe do conteudo:")
        print("  python atividade_modulo13.py c1     (encontros 12, 13 e 14)")
        print("  python atividade_modulo14.py conferir  (encontro 15)")
        print()
        print("O que ficar pendente hoje conta como nao entregue. Esta e a ultima janela.")
        sys.exit(1)

    print("Todos os arquivos do semestre estao na pasta.")
    print()
    print("Rode agora, para conferir o conteudo:")
    print("  python atividade_modulo13.py c1")
    print("  python atividade_modulo14.py conferir")
    print("  python atividade_modulo15.py pares")


def cmd_apresentacao():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if os.path.exists(ROTEIRO):
        print("O roteiro ja existe em", ROTEIRO)
        return
    with open(ROTEIRO, "w", encoding="utf-8") as f:
        f.write(TEXTO_ROTEIRO)
    print("Roteiro criado em", ROTEIRO)
    print()
    print("O bloco 4 vale tanto quanto os outros. Dizer o que nao funciona e parte")
    print("da nota, e nao desconto nela.")


def cmd_pares():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if not os.path.exists(PARES):
        with open(PARES, "w", encoding="utf-8") as f:
            f.write(TEXTO_PARES)
        print("Formulario criado em", PARES)
        print()
        print("Preencha durante as apresentacoes. Rode este comando de novo ao final")
        print("para conferir se as justificativas foram escritas.")
        return

    campos = ler_campos(PARES)
    problemas = []
    avaliadas = 0
    for i in (1, 2, 3):
        quem = campos.get("quem_apresentou_%d" % i)
        if vazio(quem):
            problemas.append("apresentacao %d: nao identificada." % i)
            continue
        avaliadas += 1
        for base, nome in (("problema_ficou_claro", "o problema ficou claro"),
                           ("demonstracao_funcionou", "a demonstracao funcionou"),
                           ("disse_o_que_nao_funciona", "disse o que nao funciona"),
                           ("voce_usaria_no_seu_setor", "voce usaria no seu setor")):
            valor = campos.get("%s_%d" % (base, i)) or ""
            if vazio(valor):
                problemas.append("apresentacao %d: falta a resposta sobre %s." % (i, nome))
                continue
            if "|" not in valor:
                problemas.append("apresentacao %d, %s: falta a justificativa depois da barra."
                                 % (i, nome))
                continue
            resposta, _, just = valor.partition("|")
            r = normalizar(resposta)
            if not (r.startswith("sim") or r.startswith("nao")):
                problemas.append("apresentacao %d, %s: a resposta precisa ser sim ou nao."
                                 % (i, nome))
            if vazio(just) or len(just.strip().split()) < 4:
                problemas.append("apresentacao %d, %s: a justificativa esta vazia ou curta demais. "
                                 "Escreva o que especificamente ficou claro ou nao ficou."
                                 % (i, nome))
        if vazio(campos.get("ideia_que_voce_leva_%d" % i)):
            problemas.append("apresentacao %d: falta a ideia que voce leva." % i)

    print("=" * 66)
    print("AVALIACAO POR PARES")
    print("=" * 66)
    print("apresentacoes avaliadas:", avaliadas, "de 3")
    print()
    if problemas:
        print("Faltam %d itens:\n" % len(problemas))
        for i, p in enumerate(problemas, 1):
            print(" %d. %s" % (i, p))
        print()
        print("A avaliacao volta para quem apresentou. 'Ficou bom' nao diz nada a ele.")
        sys.exit(1)
    print("Formulario completo. Ele volta para quem apresentou.")


def cmd_portfolio():
    pastas = ["entregas", "saidas", "modelo", "dados"]
    arquivos = []
    for pasta in pastas:
        if not os.path.isdir(pasta):
            continue
        for raiz, subpastas, nomes in os.walk(pasta):
            subpastas[:] = [s for s in subpastas if s not in (".git", "__pycache__", "restrito")]
            for nome in sorted(nomes):
                caminho = os.path.join(raiz, nome)
                try:
                    st = os.stat(caminho)
                except OSError:
                    continue
                arquivos.append((caminho, st.st_size, st.st_mtime))
    for solto in ("AGENTS.md", "README.md", ".gitignore"):
        if os.path.exists(solto):
            st = os.stat(solto)
            arquivos.append((solto, st.st_size, st.st_mtime))

    if not arquivos:
        print("Nao ha arquivos nas pastas de entrega. Rode os scripts dos encontros anteriores.")
        sys.exit(1)

    arquivos.sort(key=lambda x: x[2])

    os.makedirs(PASTA_SAIDAS, exist_ok=True)
    with open(PORTFOLIO, "w", encoding="utf-8") as f:
        f.write("# Portfolio do semestre\n\n")
        f.write("DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao\n")
        f.write("Gerado em %s\n\n" % time.strftime("%d/%m/%Y"))
        f.write("## O que voce produziu, por encontro\n\n")
        for encontro, nome, pedidos in ENTREGAS:
            achados = [existe(p) for p in pedidos]
            achados = [a for a in achados if a]
            if not achados:
                continue
            f.write("### Encontro %d - %s\n\n" % (encontro, nome))
            for a in achados:
                try:
                    st = os.stat(a)
                    f.write("- `%s` (%s, %d bytes)\n"
                            % (a, time.strftime("%d/%m/%Y", time.localtime(st.st_mtime)), st.st_size))
                except OSError:
                    f.write("- `%s`\n" % a)
            f.write("\n")
        f.write("## Todos os arquivos da pasta, em ordem de criacao\n\n")
        f.write("| arquivo | data | bytes |\n|---|---|---|\n")
        for caminho, tamanho, quando in arquivos:
            f.write("| %s | %s | %d |\n"
                    % (caminho, time.strftime("%d/%m/%Y", time.localtime(quando)), tamanho))
        f.write("\n## Tres frases suas\n\n")
        f.write("o_que_ficou_pronto: (o que, deste semestre, ja esta em uso ou pronto para uso)\n\n")
        f.write("o_que_eu_usaria_de_novo: (o metodo ou o script que voce levaria para o proximo trabalho)\n\n")
        f.write("o_que_eu_abandonaria: (o que nao serviu, e por que)\n")

    print("=" * 66)
    print("PORTFOLIO GERADO")
    print("=" * 66)
    print("arquivos indexados:", len(arquivos))
    print("gravado em:", PORTFOLIO)
    print()
    print("Abra o arquivo e escreva as tres frases do fim. O indice descreve o que voce")
    print("produziu; as tres frases dizem o que voce faria de novo.")
    print()
    print("Guarde o repositorio fora do computador do laboratorio. A maquina pode ser")
    print("restaurada; o que esta no GitHub, nao.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    comando = sys.argv[1].lower()
    if comando == "c2":
        cmd_c2()
    elif comando == "apresentacao":
        cmd_apresentacao()
    elif comando == "pares":
        cmd_pares()
    elif comando == "portfolio":
        cmd_portfolio()
    else:
        print("Comando desconhecido:", comando)
        print("Use: c2, apresentacao, pares, portfolio")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        print("\nInterrompido.")
