"""
Atividade do modulo 12 - Governanca de dados, LGPD e ciberseguranca
DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
UFMA - Curso de Administracao

O QUE ESTE SCRIPT FAZ

Ele varre a pasta do projeto procurando dado pessoal, monta o inventario de
dados do seu setor, cria o plano de resposta a incidente e confere se as tres
entregas do encontro estao completas.

Roda inteiramente na sua maquina. Nao acessa a rede, nao usa modelo de
linguagem e nao envia nada para lugar nenhum. Nao usa biblioteca externa.

COMO USAR (peca ao agente do opencode que execute cada comando)

  python atividade_modulo12.py varrer <pasta>
      Procura CPF, CNPJ, e-mail, telefone e CEP nos arquivos de texto da
      pasta. Mostra arquivo, linha e tipo, com o valor mascarado.
      Grava saidas/varredura-dados-pessoais.md.

  python atividade_modulo12.py inventario
      Cria entregas/inventario-dados.csv em branco, com as colunas exigidas.

  python atividade_modulo12.py incidente
      Cria entregas/plano-resposta-incidente.md com as secoes exigidas.

  python atividade_modulo12.py conferir
      Verifica o inventario, a secao de uso seguro do AGENTS.md e o plano.

ORDEM: varrer -> inventario -> preencher -> incidente -> preencher -> conferir.

REGRA DO ENCONTRO

O inventario registra TIPOS de dado e CAMINHOS, nunca dado real. Se voce
escrever um CPF de verdade em qualquer linha, o script recusa a entrega.
"""

import csv
import os
import re
import sys

PASTA_SAIDAS = "saidas"
PASTA_ENTREGAS = "entregas"
VARREDURA = os.path.join(PASTA_SAIDAS, "varredura-dados-pessoais.md")
INVENTARIO = os.path.join(PASTA_ENTREGAS, "inventario-dados.csv")
PLANO = os.path.join(PASTA_ENTREGAS, "plano-resposta-incidente.md")
AGENTS = "AGENTS.md"

MINIMO_LINHAS_INVENTARIO = 5
EXTENSOES = {".txt", ".md", ".csv", ".json", ".html", ".py", ".js", ".sql", ".xml", ".yaml", ".yml"}
IGNORAR_PASTAS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
LIMITE_BYTES = 3 * 1024 * 1024

BASES_LEGAIS = [
    "consentimento",
    "obrigacao legal",
    "administracao publica",
    "estudo por orgao de pesquisa",
    "execucao de contrato",
    "exercicio de direito em processo",
    "protecao da vida",
    "tutela da saude",
    "legitimo interesse",
    "protecao ao credito",
]

CABECALHO_INVENTARIO = [
    "tipo_de_dado", "sensivel", "origem", "onde_fica_guardado", "quem_acessa",
    "base_legal", "finalidade", "prazo_retencao", "poderia_ser_eliminado",
]

EXEMPLO_INVENTARIO = [
    ["EXEMPLO - apague esta linha", "nao", "formulario de inscricao",
     "planilha na pasta compartilhada do setor", "coordenador e dois assistentes",
     "administracao publica", "conceder o auxilio transporte",
     "5 anos apos o fim do beneficio", "nao"],
]

TEXTO_PLANO = """# Plano de resposta a incidente

Uma pagina. Escrita antes, para ser lida durante.

## Cenario
cenario: (o incidente mais provavel no seu setor)
por_que_e_o_mais_provavel: (em uma frase, com base no que voce viu no inventario)

## Primeiras duas horas
Escreva uma acao por linha, no formato: acao | cargo responsavel
Nao vale "a equipe" nem "o setor de TI". Precisa ser um cargo.

acao_1: (o que se faz primeiro) | (cargo)
acao_2: | (cargo)
acao_3: | (cargo)
acao_4: | (cargo)

## Comunicacao
quem_e_comunicado_primeiro: (cargo)
ordem_de_comunicacao: (quem depois de quem)
canal: (telefone, e-mail institucional, sistema interno)

## Criterio de comunicacao externa
quando_vai_a_anpd: (o que precisa acontecer para o caso ser comunicado a autoridade)
quando_os_titulares_sao_avisados: (mesmo raciocinio, do lado das pessoas afetadas)

## O que nao fazer
o_que_nao_fazer: (o que voce ja sabe que alguem vai tentar fazer e nao deve)
"""

RE_CPF = re.compile(r"(?<!\d)(\d{3})[.\s]?(\d{3})[.\s]?(\d{3})[-.\s]?(\d{2})(?!\d)")
RE_CNPJ = re.compile(r"(?<!\d)(\d{2})[.\s]?(\d{3})[.\s]?(\d{3})[/\s]?(\d{4})[-.\s]?(\d{2})(?!\d)")
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
RE_TELEFONE = re.compile(r"(?<!\d)(?:\(?\d{2}\)?[\s-]?)?9?\d{4}[-\s]?\d{4}(?!\d)")
RE_CEP = re.compile(r"(?<!\d)\d{5}-\d{3}(?!\d)")


# ------------------------------------------------------------- validacoes

def cpf_valido(digitos):
    if len(set(digitos)) == 1:
        return False
    nums = [int(d) for d in digitos]
    for tamanho in (9, 10):
        soma = sum(nums[i] * (tamanho + 1 - i) for i in range(tamanho))
        resto = (soma * 10) % 11
        if resto == 10:
            resto = 0
        if resto != nums[tamanho]:
            return False
    return True


def cnpj_valido(digitos):
    if len(set(digitos)) == 1:
        return False
    nums = [int(d) for d in digitos]
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    for pesos, pos in ((pesos1, 12), (pesos2, 13)):
        soma = sum(nums[i] * pesos[i] for i in range(pos))
        resto = soma % 11
        digito = 0 if resto < 2 else 11 - resto
        if digito != nums[pos]:
            return False
    return True


def mascarar(texto, tipo):
    if tipo == "CPF":
        d = re.sub(r"\D", "", texto)
        return "***." + d[3:6] + "." + d[6:9] + "-**"
    if tipo == "CNPJ":
        d = re.sub(r"\D", "", texto)
        return "**." + d[2:5] + "." + d[5:8] + "/****-**"
    if tipo == "e-mail":
        usuario, _, dominio = texto.partition("@")
        return usuario[0] + "***@" + dominio
    if tipo == "telefone":
        d = re.sub(r"\D", "", texto)
        return "*" * (len(d) - 4) + d[-4:]
    if tipo == "CEP":
        return texto[:5] + "-***"
    return "***"


def achados_na_linha(linha):
    saida = []
    for m in RE_CPF.finditer(linha):
        d = re.sub(r"\D", "", m.group(0))
        if len(d) == 11 and cpf_valido(d):
            saida.append(("CPF", m.group(0)))
    for m in RE_CNPJ.finditer(linha):
        d = re.sub(r"\D", "", m.group(0))
        if len(d) == 14 and cnpj_valido(d):
            saida.append(("CNPJ", m.group(0)))
    for m in RE_EMAIL.finditer(linha):
        saida.append(("e-mail", m.group(0)))
    for m in RE_CEP.finditer(linha):
        saida.append(("CEP", m.group(0)))
    ja = {v for _, v in saida}
    for m in RE_TELEFONE.finditer(linha):
        bruto = m.group(0)
        d = re.sub(r"\D", "", bruto)
        if len(d) in (10, 11) and not any(bruto in v or v in bruto for v in ja):
            saida.append(("telefone", bruto))
    return saida


# ---------------------------------------------------------------- comandos

def cmd_varrer(args):
    raiz = args[0] if args else "."
    if not os.path.isdir(raiz):
        print("Pasta nao encontrada:", raiz)
        sys.exit(1)

    achados = []
    arquivos_lidos = 0
    pulados = 0

    for pasta, subpastas, arquivos in os.walk(raiz):
        subpastas[:] = [s for s in subpastas if s not in IGNORAR_PASTAS]
        for nome in arquivos:
            caminho = os.path.join(pasta, nome)
            if os.path.splitext(nome)[1].lower() not in EXTENSOES:
                continue
            try:
                if os.path.getsize(caminho) > LIMITE_BYTES:
                    pulados += 1
                    continue
                with open(caminho, "r", encoding="utf-8", errors="replace") as f:
                    arquivos_lidos += 1
                    for numero, linha in enumerate(f, 1):
                        for tipo, valor in achados_na_linha(linha):
                            achados.append((caminho, numero, tipo, mascarar(valor, tipo)))
            except OSError:
                pulados += 1

    print("=" * 62)
    print("VARREDURA DE DADO PESSOAL")
    print("=" * 62)
    print("pasta:            ", os.path.abspath(raiz))
    print("arquivos lidos:   ", arquivos_lidos)
    if pulados:
        print("arquivos pulados: ", pulados, "(grandes demais ou ilegiveis)")
    print("achados:          ", len(achados))
    print()

    if achados:
        por_tipo = {}
        for _, _, tipo, _ in achados:
            por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        for tipo, qtd in sorted(por_tipo.items(), key=lambda x: -x[1]):
            print("  %-10s %d" % (tipo, qtd))
        print()
        for caminho, numero, tipo, valor in achados[:40]:
            print("  %s:%d  %s  %s" % (caminho, numero, tipo, valor))
        if len(achados) > 40:
            print("  ... e mais %d achados, todos no relatorio." % (len(achados) - 40))
        print()
        print("Decida linha por linha: o dado precisa estar ali? Se precisar, ele esta")
        print("no lugar certo, com o acesso certo? Registre a decisao no inventario.")
    else:
        print("Nenhum padrao de dado pessoal encontrado nos arquivos de texto da pasta.")
        print("Isso nao prova que nao ha dado pessoal. A varredura nao le PDF, imagem,")
        print("planilha binaria nem arquivo compactado, e nao reconhece nome de pessoa.")

    os.makedirs(PASTA_SAIDAS, exist_ok=True)
    with open(VARREDURA, "w", encoding="utf-8") as f:
        f.write("# Varredura de dado pessoal\n\n")
        f.write("pasta: %s\n" % os.path.abspath(raiz))
        f.write("arquivos_lidos: %d\n" % arquivos_lidos)
        f.write("achados: %d\n\n" % len(achados))
        if achados:
            f.write("| arquivo | linha | tipo | valor mascarado |\n|---|---|---|---|\n")
            for caminho, numero, tipo, valor in achados:
                f.write("| %s | %d | %s | %s |\n" % (caminho, numero, tipo, valor))
        else:
            f.write("Nenhum padrao encontrado nos arquivos de texto lidos.\n")
        f.write("\n## Limites desta varredura\n\n")
        f.write("Le apenas arquivos de texto (%s). Nao le PDF, imagem, planilha "
                "binaria nem arquivo compactado. Nao reconhece nome de pessoa, "
                "matricula nem endereco escrito por extenso.\n" % ", ".join(sorted(EXTENSOES)))
        f.write("\n## Decisao\n\n")
        f.write("(escreva o que voce vai fazer com o que foi encontrado, ou registre "
                "que nada foi encontrado e por que isso nao encerra a verificacao)\n")

    print()
    print("Relatorio gravado em", VARREDURA)
    print("Escreva a secao Decisao antes de conferir.")


def cmd_inventario():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if os.path.exists(INVENTARIO):
        print("O inventario ja existe em", INVENTARIO)
        return
    with open(INVENTARIO, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(CABECALHO_INVENTARIO)
        for linha in EXEMPLO_INVENTARIO:
            w.writerow(linha)
    print("Inventario criado em", INVENTARIO)
    print()
    print("Colunas:", ", ".join(CABECALHO_INVENTARIO))
    print()
    print("Bases legais aceitas (artigo 7 da Lei 13.709):")
    for b in BASES_LEGAIS:
        print("  -", b)
    print()
    print("Apague a linha de exemplo e escreva no minimo %d linhas suas." % MINIMO_LINHAS_INVENTARIO)
    print("Nao escreva nenhum dado pessoal real. O inventario registra tipo e caminho.")


def cmd_incidente():
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)
    if os.path.exists(PLANO):
        print("O plano ja existe em", PLANO)
        return
    with open(PLANO, "w", encoding="utf-8") as f:
        f.write(TEXTO_PLANO)
    print("Plano criado em", PLANO)
    print()
    print("Cada acao precisa de um cargo responsavel. O script recusa 'a equipe',")
    print("'o setor de TI' e qualquer responsavel que nao seja um cargo.")


# -------------------------------------------------------------- conferencia

def normalizar(t):
    t = t.strip().lower()
    for de, para in (("á", "a"), ("à", "a"), ("ã", "a"), ("â", "a"), ("é", "e"),
                     ("ê", "e"), ("í", "i"), ("ó", "o"), ("õ", "o"), ("ô", "o"),
                     ("ú", "u"), ("ç", "c")):
        t = t.replace(de, para)
    return t


def vazio(valor):
    """Vazio de verdade, ou ainda com o texto de exemplo entre parenteses."""
    if not valor:
        return True
    t = re.sub(r"\([^)]*\)", "", valor).replace("|", " ").strip()
    return t == ""


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


RESPONSAVEIS_VAGOS = ["a equipe", "equipe", "setor de ti", "o setor de ti", "ti",
                      "todos", "quem estiver", "o pessoal", "a area", "o time"]


def conferir_inventario(problemas):
    if not os.path.exists(INVENTARIO):
        problemas.append("inventario-dados.csv nao existe. Rode: python atividade_modulo12.py inventario")
        return
    with open(INVENTARIO, "r", encoding="utf-8-sig", newline="") as f:
        linhas = [l for l in csv.DictReader(f, delimiter=";")]

    linhas = [l for l in linhas if not normalizar(l.get("tipo_de_dado") or "").startswith("exemplo")]
    if len(linhas) < MINIMO_LINHAS_INVENTARIO:
        problemas.append("inventario-dados.csv tem %d linhas preenchidas. O minimo e %d."
                         % (len(linhas), MINIMO_LINHAS_INVENTARIO))

    bases_norm = [normalizar(b) for b in BASES_LEGAIS]
    for i, l in enumerate(linhas, 2):
        rot = l.get("tipo_de_dado") or ("linha %d" % i)
        for coluna in ("origem", "onde_fica_guardado", "quem_acessa", "finalidade", "prazo_retencao"):
            if vazio(l.get(coluna)):
                problemas.append("inventario-dados.csv, %s: coluna %s vazia." % (rot, coluna))

        base = normalizar(l.get("base_legal") or "")
        if not base:
            problemas.append("inventario-dados.csv, %s: base legal vazia." % rot)
        elif not any(b in base or base in b for b in bases_norm):
            problemas.append("inventario-dados.csv, %s: base legal '%s' nao esta no artigo 7. "
                             "Use uma destas: %s."
                             % (rot, l.get("base_legal"), ", ".join(BASES_LEGAIS)))

        fin = (l.get("finalidade") or "").strip()
        if fin and len(fin.split()) < 3:
            problemas.append("inventario-dados.csv, %s: a finalidade '%s' e um substantivo, "
                             "nao uma finalidade. Escreva com verbo: conceder, controlar, "
                             "comprovar, atender." % (rot, fin))

        prazo = normalizar(l.get("prazo_retencao") or "")
        if "indeterminad" in prazo and len(prazo) < 30:
            problemas.append("inventario-dados.csv, %s: retencao indeterminada sem justificativa. "
                             "Escreva na mesma celula a regra que sustenta guardar para sempre." % rot)

        # dado real no inventario
        texto_linha = " ".join(str(v) for v in l.values() if v)
        reais = [t for t, _ in achados_na_linha(texto_linha) if t in ("CPF", "CNPJ")]
        if reais:
            problemas.append("inventario-dados.csv, %s: ha um %s valido escrito na linha. "
                             "O inventario registra tipo de dado, nunca dado real. Apague."
                             % (rot, reais[0]))

        if normalizar(l.get("sensivel") or "") not in ("sim", "nao", "s", "n"):
            problemas.append("inventario-dados.csv, %s: coluna sensivel precisa ser sim ou nao." % rot)

    eliminaveis = [l for l in linhas if normalizar(l.get("poderia_ser_eliminado") or "").startswith("s")]
    if linhas and not eliminaveis:
        problemas.append("inventario-dados.csv: nenhuma linha marcada como eliminavel. "
                         "O principio da necessidade pede essa revisao. Se nenhum campo "
                         "sobra mesmo, escreva 'nao - revisado' em vez de deixar em branco.")


def conferir_agents(problemas):
    if not os.path.exists(AGENTS):
        problemas.append("AGENTS.md nao existe na pasta do projeto.")
        return
    with open(AGENTS, "r", encoding="utf-8") as f:
        texto = f.read()
    baixo = normalizar(texto)
    if "uso seguro" not in baixo:
        problemas.append("AGENTS.md nao tem a secao de uso seguro de dados.")
        return
    corpo = texto[baixo.index("uso seguro"):]
    if len(corpo.strip()) < 200:
        problemas.append("AGENTS.md: a secao de uso seguro tem menos de 200 caracteres. "
                         "Ela precisa dizer o que nunca se cola, o que se faz antes de enviar "
                         "e onde ficam as bases com dado pessoal.")
    if not os.path.exists(".gitignore"):
        problemas.append(".gitignore nao existe. A pasta de dados restritos precisa estar declarada nele.")
    else:
        with open(".gitignore", "r", encoding="utf-8") as f:
            git = normalizar(f.read())
        if "restrito" not in git and "dados/" not in git:
            problemas.append(".gitignore nao declara a pasta de dados restritos. "
                             "Sem isso a base sobe para o GitHub no proximo commit.")


def conferir_plano(problemas):
    if not os.path.exists(PLANO):
        problemas.append("plano-resposta-incidente.md nao existe. Rode: python atividade_modulo12.py incidente")
        return
    campos = ler_campos(PLANO)
    obrigatorios = [
        ("cenario", "o cenario escolhido"),
        ("por_que_e_o_mais_provavel", "a justificativa do cenario"),
        ("quem_e_comunicado_primeiro", "quem e comunicado primeiro"),
        ("ordem_de_comunicacao", "a ordem de comunicacao"),
        ("canal", "o canal de comunicacao"),
        ("quando_vai_a_anpd", "o criterio de comunicacao a ANPD"),
        ("quando_os_titulares_sao_avisados", "o criterio de aviso aos titulares"),
        ("o_que_nao_fazer", "o que nao fazer"),
    ]
    for chave, nome in obrigatorios:
        if vazio(campos.get(chave)):
            problemas.append("plano-resposta-incidente.md: falta %s (campo %s)." % (nome, chave))

    acoes = [(k, v) for k, v in campos.items() if k.startswith("acao_")]
    preenchidas = [(k, v) for k, v in acoes if not vazio(v)]
    if len(preenchidas) < 3:
        problemas.append("plano-resposta-incidente.md: ha %d acoes preenchidas das primeiras "
                         "duas horas. O minimo e 3." % len(preenchidas))
    for chave, valor in preenchidas:
        if "|" not in valor:
            problemas.append("plano-resposta-incidente.md, %s: falta o cargo responsavel "
                             "depois da barra." % chave)
            continue
        acao, _, responsavel = valor.partition("|")
        responsavel = normalizar(responsavel)
        if vazio(responsavel):
            problemas.append("plano-resposta-incidente.md, %s: cargo responsavel vazio." % chave)
        elif responsavel in RESPONSAVEIS_VAGOS:
            problemas.append("plano-resposta-incidente.md, %s: '%s' nao e um cargo. "
                             "Acao sem pessoa definida nao acontece as duas da manha."
                             % (chave, responsavel))
        if len(acao.strip().split()) < 3:
            problemas.append("plano-resposta-incidente.md, %s: a acao esta curta demais "
                             "para ser executavel." % chave)


def conferir_varredura(problemas):
    if not os.path.exists(VARREDURA):
        problemas.append("varredura-dados-pessoais.md nao existe. Rode: python atividade_modulo12.py varrer .")
        return
    with open(VARREDURA, "r", encoding="utf-8") as f:
        texto = f.read()
    if "## Decisao" not in texto:
        problemas.append("varredura-dados-pessoais.md: a secao Decisao sumiu do arquivo.")
        return
    corpo = texto.split("## Decisao", 1)[1]
    corpo = corpo.replace("(escreva o que voce vai fazer com o que foi encontrado, ou registre", "")
    corpo = corpo.replace("que nada foi encontrado e por que isso nao encerra a verificacao)", "")
    if len(corpo.strip()) < 60:
        problemas.append("varredura-dados-pessoais.md: a secao Decisao esta vazia. "
                         "Escreva o que voce vai fazer com o que foi encontrado.")


def cmd_conferir():
    problemas = []
    print("=" * 62)
    print("CONFERENCIA DO MODULO 12")
    print("=" * 62)
    conferir_varredura(problemas)
    conferir_inventario(problemas)
    conferir_agents(problemas)
    conferir_plano(problemas)

    if problemas:
        print("A entrega ainda nao esta completa. Faltam", len(problemas), "itens:\n")
        for i, p in enumerate(problemas, 1):
            print(" %d. %s" % (i, p))
        print()
        print("Corrija e rode a conferencia de novo.")
        sys.exit(1)

    print("Entrega completa.")
    print()
    print("  varredura-dados-pessoais.md      pasta varrida e decisao escrita")
    print("  inventario-dados.csv             tipos, base legal, finalidade e prazo")
    print("  AGENTS.md                        secao de uso seguro e pasta restrita ignorada")
    print("  plano-resposta-incidente.md      acoes com cargo responsavel e criterio de comunicacao")
    print()
    print("Faca o commit pelo GitHub Desktop e confira, na lista de arquivos, que a")
    print("pasta de dados restritos nao aparece.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    comando = sys.argv[1].lower()
    if comando == "varrer":
        cmd_varrer(sys.argv[2:])
    elif comando == "inventario":
        cmd_inventario()
    elif comando == "incidente":
        cmd_incidente()
    elif comando == "conferir":
        cmd_conferir()
    else:
        print("Comando desconhecido:", comando)
        print("Use: varrer, inventario, incidente, conferir")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        print("\nInterrompido.")
