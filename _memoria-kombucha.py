# -*- coding: utf-8 -*-
"""_memoria-kombucha.py — log de hoje + fatos duráveis no MEMORY.md.

    python _memoria-kombucha.py

O log diario e' APPEND-ONLY. O MEMORY.md recebe so' o que muda de estado
(catalogo 21->23, mp4 20/21->22/23, pasta nova). O detalhe tecnico fica na skill.
"""
import io
import sys

LOG = '.workbuddy-ai/memory/2026-09-22.md'
MEM = '.workbuddy-ai/memory/MEMORY.md'

FIM_DO_LOG = ('`guias/guia-de-upload.md` — uns 5 minutos, e agora sem a falsa obrigação '
              'de trocar o handle\nantes.')

NOVO_LOG = FIM_DO_LOG + '''

---

## 🥒🍉 Dois vídeos novos: pepino+alho e kombucha de melancia+maçã (tudo em inglês)

Pedido: *"pepino e garlic fermentação. tudo em inglês.... e também kombucha de melancia
e maçã"*. Os dois saíram **só em inglês** (sem irmão PT) — foi o que ele pediu.

| Vídeo | Arquivo | Entrada | Duração |
|---|---|---|---|
| Pepino + alho | `pepino/shorts-cucumber-garlic-en.html` | **#22** | 45,0 s |
| Kombucha melancia + maçã | `kombucha/shorts-watermelon-apple-en.html` | **#23** | 45,4 s |

Pasta nova: **`kombucha/`** — a primeira **bebida** e o primeiro não-legume-de-pote.

### 🔧 O que quebrou, e o conserto

1. `_criar-pepino-alho.py` nasceu com `ValueError: unsupported format character` — um `%`
   solto (`3.5 - 5%`) em string SVG que passava por formatação `%`.
2. A conversão para tokens deixou o `)` do `\\'\\'\\' % (...)` **órfão** → `SyntaxError: unmatched
   ')'`. `_consertar-pepino-gerador.py` conserta **estruturalmente**: toda linha que começa
   com `).replace(` cola na anterior, sem o `)`; e `%%` volta a `%`. **Prova:** `compile()`
   do resultado antes de gravar.
3. **Regex de bloco, off-by-one:** `def x\\(.*?\\n(?=\\n\\n\\ndef y)` **nunca casa** — o `.*?\\n`
   já consome um `\\n`, então o lookahead precisa de **um a menos**.
4. **Regex ancorado em `\\n\\n#` engole as funções seguintes.** O bloco do `bulbo_alho` vai até
   o comentário da cena 1, então engole `lab` e `nuvem_lab`. O script agora **conta
   `def <nome>` depois** de trocar e aborta se algum sumiu.

### 👁️ A ferramenta que faltava: `_zoom-cena.py`

A folha de contato do `_revisar-cenas.py` renderiza em **tamanho nativo (405×720)**. Isso
basta para **layout** — e **não basta para forma**.

```bash
python _zoom-cena.py <arquivo>.html 3 --escala 3     # cena 3, 3x
python _zoom-cena.py <arquivo>.html 0,3,5            # várias, uma por PNG
```

### 🎨 As formas que só o zoom pegou

| O que estava | O que lia | Conserto |
|---|---|---|
| dente de alho = gota simétrica | **pingo d'água** | lado esquerdo RETO + **faixa clara da face do corte** |
| rodela de pepino = elipse lisa | **azeitona** | anel de casca + miolo pálido + **sementes** |
| bulbo = 1 silhueta com 8 lóbulos | **concha / pinha** | 5 dentes separados, cada um com o seu contorno |
| bulbo = 5 dentes soltos | **flor de pétalas** + colo flutuando | **casca** (silhueta pálida pontilhada) amarrando os dentes |
| bulbo alto e bicudo | **botão / cebola** | **atarracado**: 124 de largura × 122 de altura |

**A lição nova:** o desenho passa por **três ou quatro leituras erradas** antes de acertar,
e cada uma só aparece **renderizando**. Nenhuma apareceu no grep nem no validador.

### 📐 Cena 4 do kombucha: o selo colado nas DUAS bordas

`WHY THE APPLE AND NOT THE MELON` (33 caracteres, 17px) **encostava nos dois lados** do
cartão de 340. É a **mesma família** do selo estreito do pão (#16) — só que por texto
**grande**, não por caixa pequena. Conserto: **encurtar o inglês** → `THE APPLE, NOT THE
MELON` (24 caracteres).

### 💡 Substância trocada (não é verniz)

A cena 7 do pepino dizia **"DO NOT BLANCH IT"** — espantalho: ninguém escalda pepino em
conserva. Trocada por **"TRIM THE BLOSSOM END"** — é ali que ficam as enzimas que amolecem
a conserva. Conselho que ninguém espera.

### 📦 Registro nos 3 lugares

`_registrar-novos-videos.py` valida **os três arquivos primeiro** e só então grava — se
gravasse por arquivo, uma falha no pacote deixaria a galeria já alterada.

| Arquivo | O que entrou |
|---|---|
| `_gerar-galeria.py` | `'kombucha': 'Kombucha'` no `ROTULO` + `'kombucha'` na `ORDEM` |
| `guias/pacote-legendas-descricoes-en.md` | entradas **#22** e **#23**, linha no QUICK CHART, Semanas 13/14, linhas 22/23 na tabela |
| `guias/plano-de-postagem.md` | **Semana 14** com a substância + contagens 21→23 e 13→15 semanas |

Galeria regerada: **51 shorts, 0 com bug**, 19 só aviso.
'''

TROCAS_MEM = [
    ('## 📊 Catálogo — 21 entradas no pacote',
     '## 📊 Catálogo — 23 entradas no pacote', 1),
    ('(**#1 a #21**)', '(**#1 a #23**)', 1),
    ("- **#17** pepino+maçã · **#18** cenoura+maçã · **#19** beterraba+alho ·\n"
     "  **#20** couve-flor+maçã · **#21** pão/levain (`pao/`, 1º não-legume da série).\n"
     "- **Todos com original PT** — a série é original PT + irmão `-en`.",
     "- **#17** pepino+maçã · **#18** cenoura+maçã · **#19** beterraba+alho ·\n"
     "  **#20** couve-flor+maçã · **#21** pão/levain (`pao/`, 1º não-legume da série) ·\n"
     "  **#22** pepino+alho · **#23** kombucha melancia+maçã (`kombucha/`, 1ª **bebida**).\n"
     "- **Quase todos com original PT** (a série é original PT + irmão `-en`) —\n"
     "  **#22 e #23 são só EN**, construídos em inglês a pedido do usuário.", 1),
    ('- **Com mp4 — 20 dos 21.** Falta o **#13**',
     '- **Com mp4 — 22 dos 23.** Falta o **#13**', 1),
]


def main():
    # ---- 1. log diario (append-only)
    with io.open(LOG, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    velho = FIM_DO_LOG.replace('\n', eol)
    if d.count(velho) != 1:
        print('ERRO no log: o fim do arquivo casou %d vez(es)' % d.count(velho))
        return 1
    novo = NOVO_LOG.replace('\n', eol)
    if 'kombucha de melancia' in d:
        print('  (log ja tinha a entrada de hoje — nao duplico)')
    else:
        d = d.replace(velho, novo)
        with io.open(LOG, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d)
        print('  ok: log -> %d bytes' % len(d.encode('utf-8')))

    # ---- 2. MEMORY.md (ancoras contadas)
    with io.open(MEM, 'r', encoding='utf-8', newline='') as fh:
        m = fh.read()
    m_eol = '\r\n' if m.count('\r\n') else '\n'
    antes = len(m.encode('utf-8'))
    for velho, novo, esperado in TROCAS_MEM:
        v = velho.replace('\n', m_eol)
        n = novo.replace('\n', m_eol)
        c = m.count(v)
        if c != esperado:
            print('ERRO no MEMORY.md: ancora casou %d (esperado %d): %r'
                  % (c, esperado, velho[:55]))
            return 1
        m = m.replace(v, n)
    with io.open(MEM, 'w', encoding='utf-8', newline='') as fh:
        fh.write(m)
    print('  ok: MEMORY.md %d -> %d bytes' % (antes, len(m.encode('utf-8'))))
    print('OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
