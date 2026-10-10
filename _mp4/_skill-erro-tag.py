"""Atualiza a skill com o erro (i): array `scenes` sem `tag` -> "undefined" no video.

Duas ancoras contadas. Aborta sem gravar se alguma nao casar uma vez.
"""
import sys

ARQ = r'C:\Users\Saxa\.workbuddy-ai\skills\shorts-svg-animado\SKILL.md'
d = open(ARQ, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in d else '\n'
print('%s: fim de linha %s | %d bytes' % (ARQ.split('\\')[-1], 'CRLF' if nl == '\r\n' else 'LF', len(d)))
orig = d

TROCAS = [
    # --- A) atalho do checklist
    ("""> `python _validar-short.py` (todas as checagens abaixo, com contagens),
> `python _revisar-cenas.py <arquivo>` (renderiza as cenas em PNG para **olhar**) e,
> para o player 16:9, `python _revisar-videolongo.py <arquivo> <cenas>`.
""",
     """> `python _validar-short.py` (todas as checagens abaixo, com contagens),
> `python _revisar-cenas.py <arquivo>` (renderiza as cenas em PNG para **olhar**),
> `python _checar-tag-cena.py` (o rótulo do topo sairia escrito "undefined" — erro (i)) e,
> para o player 16:9, `python _revisar-videolongo.py <arquivo> <cenas>`.
"""),

    # --- B) o erro novo, no fim da secao dos erros
    ("""por cena. Resultado: o total de problemas desses dois arquivos foi **31 → 15 → 1 → 0**.
""",
     """por cena. Resultado: o total de problemas desses dois arquivos foi **31 → 15 → 1 → 0**.

**(i) 🆕 Array `scenes` sem o campo `tag` → a palavra "undefined" QUEIMADA no vídeo.**
O motor de gravação (`_mp4/render.js`) desenha `s.tag` num rótulo no topo de cada cena:

```js
'<text x="202" y="31" text-anchor="middle" font-size="10" ... >' + esc(s.tag) + '</text>';
```

Sem o campo, `esc(undefined)` vira a string **"undefined"** — e ela sai no vídeo, em cima de
**todas** as cenas. Achado em 19/09 no `repolho/shorts-chucrute-30s` (EN **e** PT), já com o
mp4 gravado.

**Por que passou por tudo:** o rótulo não está no short, está no **motor injetado**. O
`_validar-short.py` confere animação e keyframe, não overlay; o `_revisar-cenas.py` renderiza
o short **sem** o motor; e o próprio short nunca escreve essa palavra. Só apareceu ao **tocar
o mp4** e olhar a folha de quadros.

**Duas correções, sempre as duas:**
1. **O short ganha o `tag` que faltava**, na convenção da série — `SAUERKRAUT n / 5` no EN,
   `CHUCRUTE n / 5` no PT (igual ao `shorts-repolho-maos-canva`).
2. **O motor não desenha o rótulo quando o campo não existe.** Um short novo que esquecer o
   `tag` sai **sem rótulo** (feio), nunca escrito "undefined" (defeito).

**Conferir:** `python _checar-tag-cena.py` — varre a série inteira, sai com código 1 se achar.
E **regravar** o mp4 dos arquivos afetados: o defeito está no arquivo, não só na tela.

> ⚠️ A primeira versão do `_checar-tag-cena.py` **deu 0 arquivos quebrados** — procurava
> `.tag` dentro do short (que nunca tem) em vez de conferir se o campo existe no array
> `scenes`. **Verificador que nunca falha não prova nada:** ele tem que ser testado contra a
> versão com o defeito, senão só confirma o que você já acha.
"""),
]

for i, (velho, novo) in enumerate(TROCAS, 1):
    v = velho.replace('\n', nl)
    nv = novo.replace('\n', nl)
    n = d.count(v)
    print('troca %d: casou %d vez(es)' % (i, n))
    if n != 1:
        print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
        sys.exit(1)
    d = d.replace(v, nv, 1)

assert d != orig
open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %d -> %d bytes' % (len(orig), len(d)))
