# -*- coding: utf-8 -*-
"""_limpar-keyframes.py — remove os `@keyframes` que NINGUEM usa.

Por que existe: o `_validar-short.py` acusa 25 problemas na serie e a maioria e' ruido
de `@keyframes` morto. Enquanto o ruido existe, um problema de verdade se perde no meio.

SEGURANCA (a ordem importa):

1. Só mexe em keyframe cujo nome aparece **UMA** vez no arquivo inteiro — ou seja,
   só na propria definicao. Se o nome aparecer em qualquer outro lugar (um
   `animation: 2s spin`, um `style.animation` no JS, um comentario), o arquivo e'
   PULADO. Isso cobre justamente o furo do `usados` do validador, que lê
   `animation:\\s*([\\w-]+)` e num shorthand `animation: 2s spin` captura "2s".
2. A remocao casa as CHAVES com contador (o corpo do keyframe tem `{` aninhado nos
   `0%{}`). Se as chaves nao fecharem, aborta.
3. LISTA NEGRA: `galeria-shorts.html` (o keyframe `nunca` e' um SENTINELA de
   proposito, citado 21x) e `aulas/aula-03-animacoes.html` (`massagear`, citado 2x —
   e' aula, o texto explica o keyframe). Nesses dois nada e' tocado.
4. Depois de remover, confere por arquivo: os `@keyframes` caíram exatamente pelo
   numero removido, as chaves continuam balanceadas e o nome sumiu do arquivo.
   Se qualquer conferencia falhar, o arquivo NAO e' gravado.
5. So' grava com `--apply`. O conteudo removido vai inteiro para
   `_keyframes-removidos.txt` (e' codigo morto, mas fica o registro).

    python _limpar-keyframes.py            # mostra o que faria
    python _limpar-keyframes.py --apply    # grava
    python _limpar-keyframes.py --js       # depois de gravar, roda o _checar-js.py
"""
import io
import os
import re
import subprocess
import sys

IGNORAR_PASTAS = ('.workbuddy-ai', '_revisao', 'node_modules', '_arquivo')
NAO_TOCAR = {
    'galeria-shorts.html',              # keyframe `nunca` = sentinela, citado 21x
    'aulas/aula-03-animacoes.html',     # `massagear` citado 2x, e' material de aula
}
REGISTRO = '_keyframes-removidos.txt'


def arquivos():
    fora = []
    for base, dirs, nomes in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
        for n in nomes:
            if n.endswith('.html'):
                fora.append(os.path.join(base, n).replace('\\', '/').lstrip('./'))
    return sorted(fora)


def orfaos(d):
    """(orfaos_seguros, orfaos_suspeitos) — seguro = nome aparece 1x so'."""
    defs = set(re.findall(r'@keyframes\s+([\w-]+)', d))
    usados = set(re.findall(r'animation:\s*([\w-]+)', d))
    usados |= set(re.findall(r'animation-name:\s*([\w-]+)', d))
    seguros, suspeitos = [], []
    for kf in sorted(defs - usados):
        n = len(re.findall(r'\b%s\b' % re.escape(kf), d))
        (seguros if n == 1 else suspeitos).append(kf)
    return seguros, suspeitos


def recorta_regra(d, kf):
    """Devolve (novo_texto, texto_removido) ou (None, None) se nao der para casar."""
    m = re.search(r'@keyframes\s+' + re.escape(kf) + r'\s*\{', d)
    if not m:
        return None, None
    if len(re.findall(r'@keyframes\s+' + re.escape(kf) + r'\b', d)) != 1:
        return None, None          # definido mais de uma vez: nao mexer

    # --- acha a chave de fechamento contando o aninhamento
    nivel = 0
    j = m.end() - 1
    while j < len(d):
        if d[j] == '{':
            nivel += 1
        elif d[j] == '}':
            nivel -= 1
            if nivel == 0:
                break
        j += 1
    if nivel != 0:
        return None, None          # chaves desbalanceadas: aborta

    # --- inicio: se a linha so' tem espaco antes da regra, apaga a linha inteira
    ls = d.rfind('\n', 0, m.start()) + 1
    ini = ls if d[ls:m.start()].strip() == '' else m.start()

    # --- fim: come o espaco e o fim de linha que sobram
    k = j + 1
    while k < len(d) and d[k] in ' \t':
        k += 1
    if d.startswith('\r\n', k):
        k += 2
    elif k < len(d) and d[k] in '\r\n':
        k += 1
    else:
        k = j + 1
    return d[:ini] + d[k:], d[ini:k]


def conta(d, pat):
    return len(re.findall(pat, d))


def main():
    aplicar = '--apply' in sys.argv
    rodar_js = '--js' in sys.argv

    total_arq = 0
    total_kf = 0
    pulados = []
    registro = []
    mexidos = []

    for arq in arquivos():
        with io.open(arq, 'r', encoding='utf-8', newline='') as fh:
            d = fh.read()
        seguros, suspeitos = orfaos(d)
        if not seguros and not suspeitos:
            continue
        if arq in NAO_TOCAR or os.path.basename(arq) in NAO_TOCAR:
            pulados.append((arq, seguros + suspeitos))
            continue
        if not seguros:
            continue

        novo = d
        removidos = []
        for kf in seguros:
            cand, trecho = recorta_regra(novo, kf)
            if cand is None:
                print('  [!] %s: nao consegui recortar "%s" — arquivo PULADO' % (arq, kf))
                novo = None
                break
            novo = cand
            removidos.append((kf, trecho))
        if novo is None:
            continue

        # ---------- conferencias (falhou = nao grava) ----------
        n_antes = conta(d, r'@keyframes\s')
        n_depois = conta(novo, r'@keyframes\s')
        if n_depois != n_antes - len(removidos):
            print('  [!] %s: keyframes %d -> %d (esperava %d) — NAO gravado'
                  % (arq, n_antes, n_depois, n_antes - len(removidos)))
            continue
        if any(t.count('{') != t.count('}') for _, t in removidos):
            print('  [!] %s: o trecho removido nao fecha as chaves — NAO gravado' % arq)
            continue
        if (d.count('{') - novo.count('{') != sum(t.count('{') for _, t in removidos)
                or d.count('}') - novo.count('}') != sum(t.count('}') for _, t in removidos)):
            print('  [!] %s: sumiu chave a mais ou a menos — NAO gravado' % arq)
            continue
        sobrou = [kf for kf, _ in removidos
                  if re.search(r'\b%s\b' % re.escape(kf), novo)]
        if sobrou:
            print('  [!] %s: "%s" ainda aparece — NAO gravado' % (arq, sobrou[0]))
            continue
        if len(novo) >= len(d):
            print('  [!] %s: o arquivo nao encolheu — NAO gravado' % arq)
            continue

        total_arq += 1
        total_kf += len(removidos)
        nomes = ', '.join(kf for kf, _ in removidos)
        print('  %-56s -%2d  %s  (%d -> %d bytes)'
              % (arq, len(removidos), nomes, len(d), len(novo)))

        for kf, trecho in removidos:
            registro.append('/* === %s :: @keyframes %s === */\n%s\n' % (arq, kf, trecho))

        if aplicar:
            with io.open(arq, 'w', encoding='utf-8', newline='') as fh:
                fh.write(novo)
            mexidos.append(arq)

    print()
    print('=' * 74)
    print('arquivos limpos     : %d' % total_arq)
    print('keyframes removidos : %d' % total_kf)
    if pulados:
        print('pulados (lista negra):')
        for arq, kfs in pulados:
            print('  %-52s %s' % (arq, kfs))

    if aplicar and registro:
        cab = ('# keyframes removidos por _limpar-keyframes.py\n'
               '# Sao codigo morto (o nome nao aparecia em nenhum outro lugar do\n'
               '# arquivo). Guardados apenas como registro, caso algum volte a ser usado.\n\n')
        with io.open(REGISTRO, 'w', encoding='utf-8', newline='') as fh:
            fh.write(cab + '\n'.join(registro))
        print('registro do que saiu: %s (%d regra(s))' % (REGISTRO, len(registro)))
    elif not aplicar:
        print('(dry-run — nada foi gravado; use --apply)')

    if rodar_js:
        print()
        print('--- _checar-js.py nos arquivos mexidos ---')
        ruim = 0
        for arq in mexidos:
            r = subprocess.run([sys.executable, '_checar-js.py', arq],
                               capture_output=True, text=True)
            if r.returncode != 0:
                ruim += 1
                print('  [X] %s' % arq)
                print((r.stdout or '')[-400:])
        print('arquivos conferidos: %d | JS com erro: %d' % (len(mexidos), ruim))
    return 0


if __name__ == '__main__':
    sys.exit(main())
