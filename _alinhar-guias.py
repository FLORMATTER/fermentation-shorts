# -*- coding: utf-8 -*-
"""Alinha README e o guia antigo com o pacote novo. Uma ancora errada = nao grava nada."""
R = 'README.md'
G = 'guias/como-virar-video-de-verdade.md'
r = open(R, encoding='utf-8').read()
g = open(G, encoding='utf-8').read()
r0, g0 = len(r), len(g)


def troca(d, velho, novo, n=1, onde=''):
    c = d.count(velho)
    assert c == n, '[%s] ancora casou %d vez(es) (esperado %d): %r' % (onde, c, n, velho[:70])
    return d.replace(velho, novo)


# ---- README 1: o repolho do desenho e verde, nao roxo --------------------
r = troca(r, "| Repolho | **RED CABBAGE** |", "| Repolho | **CABBAGE** |", 1, R)

# ---- README 2: o pacote agora tem 13 videos ------------------------------
r = troca(r, "| `guias/pacote-legendas-descricoes-en.md` | Títulos, descrições e hashtags dos 11 vídeos |",
             "| `guias/pacote-legendas-descricoes-en.md` | Títulos, descrições e hashtags dos **13 vídeos** (12 Shorts + 1 vídeo longo) |", 1, R)

# ---- README 3: apontar para o plano de postagem --------------------------
r = troca(r, """3. **Montar e publicar.** Use `guias/guia-capcut-pc.html` para editar e o
   `video-longo/titulo-descricao-video-longo.md` para o título e a descrição.""",
             """3. **Montar e publicar.** Use `guias/guia-capcut-pc.html` para editar e o
   `video-longo/titulo-descricao-video-longo.md` para o título e a descrição.

**Plano completo — 7 semanas, vídeo por vídeo, com o arquivo exato a abrir:**
`guias/plano-de-postagem.md`""", 1, R)

# ---- GUIA 1: frequencia coerente (2 por semana) --------------------------
g = troca(g, "4. **Poste com constância** — 3x por semana, por 3 meses",
             "4. **Poste com constância** — 2x por semana, por 3 meses", 1, G)

# ---- GUIA 2: titulo tem que vir do pacote (e em ingles) ------------------
g = troca(g, """5. **Título:** escreva algo curto e curioso. Exemplo:
   - `Rabanete fermentado em 5 dias 🌶️`
   - `O legume mais rápido de fermentar`""",
             """5. **Título e descrição:** copie do pacote em inglês —
   `guias/pacote-legendas-descricoes-en.md`. Cada vídeo tem o título dele lá.
   ⚠️ **Não invente título genérico e não repita título entre dois vídeos.**""", 1, G)

open(R, 'w', encoding='utf-8').write(r)
open(G, 'w', encoding='utf-8').write(g)
print('README %d -> %d bytes' % (r0, len(r)))
print('GUIA   %d -> %d bytes' % (g0, len(g)))
