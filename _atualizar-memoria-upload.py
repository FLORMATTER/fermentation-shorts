# -*- coding: utf-8 -*-
"""
_atualizar-memoria-upload.py — registra o trabalho de 17/09 (upload + ?rec nas guias).

Mexe em 3 arquivos, sempre com ancora contada (aborta sem gravar se nao casar):

  1. .workbuddy-ai/memory/MEMORY.md   -> ?play legado / ?rec e o modo de gravar;
                                         RED CABBAGE do guia-geral esta CERTO;
                                         aponta o novo guia de upload.
  2. .workbuddy-ai/memory/2026-09-17.md -> append do trabalho de hoje.
  3. ~/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md -> ?play -> ?rec.

Uso:
    python _atualizar-memoria-upload.py            # dry-run
    python _atualizar-memoria-upload.py --apply
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
MEM = os.path.join(RAIZ, '.workbuddy-ai', 'memory')
SKILL = os.path.join(os.path.expanduser('~'), '.workbuddy-ai', 'skills',
                     'shorts-svg-animado', 'SKILL.md')


def troca(d, velho, novo, n=1):
    c = d.count(velho)
    assert c == n, 'ancora com %d ocorrencia(s), esperado %d:\n---\n%s\n---' % (
        c, n, velho[:200])
    return d.replace(velho, novo, n)


def ler(p):
    bruto = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in bruto else '\n'
    return bruto.replace('\r\n', '\n'), nl


def gravar(p, d, nl):
    saida = d if nl == '\n' else d.replace('\n', nl)
    io.open(p, 'w', encoding='utf-8', newline='').write(saida)


# ── 1. MEMORY.md ────────────────────────────────────────────────────────────
MEM_PLAY_VELHO = """- **`?play` na URL** só existe nos arquivos **`-1080x1920`** (2 hoje:
  `repolho/shorts-sauerkraut-en-1080x1920.html`, `beterraba/shorts-beet-garlic-en-1080x1920.html`).
  Nos shorts de 405×720 o `?play` **não faz nada** — só o botão ▶."""

MEM_PLAY_NOVO = """- **`?rec` na URL é o modo de gravar** (17/09) — existe nos **18 arquivos EN**. É
  sempre `?rec`, nunca `?play`. O **`?play` virou legado**: inicia sozinho depois de
  1,5 s mas **não esconde a capa** (a capa apareceria no vídeo gravado). Além disso o
  `?play` só existe nos arquivos `-1080x1920`; nos de 405×720 não faz nada."""

MEM_COR_VELHO = """pacote PT tinha `#repolhox`. Renderizado e conferido: verde, e a tela diz `1 CABBAGE ·
2% SALT`. Corrigido. **Cor não se decide por grep — renderize.**"""

MEM_COR_NOVO = """pacote PT tinha `#repolhox`. Renderizado e conferido: verde, e a tela diz `1 CABBAGE ·
2% SALT`. Corrigido. **Cor não se decide por grep — renderize.**

**⚠️ Mas `RED CABBAGE` no `guia-geral/shorts-5-easiest-en.html` está CERTO.** É outro
vídeo: a cena 3 daquele arquivo é desenhada em **magenta de verdade** (`#a8497c`,
`#7d2f5e`, `#42162e`), então "RED CABBAGE" descreve o desenho. Conferido no SVG **antes**
de mexer. **Não trocar** — trocar seria repetir o erro do falso positivo de 149px:
consertar um defeito que só existe na leitura apressada."""

MEM_UPLOAD_VELHO = """No OBS: **Fonte de Navegador** 1080×1920, **nunca** Captura de Tela."""

MEM_UPLOAD_NOVO = """No OBS: **Fonte de Navegador** 1080×1920, **nunca** Captura de Tela.

**Upload: `guias/guia-de-upload.md`** (17/09) — as 3 portas (criar canal → gravar
`.mp4` → subir), o YouTube Studio campo por campo, Short vs vídeo normal, celular,
os erros que travam o upload e o que fazer nas primeiras 24 h. **Não existe nenhum
`.mp4` no projeto** — o usuário ainda não gravou nada, e o canal ainda não foi criado
(o nome não foi escolhido)."""

# ── 2. log do dia ───────────────────────────────────────────────────────────
LOG = """
---

## 📤 17/09 (noite) — "preciso fazer upload": o guia que faltava + 7 correções

**Pedido:** `eu presciso fazer unplownd ..` (upload).

**Estado real apurado antes de responder** — nenhum `.mp4` em lugar nenhum
(Desktop, Vídeos, Downloads, Documentos, Pictures: zero). OBS **não instalado**,
ffmpeg não existe. Conclusão: upload é a **terceira** de três portas, e as duas
primeiras estavam fechadas (canal não criado + nada gravado).

### Criado

- **`guias/guia-de-upload.md`** (261 linhas, PT-BR) — o guia que faltava. As 3 portas,
  YouTube Studio campo por campo (`studio.youtube.com` → CRIAR → Enviar vídeos →
  Detalhes/Elementos/Verificações → Visibilidade → PUBLICAR), tabela campo → de onde
  vem o texto, Short detectado automaticamente (vertical + ≤3 min, **não** existe botão
  de "postar como Short"), caminho pelo celular, a regra da música, 7 erros que travam
  o upload e o checklist das primeiras 24 h.

### Corrigido — 7 âncoras em 4 arquivos (`_consertar-guia-gravacao.py`)

| Arquivo | O que estava errado |
|---|---|
| `guias/como-virar-video-de-verdade.md` | OBS mandava usar **"Captura de tela"** → num monitor deitado o Short sai **deitado e com borda**. Agora é Fonte de Navegador + `?rec`. E a Parte 4 ganhou ponteiro para o guia de upload |
| `guia-geral/como-gravar-e-publicar.md` | URL com `?play` → `?rec` (2 pontos) |
| `repolho/como-gravar-sauerkraut.md` | URL com `?play` → `?rec` (2 pontos) |
| `README.md` | `?play` → `?rec`; ponteiro novo para `guias/guia-de-upload.md` |

Também: `guias/plano-de-postagem.md` ganhou a 4ª linha da tabela (guia de upload).
Backups: `.antes-do-rec2` nos 4 arquivos.

### Conferido (e NÃO mexido — importante)

`RED CABBAGE` na cena 3 do `guia-geral/shorts-5-easiest-en.html` **está certo**: o
desenho é magenta (`#a8497c` / `#7d2f5e` / `#42162e`). Li o SVG antes de "consertar".
Trocar seria repetir o erro do falso positivo de 149px.

### Pendências

1. **Nome do canal / @handle** — ainda não escolhido; trava a Porta 1. 30 arquivos com
   placeholder. Ferramenta pronta: `_trocar-handle.py`.
2. **OBS não instalado** — instalar (`obsproject.com`) ou usar Xbox Game Bar.
3. Nada gravado, nada publicado.
"""

# ── 3. SKILL.md ─────────────────────────────────────────────────────────────
SK_TABELA_VELHO = """| Fonte | **Navegador** (Browser) |
| URL | `file:///…/short.html?play` |
| Largura × Altura | **1080 × 1920** |"""

SK_TABELA_NOVO = """| Fonte | **Navegador** (Browser) |
| URL | `file:///…/short.html?rec` |
| Largura × Altura | **1080 × 1920** |"""

SK_PLAY_VELHO = """- **`?play` na URL** faz começar sozinho depois de 1,5 s. Sem isso, a fonte do OBS
  exigiria *botão direito → Interagir* para clicar no ▶ (e o clique apareceria)."""

SK_PLAY_NOVO = """- **`?rec` na URL** (17/09) é o que se usa para gravar: preenche 1080×1920, esconde a
  capa e os botões e começa sozinho. Sem isso, a fonte do OBS exigiria *botão direito →
  Interagir* para clicar no ▶ (e o clique apareceria no vídeo). Ver a seção
  "o modo `?rec`" acima.
- **`?play` é legado.** Só inicia sozinho (1,5 s depois de carregar) e **não esconde a
  capa** — a capa sairia no vídeo gravado. Só existe nos arquivos `-1080x1920`; nos de
  405×720 não faz nada. Em guia/documentação, sempre escrever `?rec`."""

SK_SHOT_VELHO = '  --screenshot=frame.png "file:///…/short.html?play"'
SK_SHOT_NOVO = '  --screenshot=frame.png "file:///…/short.html?rec"'


PLANO = [
    (os.path.join(MEM, 'MEMORY.md'), [
        (MEM_PLAY_VELHO, MEM_PLAY_NOVO),
        (MEM_COR_VELHO, MEM_COR_NOVO),
        (MEM_UPLOAD_VELHO, MEM_UPLOAD_NOVO),
    ]),
    (os.path.join(MEM, '2026-09-17.md'), None),   # append
    (SKILL, [
        (SK_TABELA_VELHO, SK_TABELA_NOVO),
        (SK_PLAY_VELHO, SK_PLAY_NOVO),
        (SK_SHOT_VELHO, SK_SHOT_NOVO),
    ]),
]


def main():
    aplicar = '--apply' in sys.argv
    total = 0

    for caminho, edicoes in PLANO:
        if not os.path.exists(caminho):
            print('FALTA  %s' % caminho)
            return 1
        d, nl = ler(caminho)
        antes = len(d)

        if edicoes is None:
            if LOG.strip() in d:
                print('%-46s ja tem o bloco de hoje — pulando' % os.path.basename(caminho))
                continue
            d = d.rstrip('\n') + '\n' + LOG
            n = 1
        else:
            try:
                for velho, novo in edicoes:
                    d = troca(d, velho, novo, 1)
            except AssertionError as e:
                print('ABORTOU %s\n  %s' % (caminho, e))
                return 1
            n = len(edicoes)

        print('%-46s %d -> %d bytes  (%d edicoes)' % (
            os.path.basename(caminho), antes, len(d), n))
        total += n

        if aplicar:
            gravar(caminho, d, nl)

    if aplicar:
        print('\nOK — %d edicoes aplicadas' % total)
    else:
        print('\nDRY-RUN — %d edicoes. Rode com --apply.' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
