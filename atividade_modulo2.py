#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 ATIVIDADE DO MODULO 2 - Ambiente de trabalho digital
 DECC0294 - Tecnologia da Informacao e Comunicacao Aplicada a Administracao
 UFMA - Curso de Administracao - 2026.2
=============================================================================

O QUE ESTE ARQUIVO E
    Um unico script que monta a pasta do seu projeto e depois confere se a
    entrega A1 esta completa. Voce nao precisa saber programar.

COMO USAR (peca ao agente, no opencode desktop)

    1) "execute o arquivo atividade_modulo2.py com o comando criar"
       Cria as cinco pastas, o README.md, o AGENTS.md e o .gitignore.

    2) Preencha o README.md e o AGENTS.md, e mova para entregas/ os arquivos
       do modulo 1.

    3) "execute o arquivo atividade_modulo2.py com o comando conferir"
       Verifica tudo o que a entrega A1 exige e escreve o relatorio em
       entregas/A1-relatorio.md, dizendo item por item o que esta pronto e o
       que falta.

    Sem nenhum comando, o script imprime estas instrucoes.

ONDE SALVAR ESTE ARQUIVO
    Na raiz da pasta do seu projeto, junto do README.md.

Nao precisa instalar nada. Roda com o Python que ja vem com o ambiente.
=============================================================================
"""

import os
import re
import sys
from datetime import datetime

PASTAS = ["dados", "prompts", "saidas", "entregas"]

README = """# Projeto da disciplina DECC0294

Tecnologia da Informacao e Comunicacao Aplicada a Administracao
UFMA, Curso de Administracao, 2026.2

## Identificacao

- Nome completo: PREENCHER
- Matricula: PREENCHER
- Turma: T01

## Organizacao ou base de dados escolhida

PREENCHER: qual organizacao ou base publica voce vai usar no semestre, e por que.
Duas ou tres linhas bastam. A escolha pode ser trocada ate o encontro 6.

## Como este projeto esta organizado

- `dados/` arquivos de entrada, como vieram da fonte, sem edicao
- `prompts/` as instrucoes dadas ao agente, um arquivo por tecnica
- `saidas/` material de trabalho produzido pelo agente
- `entregas/` os arquivos que valem nota
- `AGENTS.md` a configuracao de comportamento do agente neste projeto

## Declaracao de uso de inteligencia artificial

Ferramenta e modelo usados: PREENCHER

As instrucoes dadas ao agente estao registradas em `prompts/`. Os resultados
foram conferidos contra a fonte e as correcoes estao anotadas nas entregas.
"""

AGENTS = """# Instrucoes para o agente neste projeto

Este arquivo define como o agente deve se comportar em todas as sessoes
abertas nesta pasta. Preencha as quatro secoes. Entre oito e quinze linhas
no total. Apague os comentarios entre parenteses depois de preencher.

## 1. Papel e contexto

PREENCHER
(Quem voce e, em que area trabalha ou estuda, quem vai ler o que for
produzido. Exemplo: "Voce assiste um estudante de Administracao do sexto
periodo da UFMA. Os textos produzidos aqui sao avaliados por um professor.")

## 2. Formato de saida padrao

PREENCHER
(Como as respostas devem sair por padrao. Exemplo: "Analises: passo a passo,
interpretacao e limitacao declarada. Conceitos: definicao, exemplo brasileiro
e referencia verificavel.")

## 3. Vocabulario e tom

PREENCHER
(Formal ou informal, tecnico ou acessivel, e o que fazer com termos da area.
Exemplo: "Linguagem tecnica. Todo termo definido na primeira ocorrencia.
Frases curtas. Sem adjetivos promocionais.")

## 4. Regras fixas

PREENCHER
(O que o agente nunca deve fazer. Escreva regras que poderiam de fato ser
violadas. Exemplo: "Nunca inventar referencia bibliografica: se nao souber,
escrever NAO SEI. Nunca apresentar numero sem dizer de onde veio. Nunca
escrever o texto final no lugar do estudante: produzir rascunho e apontar o
que precisa de decisao humana.")
"""

GITIGNORE = """# Arquivos que nao devem ser publicados no repositorio

# Dados pessoais e material sensivel (mantenha esta secao)
*sigiloso*
*confidencial*
*pessoal*
dados/brutos-nao-anonimizados/

# Credenciais
.env
*.key
*.pem
credenciais*
senha*
token*

# Arquivos temporarios do Office e do sistema
~$*
Thumbs.db
desktop.ini
.DS_Store

# Ambientes e caches
__pycache__/
*.pyc
.venv/
venv/
.ipynb_checkpoints/

# Arquivos grandes de dado bruto
*.zip
*.7z
*.bak
"""

LEIAME_ENTREGAS = """# Pasta de entregas

Aqui ficam os arquivos que valem nota. Um arquivo por atividade, com o nome
que o roteiro do encontro indicar.

Nomes esperados ate o encontro 3:

- modulo1-ciclo1-verificacao.md
- modulo1-ciclo2-comparacao.md
- modulo1-ciclo3-tarefas.md
- modulo1-mapa-de-tarefas.csv
- modulo1-mapa-de-tarefas.md
- modulo2-ciclo1-infraestrutura.md
- A1-relatorio.md (gerado pelo script)
"""

LEIAME_PROMPTS = """# Caderno de prompts

Um arquivo por tecnica. Cada arquivo guarda a instrucao que funcionou, o que
ela produziu e o que precisou de ajuste.

Este caderno e cobrado na entrega final do semestre. Escrever aqui a cada
encontro custa cinco minutos. Reconstruir no fim do semestre custa um dia.
"""

ESPERADOS_M1 = [
    "modulo1-ciclo1-verificacao.md",
    "modulo1-ciclo2-comparacao.md",
    "modulo1-ciclo3-tarefas.md",
    "modulo1-mapa-de-tarefas.md",
]


def titulo(txt):
    print()
    print("=" * 74)
    print(" " + txt)
    print("=" * 74)


def escrever(caminho, conteudo, criados, mantidos):
    if os.path.exists(caminho):
        mantidos.append(caminho)
        return
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    criados.append(caminho)


def criar():
    titulo("MODULO 2 - CRIACAO DA PASTA DO PROJETO")
    criados, mantidos = [], []

    for p in PASTAS:
        if os.path.isdir(p):
            mantidos.append(p + os.sep)
        else:
            os.makedirs(p, exist_ok=True)
            criados.append(p + os.sep)

    escrever("README.md", README, criados, mantidos)
    escrever("AGENTS.md", AGENTS, criados, mantidos)
    escrever(".gitignore", GITIGNORE, criados, mantidos)
    escrever(os.path.join("entregas", "LEIA-ME.md"), LEIAME_ENTREGAS, criados, mantidos)
    escrever(os.path.join("prompts", "LEIA-ME.md"), LEIAME_PROMPTS, criados, mantidos)
    escrever(os.path.join("dados", ".manter"), "", criados, mantidos)
    escrever(os.path.join("saidas", ".manter"), "", criados, mantidos)

    print()
    if criados:
        print("CRIADO (%d):" % len(criados))
        for c in criados:
            print("  + " + c)
    if mantidos:
        print()
        print("JA EXISTIA, nada foi sobrescrito (%d):" % len(mantidos))
        for m in mantidos:
            print("  = " + m)

    print()
    print("PROXIMOS PASSOS, NESTA ORDEM")
    print()
    print("  1. Abra README.md e substitua os PREENCHER pelo seu nome, matricula")
    print("     e pela organizacao ou base que voce vai usar no semestre.")
    print()
    print("  2. Abra AGENTS.md e preencha as quatro secoes. Leia os comentarios:")
    print("     eles explicam o que entra em cada uma. Apague os comentarios depois.")
    print()
    print("  3. Mova para entregas/ os quatro arquivos do modulo 1.")
    print()
    print("  4. Instale o GitHub Desktop, adicione esta pasta e publique como")
    print("     repositorio PRIVADO.")
    print()
    print("  5. Peca ao agente:")
    print('     "execute atividade_modulo2.py com o comando conferir"')
    return 0


def secoes_agents(texto):
    """Devolve dict com o conteudo de cada secao numerada do AGENTS.md."""
    partes = re.split(r"^##\s+\d\.\s*(.+)$", texto, flags=re.MULTILINE)
    out = {}
    for i in range(1, len(partes), 2):
        nome = partes[i].strip()
        corpo = partes[i + 1]
        corpo = re.sub(r"\([^)]*\)", "", corpo, flags=re.DOTALL)
        corpo = corpo.replace("PREENCHER", "")
        out[nome] = corpo.strip()
    return out


def info_git():
    """Le o estado do repositorio direto dos arquivos, sem depender do git."""
    dados = {"repo": False, "commits": 0, "remoto": None, "ultima": None}
    if not os.path.isdir(".git"):
        return dados
    dados["repo"] = True

    logs = os.path.join(".git", "logs", "HEAD")
    if os.path.exists(logs):
        with open(logs, encoding="utf-8", errors="replace") as f:
            linhas = [l for l in f.read().splitlines() if l.strip()]
        # cada linha do reflog termina com "<acao>: <mensagem>" depois de um TAB
        acoes = [l.split("\t", 1)[1].strip() for l in linhas if "\t" in l]
        dados["commits"] = sum(1 for a in acoes if a.startswith("commit"))
        if acoes:
            dados["ultima"] = acoes[-1]

    cfg = os.path.join(".git", "config")
    if os.path.exists(cfg):
        with open(cfg, encoding="utf-8", errors="replace") as f:
            m = re.search(r'\[remote "origin"\][^\[]*?url\s*=\s*(\S+)', f.read(), re.DOTALL)
            if m:
                dados["remoto"] = m.group(1)
    return dados


def conferir():
    titulo("MODULO 2 - CONFERENCIA DA ENTREGA A1")
    itens = []  # (ok, titulo, detalhe)

    # 1. estrutura
    faltando = [p for p in PASTAS if not os.path.isdir(p)]
    itens.append((
        not faltando,
        "Estrutura de pastas",
        "Todas as quatro pastas existem." if not faltando
        else "Faltam: " + ", ".join(faltando) + ". Execute o comando criar."
    ))

    # 2. README
    if os.path.exists("README.md"):
        txt = open("README.md", encoding="utf-8", errors="replace").read()
        pend = txt.count("PREENCHER")
        itens.append((
            pend == 0,
            "README.md preenchido",
            "Nome, matricula, organizacao e declaracao de uso preenchidos." if pend == 0
            else "Ainda ha %d campo(s) marcado(s) como PREENCHER." % pend
        ))
    else:
        itens.append((False, "README.md preenchido", "Arquivo nao encontrado."))

    # 3. AGENTS.md
    if os.path.exists("AGENTS.md"):
        txt = open("AGENTS.md", encoding="utf-8", errors="replace").read()
        secs = secoes_agents(txt)
        vazias = [k for k, v in secs.items() if len(v) < 25]
        ok = len(secs) >= 4 and not vazias
        if ok:
            det = "As quatro secoes estao preenchidas."
        elif len(secs) < 4:
            det = "Encontrei %d secoes numeradas, esperava 4." % len(secs)
        else:
            det = "Secoes ainda vazias ou curtas demais: " + "; ".join(vazias)
        itens.append((ok, "AGENTS.md com as quatro secoes", det))
    else:
        itens.append((False, "AGENTS.md com as quatro secoes", "Arquivo nao encontrado."))

    # 4. entregas do modulo 1
    presentes = os.listdir("entregas") if os.path.isdir("entregas") else []
    faltam_m1 = [e for e in ESPERADOS_M1 if e not in presentes]
    itens.append((
        not faltam_m1,
        "Entregas do modulo 1 na pasta entregas/",
        "Os quatro arquivos estao no lugar." if not faltam_m1
        else "Faltam: " + ", ".join(faltam_m1)
    ))

    # 5. ficha do ciclo 2.1
    tem_ficha = any(f.startswith("modulo2-ciclo1") for f in presentes)
    itens.append((
        tem_ficha,
        "Ficha de infraestrutura do ciclo 2.1",
        "Encontrada." if tem_ficha
        else "Salve a ficha em entregas/modulo2-ciclo1-infraestrutura.md"
    ))

    # 6. gitignore
    itens.append((
        os.path.exists(".gitignore"),
        "Arquivo .gitignore presente",
        "Presente." if os.path.exists(".gitignore") else "Execute o comando criar."
    ))

    # 7 a 9. repositorio
    g = info_git()
    itens.append((
        g["repo"],
        "Pasta sob controle de versao",
        "Repositorio local encontrado." if g["repo"]
        else "Adicione esta pasta no GitHub Desktop (File, Add Local Repository)."
    ))
    itens.append((
        g["commits"] >= 2,
        "Pelo menos duas versoes gravadas",
        "%d versao(oes) gravada(s)." % g["commits"] if g["commits"]
        else "Nenhuma versao gravada. Escreva uma mensagem e clique em Commit to main."
    ))
    itens.append((
        bool(g["remoto"]),
        "Repositorio publicado",
        ("Publicado em: " + g["remoto"]) if g["remoto"]
        else "Clique em Publish repository, marcando Keep this code private."
    ))

    # relatorio na tela
    ok_n = sum(1 for i in itens if i[0])
    print()
    for ok, tit, det in itens:
        print(("  [OK]    " if ok else "  [FALTA] ") + tit)
        print("           " + det)
    print()
    print("Concluidos: %d de %d." % (ok_n, len(itens)))

    gerar_relatorio(itens, g, ok_n)
    print()
    print("Relatorio escrito em entregas/A1-relatorio.md")
    if ok_n < len(itens):
        print()
        print("Resolva os itens marcados como FALTA e execute 'conferir' de novo.")
        print("Nao saia da aula com item pendente: sem repositorio funcionando voce")
        print("nao acompanha os encontros seguintes.")
        return 1
    print()
    print("Entrega A1 completa. Grave a versao final com a mensagem 'entrega A1',")
    print("publique e envie o endereco do repositorio na turma virtual.")
    return 0


def gerar_relatorio(itens, g, ok_n):
    os.makedirs("entregas", exist_ok=True)
    L = []
    L.append("# Relatorio da entrega A1")
    L.append("")
    L.append("Modulo 2, encontro 3. DECC0294, UFMA, Curso de Administracao.")
    L.append("Gerado em %s pelo script atividade_modulo2.py."
             % datetime.now().strftime("%d/%m/%Y as %H:%M"))
    L.append("")
    L.append("Situacao: %d de %d itens concluidos." % (ok_n, len(itens)))
    L.append("")
    L.append("| Item | Situacao | Observacao |")
    L.append("|---|---|---|")
    for ok, tit, det in itens:
        L.append("| %s | %s | %s |" % (tit, "concluido" if ok else "pendente", det))
    L.append("")
    if g["remoto"]:
        L.append("Endereco do repositorio: %s" % g["remoto"])
        L.append("")
    if g["ultima"]:
        L.append("Ultima versao gravada: %s" % g["ultima"])
        L.append("")
    L.append("## Conferido por mim")
    L.append("")
    L.append("Nome e matricula: ______________________________")
    L.append("")
    L.append(
        "Declaro que o repositorio nao contem dado pessoal identificavel de "
        "terceiro, senha ou chave de acesso, e que conferi a lista de arquivos "
        "antes de publicar."
    )
    L.append("")
    with open(os.path.join("entregas", "A1-relatorio.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main():
    cmd = (sys.argv[1].strip().lower() if len(sys.argv) > 1 else "")
    if cmd in ("criar", "iniciar", "start"):
        return criar()
    if cmd in ("conferir", "validar", "check"):
        return conferir()
    print(__doc__)
    print("Comandos disponiveis:")
    print("  python atividade_modulo2.py criar      monta a pasta do projeto")
    print("  python atividade_modulo2.py conferir   verifica a entrega A1")
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
