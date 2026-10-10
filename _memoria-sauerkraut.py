# -*- coding: utf-8 -*-
"""_memoria-sauerkraut.py — append no log do dia (19/09).

1. O veredito do sauerkraut: duplicata sob outro nome, nao gravar.
2. A lista DUPLICATAS no _gerar-mp4.js e o lote que sobrou (3 variantes).
3. A rodada de skill (2 secoes + 1 edicao) e a consolidacao do MEMORY.md.
Append puro: nunca reescreve o que ja' esta la.
"""
import io
import sys

ARQ = r'.workbuddy-ai\memory\2026-09-19.md'

TEXTO = """
## 🥬 Sauerkraut: o arquivo que o filtro revelou era DUPLICATA (19/09)

O conserto do filtro do `_gerar-mp4.js` trouxe de volta
`repolho/shorts-sauerkraut-en-1080x1920.html` como candidato do lote. **Não gravar:** é o
**mesmo vídeo** que `repolho/shorts-repolho-maos-canva-en.html`, que **já tem mp4**.

Comparado **cena a cena** (não por nome):

| | sauerkraut-en-1080x1920 | repolho-maos-canva-en |
|---|---|---|
| cenas | 8 | 8 |
| duração | 52,0 s | 52,0 s |
| tag da cena 1 | `SAUERKRAUT 1 / 8` | `SAUERKRAUT 1 / 8` |
| CTA final | "Which one should I ferment next?" | idem |
| mp4 | — | **52,00 s**, 1080×1920 |

O `viewBox` dos dois é `0 0 405 720` — o sufixo `-1080x1920` é só o **alvo de render**, não
muda o desenho. Só a redação das legendas muda um pouco ("Wash it, peel the outer leaves" ×
"Wash and pull the outer leaves").

**A lição:** a regra do gêmeo procura o **mesmo nome** sem o sufixo — e **não pega** o caso
em que o mesmo vídeo existe com **outro nome**. Resolvido com a lista **nomeada**
`DUPLICATAS` no `_gerar-mp4.js` (`{arquivo: motivo}`): não é filtro que esconde, é registro
de duplicata **com o motivo escrito** — e **argumento explícito continua gravando**.

**O lote ficou com 3**, todos **variantes de estilo** (tag genérica `SCENE n / N`), não
entradas do pacote: `beterraba/shorts-beterraba-animado-en` (32,8 s),
`beterraba/shorts-beterraba-camadas-en` (30,0 s), `repolho/shorts-repolho-animado-en`
(28,6 s). **Oferecido, não aprovado.**

**Também nesta rodada:**

- **Skill** ganhou o caso **claro sobre claro** (conserto por **contorno**, não por fundo
  escuro), a seção **"A SILHUETA vem antes da cor"** e a lição da **duplicata sob outro
  nome**. `_skill-couveflor-maca.py` (2 âncoras) + 1 edição — **94.926 bytes, 0 NUL**.
- **MEMORY.md consolidado:** 10.360 → **5.863 bytes** (−43%). Estava **truncado na
  injeção**; tirei o que a skill já carrega (o detalhe das regras de desenho) e mantive
  **estado do projeto + regra do usuário**, como o próprio cabeçalho do arquivo manda.
"""


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    crlf = d.count('\r\n')
    eol = '\r\n' if crlf else '\n'
    print('log: %d bytes, %d CRLF' % (len(d), crlf))

    if 'Sauerkraut: o arquivo que o filtro revelou' in d:
        print('JA GRAVADO — nada a fazer.')
        return 0

    if not d.endswith(eol):
        d += eol
    d += TEXTO.replace('\n', eol)

    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: %s (%d bytes)' % (ARQ, len(d)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
